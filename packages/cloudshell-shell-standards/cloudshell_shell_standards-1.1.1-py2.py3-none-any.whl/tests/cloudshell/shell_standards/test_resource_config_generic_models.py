import sys
import unittest

from cloudshell.shell.standards.attribute_names import (
    DISABLE_SNMP,
    ENABLE_SNMP,
    SNMP_READ_COMMUNITY,
    SNMP_V3_AUTH_PROTOCOL,
    SNMP_V3_PASSWORD,
    SNMP_V3_PRIVACY_PROTOCOL,
    SNMP_V3_PRIVATE_KEY,
    SNMP_V3_USER,
    SNMP_VERSION,
    SNMP_WRITE_COMMUNITY,
)
from cloudshell.shell.standards.resource_config_generic_models import GenericSnmpConfig

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock
else:
    from mock import MagicMock


class TestGenericSnmpConfig(unittest.TestCase):
    def test_snmp_config(self):
        shell_name = "Shell name"
        api = MagicMock(DecryptPassword=lambda password: MagicMock(Value=password))

        attributes = {
            SNMP_READ_COMMUNITY: "community",
            SNMP_WRITE_COMMUNITY: "write community",
            SNMP_V3_USER: "snmp user",
            SNMP_V3_PASSWORD: "snmp password",
            SNMP_V3_PRIVATE_KEY: "snmp private key",
            SNMP_V3_AUTH_PROTOCOL: "snmp auth protocol",
            SNMP_V3_PRIVACY_PROTOCOL: "snmp priv protocol",
            SNMP_VERSION: "v2c",
            ENABLE_SNMP: "True",
            DISABLE_SNMP: "False",
        }
        attributes = {
            "{}.{}".format(shell_name, key): value for key, value in attributes.items()
        }

        config = GenericSnmpConfig(shell_name, attributes=attributes, api=api)
        self.assertEqual("community", config.snmp_read_community)
        self.assertEqual("write community", config.snmp_write_community)
        self.assertEqual("snmp user", config.snmp_v3_user)
        self.assertEqual("snmp password", config.snmp_v3_password)
        self.assertEqual("snmp private key", config.snmp_v3_private_key)
        self.assertEqual("snmp auth protocol", config.snmp_v3_auth_protocol)
        self.assertEqual("snmp priv protocol", config.snmp_v3_priv_protocol)
        self.assertEqual("v2c", config.snmp_version)
        self.assertEqual("True", config.enable_snmp)
        self.assertEqual("False", config.disable_snmp)
