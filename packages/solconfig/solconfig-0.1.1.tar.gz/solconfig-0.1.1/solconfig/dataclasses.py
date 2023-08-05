from typing import Any
import logging
import sys

class CmdOption:
    admin_user  :str
    password    :str
    host        :str
    curl_only   :bool
    insecure    :bool
    ca_bundle   :str
    verbose     :bool
    base_url    :str
    request_verify: Any
    request_auth: tuple
    opaque_password: str

    def __init__(self, admin_user :str, password :str, host :str, curl_only :bool, insecure :bool, ca_bundle :str, verbose :bool):

        self.admin_user = admin_user
        self.password   = password  
        self.host       = host      
        self.curl_only  = curl_only 
        self.insecure   = insecure  
        self.ca_bundle  = ca_bundle 
        self.verbose    = verbose   

        if self.host[-1]=='/': self.host=self.host[:-1]
        self.base_url = self.host+"/SEMP/v2/config"

        if len(self.ca_bundle)>0:
            self.request_verify = self.ca_bundle
        else:
            self.request_verify = not self.insecure
        self.request_auth=(self.admin_user, self.password)
        self.opaque_password=""

    def set_opaque_password(self, opaque_password:str):
        l = len(opaque_password)
        if l > 0 and self.host[:5].upper() != "HTTPS":
            logging.error("Opaque Password query is only supported over HTTPS, this current host is {}!" \
                .format(self.host))
            sys.exit()
        if l>0 and (l<8 or l>128):
            logging.error("Opaque Password must be between 8 and 128 characters inclusive!")
            sys.exit()
        self.opaque_password = opaque_password
