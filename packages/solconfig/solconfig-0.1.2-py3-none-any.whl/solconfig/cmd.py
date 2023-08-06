import click
import logging
import json
import pkg_resources

from solconfig.solconfig import BrokerOption, SolConfig

logging.basicConfig(level=logging.INFO)

@click.group()
@click.version_option(pkg_resources.get_distribution('solconfig').version)
@click.option('-u', '--admin-user', default='admin', show_default=True,
    help='The username of the management user')
@click.option('-p', '--admin-password', default='admin', show_default=True,
    envvar='SOL_ADMIN_PWD', help='The password of the management user, could be set by env variable [SOL_ADMIN_PWD]')
@click.option('-h', '--host', default='http://localhost:8080', show_default=True,
    help='URL to access the management endpoint of the broker')
@click.option('--curl-only', default=False, show_default=True, is_flag=True,
    help='Output curl commands only, no effect on BACKUP command')
@click.option('--insecure', default=False, show_default=True, is_flag=True,
    help='Allow insecure server connections when using SSL')
@click.option('--ca-bundle', default='',
    help='The path to a CA_BUNDLE file or directory with certificates of trusted CAs')
@click.pass_context
def cli(ctx, admin_user, admin_password, host, curl_only, insecure, ca_bundle):
    """Backing Up and Restoring Solace PubSub+ Broker Configuration with SEMPv2 protocol
    
    Use the "backup" command to export the configuration of objects on a PS+  Broker into a single JSON, 
    then use the "create" or "update" command to restore the configuration."""
    cmd_option = BrokerOption(admin_user, admin_password, host, curl_only, insecure, ca_bundle, False)
    solconfig = SolConfig(cmd_option)
    ctx.ensure_object(dict)
    ctx.obj["SOLCONFIG"] = solconfig


# -----------------------------sub commands-----------------------------
TYPE_2_COLL_NAME = {
    "vpn": "msgVpns", 
    "cluster":"dmrClusters",
    "ca":"certAuthorities"
}

@cli.command(name="backup")
@click.argument('object_type', type=click.Choice(TYPE_2_COLL_NAME.keys()))
@click.argument('object_names')
@click.option('--reserve-default-value', default=False, show_default=True, is_flag=True,
    help='Reserve the attributes with default value, by default they are removed to make the result JSON more concise')
@click.option('--reserve-deprecated', default=False, show_default=True, is_flag=True,
    help='Reserve the deprecated attributes for possible backward compatibility')
@click.option('-o', '--opaque-password', default='',
    help="""The opaquePassword for receiving opaque properties like the password of Client Usernames.
    
    Before version 9.6.x (sempVersion 2.17), there is no way to get the value of "write-only" attributes
    like the password of Client Usernames, so that the backup output is not 100 percent as same as the
    configuration on the PS+ broker. Means you need to set those "write-only" attributes manually after
    your restore the configuration.
    
    Since version 9.6.x (sempVersion 2.17), with a password is provided in the opaquePassword query parameter,
    attributes with the opaque property (like the password of Client Usernames) are retrieved in a GET in
    opaque form, encrypted with this password.
    
    The backup output is now 100 percent as same as the configuration on the PS+ broker, and the same 
    opaquePassword is used to restore the configuration.
    
    The opaquePassword is only supported over HTTPS, and must be between 8 and 128 characters inclusive!""")
@click.pass_context
def backup(ctx, object_type, object_names, reserve_default_value, reserve_deprecated, opaque_password):
    """Export the whole configuration of objects into a single JSON

    OBJECT_NAMES is a comma-separated list of names, like "vpn01" or "vpn01,vpn02", or "*" means all."""

    solconfig = ctx.obj["SOLCONFIG"]
    # fetch spec and api first without opaque_password
    solconfig.fetch_spec_and_api()
    solconfig.option.set_opaque_password(opaque_password)
    result = solconfig.backup(TYPE_2_COLL_NAME[object_type], 
        object_names, reserve_default_value, reserve_deprecated, opaque_password)
    print(json.dumps(result, indent=2))


@cli.command(name="delete")
@click.argument('object_type', type=click.Choice(TYPE_2_COLL_NAME.keys()))
@click.argument('object_names')
@click.pass_context
def delete(ctx, object_type, object_names):
    """Delete the specified objects
    
    OBJECT_NAMES is a comma-separated list of names, like "vpn01" or "vpn01,vpn02", or "*" means all."""

    solconfig = ctx.obj["SOLCONFIG"]
    solconfig.fetch_spec_and_api()
    solconfig.delete(TYPE_2_COLL_NAME[object_type], object_names)


@cli.command(name="create")
@click.argument('config-file', type=click.Path(exists=True))
@click.pass_context
def create(ctx, config_file):
    """Create objects from the configuration file
    
    It will NOT touch objects already existed"""
    broker = ctx.obj["SOLCONFIG"]
    broker.fetch_spec_and_api()
    broker.create(config_file)


@cli.command(name="update")
@click.argument('config-file', type=click.Path(exists=True))
@click.pass_context
def update(ctx, config_file):
    """**READ HELP BEFORE YOU USE THIS COMMAND**
    
    Update the existing objects in the PS+ Broker to make them the same as the configuration file. 

    Be careful, it will DELETE existing objects like Queues or Client Usernames, etc on the PS+ broker
    if they are absent in the configuration file.
    
    This "update" command is a good complement to "create" command, especially for the
    "default" VPN or the VPN of the Solace Cloud Service instance, since you can only update them.
    """

    solconfig = ctx.obj["SOLCONFIG"]
    solconfig.fetch_spec_and_api()
    solconfig.update(config_file)
