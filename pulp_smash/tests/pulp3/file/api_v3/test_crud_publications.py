# coding=utf-8
"""Tests that CRUD publications."""
import unittest

from requests.exceptions import HTTPError

from pulp_smash import api, config, exceptions
from pulp_smash.tests.pulp3.constants import(
    BASE_PUBLICATION_PATH,
    FILE_PUBLISHER_PATH,
    REPO_PATH,
)
from pulp_smash.tests.pulp3.file.api_v3.utils import gen_publisher
from pulp_smash.tests.pulp3.file.utils import set_up_module as setUpModule  # noqa pylint:disable=unused-import
from pulp_smash.tests.pulp3.pulpcore.utils import gen_repo
from pulp_smash.tests.pulp3.utils import get_auth


class CRUDPublicationsTestCase(unittest.TestCase):
    """CRUD publishers."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables.

        In order to create a publisher a repository has to be created first.
        """
        cls.cfg = config.get_config()
        cls.client = api.Client(cls.cfg, api.json_handler)
        cls.client.request_kwargs['auth'] = get_auth()
        cls.repo = cls.client.post(REPO_PATH, gen_repo())
        cls.publisher = cls.client.post(
            FILE_PUBLISHER_PATH,
            gen_publisher(cls.repo)
        )
        from pprint import pprint
        pprint(cls.repo)
        pprint(cls.publisher['_href'])
        cls.publication = {}

    # @classmethod
    # def tearDownClass(cls):
    #     """Clean class-wide variables."""
    #     cls.client.delete(cls.repo['_href'])
    #     cls.client.delete(cls.publisher['_href'])

    def test_01_create_publication(self):
        """Create a publication."""
        # from pprint import pprint
        # pprint(self.publisher)
        with self.assertRaises(exceptions.TaskReportError) as context:
            type(self).publication = self.client.post(
                BASE_PUBLICATION_PATH,
                {'publisher': self.publisher['_href']}
            )
        task = context.exception.task
        from pprint import pprint
        pprint(task)

    # @selectors.skip_if(bool, 'publication', False)
    # def test_02_read_publisher(self):
    #     """Read a publisher by its href."""
    #     pass
    #
    # @selectors.skip_if(bool, 'publication', False)
    # def test_02_read_publishers(self):
    #     """Read a publisher by its name."""
    #     pass
    #
    # @selectors.skip_if(bool, 'publication', False)
    # def test_03_partially_update(self):
    #     """Update a publisher using HTTP PATCH."""
    #     pass
    #
    # @selectors.skip_if(bool, 'publication', False)
    # def test_04_fully_update(self):
    #     """Update a publisher using HTTP PUT."""
    #     pass
    #
    # @selectors.skip_if(bool, 'publication', False)
    # def test_05_delete(self):
    #     """Delete a publisher."""
    #     pass
