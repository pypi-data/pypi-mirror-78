import os
from jinja2 import Environment, FileSystemLoader
import json

from solconfig.spec import Spec
from solconfig.rest_commands import RestCommands

class Config:
    def __init__(self, spec_definition):
        self.spec_definition = spec_definition
        pass

    def read_config_file(self, filename:str):
        """Read the config json file and perform jinja2 templating"""
        
        filedir=os.path.dirname(os.path.abspath(filename))
        filename=os.path.basename(filename)
        e = Environment(
            loader=FileSystemLoader(filedir), 
            trim_blocks=True, 
            lstrip_blocks=True)
        config_txt = e.get_template(filename).render()
        result = json.loads(config_txt)

        return result

    @staticmethod
    def generate_update_commands_recursively(
        rest_commands:RestCommands, parent_uri, coll_name, new_json, old_json, obj_def):
        # skip this reserved object
        if Spec.is_reserved_object(old_json, obj_def):
            return

        # build collention url and object url for this object
        id_uri = Spec.build_identifiers_uri(new_json, obj_def)
        collention_uri = parent_uri+"/"+coll_name
        object_uri = collention_uri+"/"+id_uri

        # Extract the payload of this object
        new_payload = Spec.extract_payload(new_json, obj_def)
        old_payload = Spec.extract_payload(old_json, obj_def)

        # update current object
        requires_disable = Spec.is_requires_disable_need(new_json, old_json, obj_def)
        if requires_disable: # means new_json["enabled"]==True
            new_payload["enabled"]=False

        if new_payload != old_payload:
            new_temp = new_payload.copy()
            old_temp = old_payload.copy()
            new_enable = new_temp.pop("enabled", obj_def["Defaults"]["enabled"])
            old_temp.pop("enabled", obj_def["Defaults"]["enabled"])            
            if new_temp == old_temp:
                # means old_enabled == True, disable it, other attributes unchanged
                rest_commands.append("patch", object_uri, {"enabled":new_enable})
            else:
                # PUT method, other attributes set to default
                rest_commands.append("put", object_uri, new_payload)
        # else
            # old_payload == new_payload: nothing to change
        commands_len = len(rest_commands.commands)

        # recursively process all children objects
        for child_coll_name, child_obj_def in obj_def["Children"].items():
            if child_coll_name in old_json:
                if child_coll_name in new_json:
                    # This child_coll in both new and old json
                    Config.compare_two_collection(rest_commands, object_uri, child_coll_name, 
                        new_json[child_coll_name], old_json[child_coll_name], child_obj_def)
                else:
                    # in old one only,, just delete them
                    for child_obj in old_json[child_coll_name]:
                        Config.generate_delete_commands_recursively(rest_commands, object_uri, child_coll_name, child_obj, child_obj_def)
            elif child_coll_name in new_json:
                # in new one only, create them
                for child_obj in new_json[child_coll_name]:
                    Config.generate_new_commands_recursively(rest_commands, object_uri, child_coll_name, child_obj, child_obj_def)
            else:
                continue

        if not requires_disable: return

        if commands_len > 0 and \
            commands_len == len(rest_commands.commands) and \
            "patch" == rest_commands.commands[-1]["verb"] and \
            {"enabled":False} == rest_commands.commands[-1]["data_json"]:
            # Noting to do since the previous action is just to simplely deisable the object
            rest_commands.commands.pop()
        else:
            # Enable the object after the Requires-Disable attributes are changed
            rest_commands.append("patch", object_uri, {"enabled":True})
            

    @staticmethod
    def compare_two_collection(rest_commands, object_url, coll_name, new_list, old_list, obj_def):
        while len(old_list)>0:
            find_match = False
            old_obj = old_list.pop(0)
            old_id_uri = Spec.build_identifiers_uri(old_obj, obj_def)
            for new_idx, new_obj in enumerate(new_list):
                new_id_uri = Spec.build_identifiers_uri(new_obj, obj_def)
                if new_id_uri == old_id_uri:
                    find_match = True
                    break
            if find_match:
                Config.generate_update_commands_recursively(rest_commands, object_url, coll_name, new_obj, old_obj, obj_def)
                new_list.pop(new_idx)
            else:
                # old only objects
                Config.generate_delete_commands_recursively(rest_commands, object_url, coll_name, old_obj, obj_def)

        for new_obj in new_list:
                # this is a new only object
                Config.generate_new_commands_recursively(rest_commands, object_url, coll_name, new_obj, obj_def)            

        return


    def generate_new_commands(self, config_json) -> RestCommands:
        rest_commands = RestCommands()
        for coll_name in Spec.TOP_COLLECTIONS:
            for obj_json in config_json.get(coll_name, []):
                Config.generate_new_commands_recursively(
                    rest_commands, "", coll_name, obj_json, self.spec_definition[coll_name])
        return rest_commands

    @staticmethod
    def generate_new_commands_recursively(rest_commands:RestCommands, parent_uri, coll_name, obj_json, obj_def):
        #Extract the payload of this object
        payload = Spec.extract_payload(obj_json, obj_def)

        # build collention url and object url for this object
        id_uri = Spec.build_identifiers_uri(obj_json, obj_def)
        collention_uri = parent_uri+"/"+coll_name
        object_uri = collention_uri+"/"+id_uri

        requires_disable = Spec.is_requires_disable_on_children_update_need(obj_json, obj_def)
        if requires_disable:
            payload["enabled"]=False

        if Spec.is_build_in_object(obj_json, obj_def):
            # This is a existed built-in object
            # Patch to update this existed object
            rest_commands.append("patch", object_uri, payload)
        else:
            # Post to create new object
            rest_commands.append("post", collention_uri, payload)

        # recursively process all children
        for child_coll_name, child_obj_def in obj_def["Children"].items():
            if child_coll_name not in obj_json:
                continue
            for child_obj in obj_json[child_coll_name]:
                Config.generate_new_commands_recursively(rest_commands, object_uri, child_coll_name, child_obj, child_obj_def)

        if requires_disable:
            # Enable the object after the Requires-Disable children are changed
            rest_commands.append("patch", object_uri, {"enabled":True})

    def remove_special_attributes(self, config_json, reserve_default_value=False, reserve_deprecated=False):
        self.reserve_default_value = reserve_default_value
        self.reserve_deprecated = reserve_deprecated
        for coll_name in Spec.TOP_COLLECTIONS:
            for obj_json in config_json.get(coll_name, []):
                self._remove_special_attributes_recursively(
                    obj_json, 
                    self.spec_definition[coll_name],
                    parent_identifiers=[])
        pass


    def _remove_special_attributes_recursively(self, obj_json, obj_def, parent_identifiers):
        remove_parent_identifiers(obj_json, parent_identifiers)
        if not self.reserve_default_value:
            remove_default_values(obj_json, obj_def)
        if not self.reserve_deprecated:
            remove_particular_attributes(obj_json, obj_def, "Deprecated")

        parent_identifiers_for_child = parent_identifiers + obj_def["Identifiers"]
        for child_coll_name, child_obj_def in obj_def["Children"].items():
            if child_coll_name not in obj_json: # skip empty elements
                continue
            
            # Remove reserved objects
            obj_json[child_coll_name][:] = [child_obj for child_obj in obj_json[child_coll_name] \
                if not  Spec.is_reserved_object(child_obj, child_obj_def)]

            for child_obj in obj_json[child_coll_name]:
                self._remove_special_attributes_recursively(child_obj, child_obj_def, parent_identifiers_for_child)

    def generate_delete_commands(self, config_json) -> RestCommands:
        rest_commands = RestCommands()
        for coll_name in Spec.TOP_COLLECTIONS:
            for obj_json in config_json.get(coll_name, []):
                Config.generate_delete_commands_recursively(
                    rest_commands, "", coll_name, obj_json, self.spec_definition[coll_name])
        return rest_commands

    @staticmethod
    def generate_delete_commands_recursively(rest_commands:RestCommands, parent_uri, coll_name, obj_json, obj_def):
        # Skip the delete operation for build-in or reserved objects
        if Spec.is_build_in_object(obj_json, obj_def): return
        if Spec.is_reserved_object(obj_json, obj_def): return

        #1. build the uri for current object
        id_uri = Spec.build_identifiers_uri(obj_json, obj_def)
        object_uri = parent_uri+"/"+coll_name+"/"+id_uri

        requires_disable = Spec.is_requires_disable_on_children_update_need(obj_json, obj_def)
        if requires_disable:
            # disable this object before deleting its children
            rest_commands.append("patch", object_uri, {"enabled":False})

        #3. recursively process all children
        for child_coll_name, child_obj_def in obj_def["Children"].items():
            if child_coll_name not in obj_json:
                continue
            for child_obj in obj_json[child_coll_name]:
                Config.generate_delete_commands_recursively(rest_commands, object_uri, child_coll_name, child_obj, child_obj_def)

        #4. delete current element
        rest_commands.append("delete", object_uri)

def remove_default_values(obj_json, obj_def):
    """remove attributes with default values"""
    Defaults = obj_def["Defaults"]
    for k, v in Defaults.items():
        if k in obj_json and obj_json[k] == v:
            obj_json.pop(k)

def remove_parent_identifiers(obj_json, parent_identifiers):
    """remove duplicated parent's identifiers"""
    for identify in parent_identifiers:
        if identify in obj_json:
            obj_json.pop(identify)

def remove_particular_attributes(obj_json, obj_def, particular):
    to_delete = obj_def[particular]
    for key_name in to_delete:
        obj_json.pop(key_name, "")
