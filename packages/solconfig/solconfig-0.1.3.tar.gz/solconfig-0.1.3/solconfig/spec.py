import json
import re
from urllib.parse import quote_plus

# Objects that need to be disabled before modifying their "children"
RequiresDisableOnChildren_DEF = {
    "dmrClusters": [
        {
            "path": "links",
            "children": [
            "remoteAddresses"
            ]
        }
    ]
}
 

class Spec:
    sempVersion = ""
    definitions = dict()
    TOP_COLLECTIONS=["msgVpns", "dmrClusters", "certAuthorities"]

    def fromJson(self, spec_json):
        self._spec_json = spec_json
        self._all_paths =  spec_json['paths'].keys()
        for coll in Spec.TOP_COLLECTIONS:
            self.definitions[coll] = self.build_definitions("", coll)
            if coll not in RequiresDisableOnChildren_DEF: continue

            obj_def = self.definitions[coll]
            for rdc_def in RequiresDisableOnChildren_DEF[coll]:
                for path in rdc_def["path"].split("/"):
                    obj_def = obj_def["Children"][path]
                obj_def["RequiresDisableOnChildren"] = rdc_def["children"]


    def build_definitions(self, parent_path, collection_name):
        result = {}

        # build the collection path and find the object path
        collection_path = parent_path + "/" + collection_name

        # return None if there is no such resource there
        if (not self._spec_json
            .get("paths")
            .get(collection_path)):
            return None

        if(self._spec_json
            .get("paths")
            .get(collection_path)
            .get("get")
            .get("deprecated")):
            # This path has been deprecated!
            result["isDeprecated"]=True

        obj_re = re.compile("^"+collection_path+"/{[^/]+}$")
        obj_path = [path for path in self._all_paths if re.search(obj_re, path)][0]

        result = { ** result,
            ** self.generate_identifiers_from_object_path(obj_path),
            ** self.find_special_attributes(obj_path), 
            ** self.find_default_values(collection_path)}

        # find out all children collection name from paths
        children_re = re.compile(obj_path+"/([^/]+)$")
        children_coll_names = [re.search(children_re, path).group(1) for path in self._all_paths if re.search(children_re, path)]

        result["Children"] = {}
        for coll_name in children_coll_names:
            child_ef = self.build_definitions(obj_path, coll_name)
            result["Children"][coll_name] = child_ef

        return result


    def find_default_values(self, collection_path):
        coll_post_json = self._spec_json["paths"][collection_path]["post"]
        def_name = Spec.get_openapi_definition_name_from_post_json(coll_post_json)
        return {"Defaults": self._find_default_values_of_definition(def_name)}

    @staticmethod
    def get_openapi_definition_name_from_post_json(coll_post_json):
        ref = [p["schema"]["$ref"] for p in coll_post_json["parameters"] if p.get("name")=="body"][0]
        result = ref.split("/")[-1]
        return result

    def _find_default_values_of_definition(self, def_name):
        value_re = re.compile("The default value is `([^`]+)`.")
        properties = self._spec_json["definitions"][def_name]["properties"]

        result = {}
        for key in properties:
            p = properties[key]
            description = p.get("description", "")
            match = re.search(value_re, description)
            if not match: continue
            pType = p["type"]
            if   "integer" == pType:
                result[key] = int(match.group(1))
            elif "boolean" == pType:
                result[key] = True if match.group(1) == "true" else False
            elif "string"  == pType:
                # remove quote marks at both the begin and the end
                result[key] = match.group(1)[1:-1]
            else:
                raise TypeError("Unknown type '{}' of property '{}' of definition '{}', the default value is {}."\
                    .format(pType, key, def_name, match.group(1)))

        return result

    def find_special_attributes(self, obj_path):
        """
        Find special attributes from description like below:
Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated|Opaque
:---|:---:|:---:|:---:|:---:|:---:|:---:
accessType||||x||
msgVpnName|x|x||||
owner||||x||
permission||||x||
queueName|x|x||||
respectMsgPriorityEnabled||||x||
        """
        
        obj_path_json = self._spec_json["paths"][obj_path]
        # only **update** action provides description with "Requires-Disable"
        description = obj_path_json["patch"]["description"] if \
            obj_path_json.get("patch") else ""
        return Spec.generate_special_attributes_from_patch_description(description)

    @staticmethod
    def generate_special_attributes_from_patch_description(description):
        tempResult = {}
        for line in description.splitlines():
            attribute = line.split("|")
            if len(attribute) < 5 : continue
            for idx, val in enumerate(attribute):
                if val == "x":
                    tempResult[idx] = tempResult[idx] + [attribute[0]] if tempResult.get(idx) \
                        else [attribute[0]]

        idx2name = {2: "ReadOnly",3: "WriteOnly", 
                    4: "RequiresDisable", 5: "Deprecated", 6: "Opaque"}
        result = {}
        for idx in idx2name.keys():
            result[idx2name[idx]]=tempResult.get(idx, [])
        
        return result

    @staticmethod
    # /msgVpns/{msgVpnName}/aclProfiles/{aclProfileName}/publishTopicExceptions/{publishTopicExceptionSyntax},{publishTopicException}
    # -> {'Identifiers': [publishTopicExceptionSyntax, publishTopicException]}
    def generate_identifiers_from_object_path(obj_path):
        id_re = re.compile("{([^}]+)}")
        Identifiers = re.findall(id_re, obj_path.split("/")[-1])
        return {'Identifiers': Identifiers}

    @staticmethod
    def build_identifiers_uri(obj_json, obj_def):
        """Find out Identifiers and build the combined uri"""
        result = ",".join(
            [quote_plus(obj_json.get(id_name, "")) for id_name in obj_def["Identifiers"]])
        return result

    @staticmethod
    def get_object_names(obj_list, obj_def):
        names = [Spec.build_identifiers_uri(obj, obj_def) for obj in obj_list]
        return names

    @staticmethod
    def is_build_in_object(obj_json, obj_def) -> bool:
        """An new VPN will have these build-in objects, which can not be deleted.
        You could change the config of these objects."""
        id_uri = Spec.build_identifiers_uri(obj_json, obj_def)
        objs_has_build_in = ["aclProfileName", "clientProfileName", "clientUsername"]
        if id_uri == "default" and \
            obj_def["Identifiers"][0] in objs_has_build_in:
            return True
        else:
            return False

    @staticmethod
    def is_reserved_object(obj_json, obj_def) -> bool:
        """Objects starting with '#'->'%23' are reserved, they are managed
        by the system"""
        uri = Spec.build_identifiers_uri(obj_json, obj_def)
        return uri.startswith("%23")

    @staticmethod
    def extract_payload(obj_json, obj_def):
        """Extract the payload of this object"""
        result = {}
        for k in obj_json:
            if k not in obj_def["Children"]:
                result[k] = obj_json[k]
        return result

    @staticmethod
    def is_requires_disable_need(new_json, old_json, obj_def)->bool:
        """Check if the new configuration has different "RequiresDisable" attributes than the old one.
           Or if  there are special children need to be updated """

        if Spec.is_requires_disable_on_children_update_need(new_json, obj_def) or \
            Spec.is_requires_disable_on_children_update_need(old_json, obj_def):
            # Means this obj has "RequiresDisable" children, 
            # so it must has a "enabled" attribute with default value 'False'
            return new_json.get("enabled", obj_def["Defaults"]["enabled"])

        new_requires_disable_attr = [{k:new_json[k]} for k in obj_def["RequiresDisable"] if k in new_json]
        old_requires_disable_attr = [{k:old_json[k]} for k in obj_def["RequiresDisable"] if k in old_json]
        if new_requires_disable_attr == old_requires_disable_attr:
            return False
        
        # Means this obj has "RequiresDisable" attributes, 
        # so it must has a "enabled" attribute with default value 'False'       
        # If the enabled attribute of the new one is False already
        # then there is no need to disable it first to change it
        return new_json.get("enabled", obj_def["Defaults"]["enabled"])

    @staticmethod
    def is_requires_disable_on_children_update_need(obj_json, obj_def):
        if "RequiresDisableOnChildren" not in obj_def: return False
        if not obj_json.get("enabled", obj_def["Defaults"]["enabled"]): return False

        for child in obj_def["RequiresDisableOnChildren"]:
            if child in obj_json: return True
