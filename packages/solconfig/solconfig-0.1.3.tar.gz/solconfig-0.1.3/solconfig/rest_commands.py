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

    def exec(commands, option:BrokerOption, retry_on_not_allow=False):
        get_semp_error = retry_on_not_allow
        retry_commands = []
        for c in commands:
            logging.info("{:<6} {}".format(c["verb"].upper(), c["uri"]))
            error = RestCommands.http(option, c["verb"], option.base_url+c["uri"], c["data_json"], get_semp_error=get_semp_error)
            if retry_on_not_allow:
                if error.get("code") == 89 and \
                    error.get("status") == "NOT_ALLOWED":
                    logging.warn("{}({}), {}, retry it later"
                        .format(error.get("status"), error.get("code"), error.get("description")))
                    retry_commands.append(c)
                elif error.get("code", 0) != 0:
                    raise RuntimeError("SEMP Error: {}".format(json.dumps(error, indent=2)))

        if retry_on_not_allow and len(retry_commands) > 0:
            RestCommands.exec(retry_commands, option)


    @staticmethod
    def http(option:BrokerOption, verb:str, url:str, data_json=None, get_broker_server=False, get_semp_error=False):
        """Submit REST request and retrun the response in json format"""

        headers={"content-type": "application/json"}
        params = {"opaquePassword": option.opaque_password} if len(option.opaque_password) > 0 else {}
        str_json = json.dumps(data_json, indent=2) if data_json != None else None
        r = getattr(requests, verb)(url, headers=headers,
            params=params,
            auth=option.request_auth,
            data=(str_json),
            verify=option.request_verify)

        if r.status_code != 200:
            if not get_semp_error: raise RuntimeError(r.text)
            try:
                return r.json()["meta"]["error"]
            except:
                raise RuntimeError(r.text)
        else:
            if get_broker_server:
                option.serverVersion = r.headers.get("Server", None)
            return r.json()
