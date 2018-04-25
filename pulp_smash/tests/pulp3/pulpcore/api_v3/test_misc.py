# coding=utf-8
"""Test miscelaenous."""
import unittest

from jsonschema import validate
from requests.exceptions import HTTPError

from pulp_smash import api, config, utils
from pulp_smash.tests.pulp3.constants import (
    API_DOCS_PATH,
    ARTIFACTS_PATH,
    BASE_REMOTE_PATH,
    BASE_PUBLISHER_PATH,
    CONTENT_PATH,
    DISTRIBUTION_PATH,
    FILE_CONTENT_PATH,
    FILE_REMOTE_PATH,
    FILE_PUBLISHER_PATH,
    ORPHANS_PATH,
    PUBLICATIONS_PATH,
    REPO_PATH,
    STATUS_PATH,
    USER_PATH,
    WORKER_PATH,
)

from pulp_smash.tests.pulp3.pulpcore.utils import set_up_module as setUpModule  # pylint:disable=unused-import


class OptionHTTPMethodTestCase(unittest.TestCase, utils.SmokeTest):
        """Test whether the OPTION HTTP method is available."""

        def test_all(self):
            """Test whether the OPTION HTTP method is available.

            This test targets the following issue:

            """
            endpoints = (#API_DOCS_PATH,
                        ARTIFACTS_PATH,
                        DISTRIBUTION_PATH,
                        FILE_CONTENT_PATH,
                        FILE_REMOTE_PATH,
                        FILE_PUBLISHER_PATH,
                        ORPHANS_PATH,
                        PUBLICATIONS_PATH,
                        REPO_PATH,
                        STATUS_PATH,
                        USER_PATH,
                        WORKER_PATH,)
            cfg = config.get_config()
            client = api.Client(cfg, api.json_handler)
            for endpoint in endpoints:
                with self.subTest(endpoint=endpoint):
                    response = client.options(endpoint)
                    from pprint import pprint
                    pprint(response)