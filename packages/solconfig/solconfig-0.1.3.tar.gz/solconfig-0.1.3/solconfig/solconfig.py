import json
import logging
import sys

from solconfig.dataclasses import *
from solconfig.util import *
from solconfig.spec import Spec
from solconfig.config import Config
from solconfig.rest_commands import RestCommands

class SolConfig:
    option : BrokerOption
    spec = Spec()
    config : Config

    def __init__(self, option):
        self.option = option

    def fetch_spec_and_api(self):
        # get sempVersion first
        api_json = RestCommands.http(self.option, "get", self.option.base_url+"/about/api",
            get_broker_server=True)
        self.option.set_sempVersion(dict_safe_get(api_json, "data", "sempVersion"))

        # get the spec of semp
        spec_json = RestCommands.http(self.option, "get", self.option.base_url+"/spec")
        self.spec.fromJson(spec_json)
        self.config = Config(self.spec.definitions)


    def backup(self, coll_name, obj_names, reserve_default_value=False, reserve_deprecated=False, 
            exit_on_not_found=True):

        name_list = obj_names.split(",")
        collection_uris = {}
        identifiers_name = "".join(self.spec.definitions[coll_name]["Identifiers"])
        for name in name_list:
            collection_uris[name] = \
                "{}/{}?where={}=={}"\
                .format(self.option.base_url, coll_name, identifiers_name, name)
        
        result = {"sempVersion": self.option.sempVersion}
        if len(self.option.opaque_password) > 0:
            result["opaquePassword"]=self.option.opaque_password
        self.get_collections_recursively(result, collection_uris, exit_on_not_found=exit_on_not_found)

        self.config.remove_special_attributes(result, reserve_default_value, reserve_deprecated)
        return result

    def delete(self,coll_name, obj_names):
        config_json = self.backup(coll_name, obj_names)
        rest_commands = self.config.generate_delete_commands(config_json)
        if self.option.curl_only:
            rest_commands.build_curl_commands(self.option)
        else:
            to_delete = query_yes_no("Do you want to continue to delete {} objects '{}'?"
                .format(coll_name, 
                ",".join(Spec.get_object_names(config_json[coll_name], self.spec.definitions[coll_name]))))
            if to_delete:
                RestCommands.exec(rest_commands.commands, self.option, retry_on_not_allow=True)

    def create(self, config_file_name):
        config_json = self.config.read_config_file(config_file_name)
        self.option.set_opaque_password(config_json.get("opaquePassword", ""))
        rest_commands = self.config.generate_new_commands(config_json)
        if self.option.curl_only:
            rest_commands.build_curl_commands(self.option)
        else:
            RestCommands.exec(rest_commands.commands, self.option)
        pass

    def update(self, config_file_name):
        config_json = self.config.read_config_file(config_file_name)
        self.option.set_opaque_password(config_json.get("opaquePassword", ""))
        rest_commands = RestCommands()
        is_object_not_found = False
        for coll_name in Spec.TOP_COLLECTIONS:
            if coll_name not in config_json: continue
            obj_def = self.spec.definitions[coll_name]

            for new_json in config_json[coll_name]:
                obj_name = Spec.build_identifiers_uri(new_json, obj_def)
                backup = self.backup(coll_name, obj_name, exit_on_not_found=False)
                old_collection = backup.get(coll_name, [])
                if len(old_collection) == 0:
                    is_object_not_found = True
                    logging.warn("The {} object '{}' is not existed!".format(coll_name, obj_name))
                    continue
                old_json = old_collection[0]
                Config.generate_update_commands_recursively(rest_commands, "", coll_name, new_json, old_json, obj_def)

        if len(rest_commands.commands) == 0:
            if not is_object_not_found:
                logging.info("The config file '{}' is identical to the existing objects."
                    .format(config_file_name))
            logging.info("Nothing to update.")
            return

        if self.option.curl_only:
            rest_commands.build_curl_commands(self.option)
        else:
            RestCommands.exec(rest_commands.commands, self.option)
        pass

    def get_collections_recursively(self, config_dict, collection_uris, exit_on_not_found=False):
        for key, coll_uri in collection_uris.items():
            # ignore the link pointed to itself
            if (key == "uri"): continue
            
            coll_name = SolConfig.get_collection_name_from_uri(coll_uri)
            list_of_data, list_of_links = self._get_collection(coll_uri)

            # skip empty objects
            if len(list_of_data)==0:
                if exit_on_not_found:
                    logging.error("The {} object '{}' is not found!"\
                        .format(coll_name, coll_uri.split("=")[-1]))
                    sys.exit()
                else:
                    continue
            
            if coll_name not in config_dict: config_dict[coll_name] = []
            obj_list = config_dict[coll_name]

            for i in range(len(list_of_data)):
                obj_list.append(list_of_data[i])
                self.get_collections_recursively(obj_list[-1], list_of_links[i])


    def _get_collection(self, coll_uri):
        list_of_data = []
        list_of_links = []

        while coll_uri: # there is next page
            resp_json = RestCommands.http(self.option, "get", coll_uri)
            list_of_data.extend(resp_json['data'])
            list_of_links.extend(resp_json['links'])
            coll_uri = dict_safe_get(resp_json, "meta","paging","nextPageUri")
        
        return list_of_data, list_of_links


    @staticmethod
    def get_collection_name_from_uri(coll_uri: str):
        result = coll_uri.split("/")[-1]
        result = result.split("?")[0]
        return result

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        print(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').")