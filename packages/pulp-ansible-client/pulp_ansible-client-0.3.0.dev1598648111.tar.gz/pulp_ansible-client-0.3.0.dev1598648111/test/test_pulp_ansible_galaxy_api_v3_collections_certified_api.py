# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import pulpcore.client.pulp_ansible
from pulpcore.client.pulp_ansible.api.pulp_ansible_galaxy_api_v3_collections_certified_api import PulpAnsibleGalaxyApiV3CollectionsCertifiedApi  # noqa: E501
from pulpcore.client.pulp_ansible.rest import ApiException


class TestPulpAnsibleGalaxyApiV3CollectionsCertifiedApi(unittest.TestCase):
    """PulpAnsibleGalaxyApiV3CollectionsCertifiedApi unit test stubs"""

    def setUp(self):
        self.api = pulpcore.client.pulp_ansible.api.pulp_ansible_galaxy_api_v3_collections_certified_api.PulpAnsibleGalaxyApiV3CollectionsCertifiedApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_set_certified(self):
        """Test case for set_certified

        """
        pass


if __name__ == '__main__':
    unittest.main()
