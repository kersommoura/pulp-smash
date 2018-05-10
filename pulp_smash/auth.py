# coding=utf-8
"""A client for working with Pulp's API."""

# Tools for managing information about hosts under test.

from requests import HTTPBasicAuth
from packaging.version import Version

from pulp_smash import api, config, cli


def get_auth(cfg=None):
    if not cfg:
        cfg = config.get_config()
    if cfg.pulp_version > Version('3'):
        return HTTPBasicAuth(cfg.pulp_auth[0], cfg.pulp_auth[1])
    else:
        return

def pulp2_admin_login(server_config):
    """Execute ``pulp-admin login``.
    :param pulp_smash.config.PulpSmashConfig server_config: Information about
        the Pulp server being targeted.
    :return: The completed process.
    :rtype: pulp_smash.cli.CompletedProcess
    """
    return cli.Client(server_config).run((
        'pulp-admin', 'login', '-u', server_config.pulp_auth[0],
        '-p', server_config.pulp_auth[1]
    ))
