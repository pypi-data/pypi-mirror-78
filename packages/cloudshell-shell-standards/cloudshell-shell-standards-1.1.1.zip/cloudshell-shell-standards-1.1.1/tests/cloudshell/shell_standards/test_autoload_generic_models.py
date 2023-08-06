import unittest

from cloudshell.shell.standards.autoload_generic_models import (
    GenericResourceModel,
    ResourcePort,
)


class TestGenericResourceModel(unittest.TestCase):
    def setUp(self):
        class ResourceModel(GenericResourceModel):
            SUPPORTED_FAMILY_NAMES = ["Family Name"]

            @property
            def entities(self):
                class _ResourceEntities:
                    Port = ResourcePort

                return _ResourceEntities

        self.resource_model_class = ResourceModel

    def test_resource_model(self):
        resource_name = "resource name"
        shell_name = "shell name"
        family_name = "Family Name"

        resource = self.resource_model_class(resource_name, shell_name, family_name)

        self.assertEqual(family_name, resource.family_name)
        self.assertEqual(shell_name, resource.shell_name)
        self.assertEqual(resource_name, resource.name)
        self.assertEqual("", resource.relative_address.__repr__())
        self.assertEqual("GenericResource", resource.resource_model)
        self.assertEqual(
            "{}.{}".format(shell_name, resource.resource_model),
            resource.cloudshell_model_name,
        )
        self.assertEqual(ResourcePort, resource.entities.Port)
        self.assertIsInstance(resource.unique_identifier, str)
        self.assertTrue(resource.unique_identifier)

    def test_resource_build(self):
        resource_name = "resource name"
        shell_name = "shell name"
        family_name = "Family Name"
        contact_name = "contact name"
        system_name = "system name"
        location = "location"
        model = "model"
        model_name = "model name"
        os_version = "os version"
        vendor = "vendor"

        resource = self.resource_model_class(resource_name, shell_name, family_name)

        resource.contact_name = contact_name
        resource.system_name = system_name
        resource.location = location
        resource.model = model
        resource.model_name = model_name
        resource.os_version = os_version
        resource.vendor = vendor

        autoload_detail = resource.build()
        resource_attributes = {
            attr.attribute_name: attr.attribute_value
            for attr in autoload_detail.attributes
        }
        expected_attributes = {
            "Contact Name": contact_name,
            "Location": location,
            "Model": model,
            "Model Name": model_name,
            "OS Version": os_version,
            "System Name": system_name,
            "Vendor": vendor,
        }
        expected_attributes = {
            "{}.{}".format(family_name, k): v for k, v in expected_attributes.items()
        }

        self.assertDictEqual(expected_attributes, resource_attributes)
