from typing import Any
from dataclasses import dataclass, field
import logging
import sys

@dataclass
class CmdOption:
    admin_user  :str
    password    :str
    host        :str
    curl_only   :bool
    insecure    :bool
    ca_bundle   :str
    verbose     :bool
    base_url    :str = field(init=False)
    request_verify: Any = field(init=False)
    request_auth: tuple = field(init=False)
    opaque_password: str = field(default="")

    def __post_init__(self):
        if self.host[-1]=='/': self.host=self.host[:-1]
        self.base_url = self.host+"/SEMP/v2/config"

        if len(self.ca_bundle)>0:
            self.request_verify = self.ca_bundle
        else:
            self.request_verify = not self.insecure
        self.request_auth=(self.admin_user, self.password)

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
