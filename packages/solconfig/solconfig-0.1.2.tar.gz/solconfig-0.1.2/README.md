# Backing Up and Restoring [Solace](https://solace.com/) PubSub+ Broker Configuration with [SEMPv2](https://docs.solace.com/SEMP/SEMP-API-Ref.htm) protocol

## Install

Run `pip install solconfig` to install this tool.

## Usage

Use the "backup" command to export the configuration of objects on a PS+ Broker into a single JSON,  then use the "create" or "update" command to restore the configuration.

Check the help message of each command carefully before you use it.

```bash
$ solconfig --help
Usage: solconfig [OPTIONS] COMMAND [ARGS]...

  Backing Up and Restoring Solace PubSub+ Broker Configuration with SEMPv2
  protocol

  Use the "backup" command to export the configuration of objects on a PS+
  Broker into a single JSON,  then use the "create" or "update" command to
  restore the configuration.

Options:
  --version                  Show the version and exit.
  -u, --admin-user TEXT      The username of the management user  [default:
                             admin]

  -p, --admin-password TEXT  The password of the management user, could be set
                             by env variable [SOL_ADMIN_PWD]  [default: admin]

  -h, --host TEXT            URL to access the management endpoint of the
                             broker  [default: http://localhost:8080]

  --curl-only                Output curl commands only, no effect on BACKUP
                             command  [default: False]

  --insecure                 Allow insecure server connections when using SSL
                             [default: False]

  --ca-bundle TEXT           The path to a CA_BUNDLE file or directory with
                             certificates of trusted CAs

  --help                     Show this message and exit.

Commands:
  backup  Export the whole configuration of objects into a single JSON...
  create  Create objects from the configuration file It will NOT touch...
  delete  Delete the specified objects OBJECT_NAMES is a comma-separated...
  update  **READ HELP BEFORE YOU USE THIS COMMAND** Update the existing...
```

### BACKUP: Export the whole configuration of objects into a single JSON

```bash
$ solconfig backup --help
Usage: solconfig backup [OPTIONS] [vpn|cluster|ca] OBJECT_NAMES

  Export the whole configuration of objects into a single JSON

  OBJECT_NAMES is a comma-separated list of names, like "vpn01" or
  "vpn01,vpn02", or "*" means all.

Options:
  --reserve-default-value     Reserve the attributes with default value, by
                              default they are removed to make the result JSON
                              more concise  [default: False]

  --reserve-deprecated        Reserve the deprecated attributes for possible
                              backward compatibility  [default: False]

  -o, --opaque-password TEXT  The opaquePassword for receiving opaque
                              properties like the password of Client
                              Usernames.

                              Before version 9.6.x (sempVersion 2.17), there
                              is no way to get the value of "write-only"
                              attributes like the password of Client
                              Usernames, so that the backup output is not 100
                              percent as same as the configuration on the PS+
                              broker. Means you need to set those "write-only"
                              attributes manually after your restore the
                              configuration.

                              Since version 9.6.x (sempVersion 2.17), with a
                              password is provided in the opaquePassword query
                              parameter, attributes with the opaque property
                              (like the password of Client Usernames) are
                              retrieved in a GET in opaque form, encrypted
                              with this password.

                              The backup output is now 100 percent as same as
                              the configuration on the PS+ broker, and the
                              same  opaquePassword is used to restore the
                              configuration.

                              The opaquePassword is only supported over HTTPS,
                              and must be between 8 and 128 characters
                              inclusive!

  --help                      Show this message and exit.
```

### CREATE: Create objects from the configuration file

```bash
$ solconfig create --help
Usage: solconfig create [OPTIONS] CONFIG_FILE

  Create objects from the configuration file

  It will NOT touch objects already existed

Options:
  --help  Show this message and exit.
```

### UPDATE: Update existing objects in the Broker from the configuration file

```bash
solconfig update --help
Usage: solconfig update [OPTIONS] CONFIG_FILE

  **READ HELP BEFORE YOU USE THIS COMMAND**

  Update the existing objects in the PS+ Broker to make them the same as the
  configuration file.

  Be careful, it will DELETE existing objects like Queues or Client
  Usernames, etc on the PS+ broker if they are absent in the configuration
  file.

  This "update" command is a good complement to "create" command, especially
  for the "default" VPN or the VPN of the Solace Cloud Service instance,
  since you can only update them.

Options:
  --help  Show this message and exit.
```

### DELETE: Delete the specified objects

```bash
solconfig delete --help
Usage: solconfig delete [OPTIONS] [vpn|cluster|ca] OBJECT_NAMES

  Delete the specified objects

  OBJECT_NAMES is a comma-separated list of names, like "vpn01" or
  "vpn01,vpn02", or "*" means all.

Options:
  --help  Show this message and exit.
```
