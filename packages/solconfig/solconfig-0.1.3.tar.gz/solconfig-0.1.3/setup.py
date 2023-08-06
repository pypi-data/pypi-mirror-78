# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solconfig']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'jinja2>=2.11.2,<3.0.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['solconfig = solconfig.cmd:cli']}

setup_kwargs = {
    'name': 'solconfig',
    'version': '0.1.3',
    'description': 'Backing Up and Restoring Solace PubSub+ Broker Configuration with SEMPv2 protocol',
    'long_description': '# Backing Up and Restoring [Solace](https://solace.com/) PubSub+ Broker Configuration with [SEMPv2](https://docs.solace.com/SEMP/SEMP-API-Ref.htm) protocol\n\n## Install\n\nRun `pip install solconfig` to install this tool.\n\n## Usage\n\nUse the "backup" command to export the configuration of objects on a PS+ Broker into a single JSON,  then use the "create" or "update" command to restore the configuration.\n\nCheck the help message of each command carefully before you use it.\n\n```bash\n$ solconfig --help\nUsage: solconfig [OPTIONS] COMMAND [ARGS]...\n\n  Backing Up and Restoring Solace PubSub+ Broker Configuration with SEMPv2\n  protocol\n\n  Use the "backup" command to export the configuration of objects on a PS+\n  Broker into a single JSON,  then use the "create" or "update" command to\n  restore the configuration.\n\nOptions:\n  --version                  Show the version and exit.\n  -u, --admin-user TEXT      The username of the management user  [default:\n                             admin]\n\n  -p, --admin-password TEXT  The password of the management user, could be set\n                             by env variable [SOL_ADMIN_PWD]  [default: admin]\n\n  -h, --host TEXT            URL to access the management endpoint of the\n                             broker  [default: http://localhost:8080]\n\n  --curl-only                Output curl commands only, no effect on BACKUP\n                             command  [default: False]\n\n  --insecure                 Allow insecure server connections when using SSL\n                             [default: False]\n\n  --ca-bundle TEXT           The path to a CA_BUNDLE file or directory with\n                             certificates of trusted CAs\n\n  --help                     Show this message and exit.\n\nCommands:\n  backup  Export the whole configuration of objects into a single JSON...\n  create  Create objects from the configuration file It will NOT touch...\n  delete  Delete the specified objects OBJECT_NAMES is a comma-separated...\n  update  **READ HELP BEFORE YOU USE THIS COMMAND** Update the existing...\n```\n\n### BACKUP: Export the whole configuration of objects into a single JSON\n\n```bash\n$ solconfig backup --help\nUsage: solconfig backup [OPTIONS] [vpn|cluster|ca] OBJECT_NAMES\n\n  Export the whole configuration of objects into a single JSON\n\n  OBJECT_NAMES is a comma-separated list of names, like "vpn01" or\n  "vpn01,vpn02", or "*" means all.\n\nOptions:\n  --reserve-default-value     Reserve the attributes with default value, by\n                              default they are removed to make the result JSON\n                              more concise  [default: False]\n\n  --reserve-deprecated        Reserve the deprecated attributes for possible\n                              backward compatibility  [default: False]\n\n  -o, --opaque-password TEXT  The opaquePassword for receiving opaque\n                              properties like the password of Client\n                              Usernames.\n\n                              Before version 9.6.x (sempVersion 2.17), there\n                              is no way to get the value of "write-only"\n                              attributes like the password of Client\n                              Usernames, so that the backup output is not 100\n                              percent as same as the configuration on the PS+\n                              broker. Means you need to set those "write-only"\n                              attributes manually after your restore the\n                              configuration.\n\n                              Since version 9.6.x (sempVersion 2.17), with a\n                              password is provided in the opaquePassword query\n                              parameter, attributes with the opaque property\n                              (like the password of Client Usernames) are\n                              retrieved in a GET in opaque form, encrypted\n                              with this password.\n\n                              The backup output is now 100 percent as same as\n                              the configuration on the PS+ broker, and the\n                              same  opaquePassword is used to restore the\n                              configuration.\n\n                              The opaquePassword is only supported over HTTPS,\n                              and must be between 8 and 128 characters\n                              inclusive!\n\n  --help                      Show this message and exit.\n```\n\n### CREATE: Create objects from the configuration file\n\n```bash\n$ solconfig create --help\nUsage: solconfig create [OPTIONS] CONFIG_FILE\n\n  Create objects from the configuration file\n\n  It will NOT touch objects already existed\n\nOptions:\n  --help  Show this message and exit.\n```\n\n### UPDATE: Update existing objects in the Broker from the configuration file\n\n```bash\nsolconfig update --help\nUsage: solconfig update [OPTIONS] CONFIG_FILE\n\n  **READ HELP BEFORE YOU USE THIS COMMAND**\n\n  Update the existing objects in the PS+ Broker to make them the same as the\n  configuration file.\n\n  Be careful, it will DELETE existing objects like Queues or Client\n  Usernames, etc on the PS+ broker if they are absent in the configuration\n  file.\n\n  This "update" command is a good complement to "create" command, especially\n  for the "default" VPN or the VPN of the Solace Cloud Service instance,\n  since you can only update them.\n\nOptions:\n  --help  Show this message and exit.\n```\n\n### DELETE: Delete the specified objects\n\n```bash\nsolconfig delete --help\nUsage: solconfig delete [OPTIONS] [vpn|cluster|ca] OBJECT_NAMES\n\n  Delete the specified objects\n\n  OBJECT_NAMES is a comma-separated list of names, like "vpn01" or\n  "vpn01,vpn02", or "*" means all.\n\nOptions:\n  --help  Show this message and exit.\n```\n',
    'author': 'flyisland',
    'author_email': 'island.chen@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/flyisland/solconfig',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
