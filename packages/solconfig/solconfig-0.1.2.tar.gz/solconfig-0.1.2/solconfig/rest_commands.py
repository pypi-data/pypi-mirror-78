import json
import logging
import requests

from solconfig.dataclasses import *

class RestCommands:
    commands : list

    def __init__(self):
        self.commands = []
        pass

    def __str__(self):
        return json.dumps(self.commands, indent=2)

    def append(self, verb, uri, data_json=None):
#        self.commands.append(RestCommand(verb, uri, data_json))
        self.commands.append({"verb":verb, "uri":uri, "data_json":data_json})

    def build_curl_commands(self, option:BrokerOption):
        print("#!/bin/sh +x")
        print("export HOST={}".format(option.base_url))
        print("export ADMIN={}".format(option.admin_user))
        print("export PWD={}".format(option.password))

        for c in self.commands:
            print("")
            curl_cmd = "curl -X {} -u $ADMIN:$PWD $HOST{}".format(c["verb"].upper(), c["uri"])
            if c["data_json"] !=None:
                curl_cmd += """ -H 'content-type: application/json' -d '
{}'""".format(json.dumps(c["data_json"], indent=2))
            print(curl_cmd)

    def exec(self, option:BrokerOption):
        for c in self.commands:
            logging.info("{:<6} {}".format(c["verb"].upper(), c["uri"]))
            RestCommands.http(option, c["verb"], option.base_url+c["uri"], c["data_json"])
            pass


    @staticmethod
    def http(option:BrokerOption, verb:str, url:str, data_json=None, get_broker_server=False):
        """Submit REST request and retrun the response in json format"""

        headers={"content-type": "application/json"}
        params = {"opaquePassword": option.opaque_password} if len(option.opaque_password) > 0 else {}
        str_json = json.dumps(data_json, indent=2) if data_json != None else None
        r = getattr(requests, verb)(url, headers=headers,
            params=params,
            auth=option.request_auth,
            data=(str_json),
            verify=option.request_verify)

        if (r.status_code != 200):
            raise RuntimeError(r.text)
        else:
            if get_broker_server:
                option.serverVersion = r.headers.get("Server", None)
            return r.json()
