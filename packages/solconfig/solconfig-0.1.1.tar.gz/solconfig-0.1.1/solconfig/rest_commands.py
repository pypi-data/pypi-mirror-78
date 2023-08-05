import json
import logging
import requests

from solconfig.dataclasses import *

class RestCommand:
    verb: str
    uri: str
    data_json: dict

    def __init__(self, verb: str, uri: str, data_json: dict = None):
        self.verb = verb
        self.uri = uri
        self.data_json = data_json

class RestCommands:
    commands = []

    def append(self, verb, uri, data_json=None):
        self.commands.append(RestCommand(verb, uri, data_json))

    def build_curl_commands(self, option:CmdOption):
        print("#!/bin/sh +x")
        print("export HOST={}".format(option.base_url))
        print("export ADMIN={}".format(option.admin_user))
        print("export PWD={}".format(option.password))

        for c in self.commands:
            print("")
            curl_cmd = "curl -X {} -u $ADMIN:$PWD $HOST{}".format(c.verb.upper(), c.uri)
            if c.data_json !=None:
                curl_cmd += """ -H 'content-type: application/json' -d '
{}'""".format(json.dumps(c.data_json, indent=2))
            print(curl_cmd)

    def exec(self, option:CmdOption):
        for c in self.commands:
            logging.info("{:<6} {}".format(c.verb.upper(), c.uri))
            RestCommands.http(option, c.verb, option.base_url+c.uri, c.data_json)
            pass


    @staticmethod
    def http(option:CmdOption, verb:str, url:str, data_json=None):
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
            return r.json()
