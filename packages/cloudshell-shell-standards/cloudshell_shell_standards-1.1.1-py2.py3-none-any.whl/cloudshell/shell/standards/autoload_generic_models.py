#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import abstractmethod

import cloudshell.shell.standards.attribute_names as attribute_names
from cloudshell.shell.standards.core.autoload.resource_model import (
    AbstractResource,
    ResourceAttribute,
)
from cloudshell.shell.standards.core.autoload.utils import AutoloadDetailsBuilder
from cloudshell.shell.standards.exceptions import ResourceModelException


class GenericResourceModel(AbstractResource):
    _RESOURCE_MODEL = "GenericResource"
    SUPPORTED_FAMILY_NAMES = []

    # Attributes
    contact_name = ResourceAttribute(
        attribute_names.CONTACT_NAME, ResourceAttribute.NAMESPACE.FAMILY_NAME
    )
    system_name = ResourceAttribute(
        attribute_names.SYSTEM_NAME, ResourceAttribute.NAMESPACE.FAMILY_NAME
    )
    location = ResourceAttribute(
        attribute_names.LOCATION, ResourceAttribute.NAMESPACE.FAMILY_NAME
    )
    model = ResourceAttribute(
        attribute_names.MODEL, ResourceAttribute.NAMESPACE.FAMILY_NAME
    )
    model_name = ResourceAttribute(
        attribute_names.MODEL_NAME, ResourceAttribute.NAMESPACE.FAMILY_NAME
    )
    os_version = ResourceAttribute(
        attribute_names.OS_VERSION, ResourceAttribute.NAMESPACE.FAMILY_NAME
    )
    vendor = ResourceAttribute(
        attribute_names.VENDOR, ResourceAttribute.NAMESPACE.FAMILY_NAME
    )

    def __init__(self, resource_name, shell_name, family_name):

        if family_name not in self.SUPPORTED_FAMILY_NAMES:
            raise ResourceModelException(
                "Not supported family name {}. Family name should be one of: {}".format(
                    family_name, ", ".join(self.SUPPORTED_FAMILY_NAMES)
                )
            )
        super(GenericResourceModel, self).__init__(
            None, shell_name, name=resource_name, family_name=family_name
        )

    @property
    @abstractmethod
    def entities(self):
        pass

    def connect_chassis(self, chassis):
        """Connect chassis sub resource.

        :param AbstractResource chassis:
        """
        self._add_sub_resource_with_type_restrictions(chassis, [GenericChassis])

    def connect_port_channel(self, port_channel):
        """Connect port channel sub resource.

        :param AbstractResource port_channel:
        """
        self._add_sub_resource_with_type_restrictions(
            port_channel, [GenericPortChannel]
        )

    def build(self):
        return AutoloadDetailsBuilder(self).build_details()

    @classmethod
    def from_resource_config(cls, resource_config):
        """Initialize from resource config.

        :type resource_config: cloudshell.shell_standards.core.resource_config_entities.GenericResourceConfig  # noqa: E501
        """
        return cls(
            resource_config.name,
            resource_config.shell_name,
            resource_config.family_name,
        )


class GenericChassis(AbstractResource):
    _RELATIVE_ADDRESS_PREFIX = "CH"
    _NAME_TEMPLATE = "Chassis {}"
    _FAMILY_NAME = "CS_Chassis"
    _RESOURCE_MODEL = "GenericChassis"

    # Attributes
    model = ResourceAttribute(
        attribute_names.MODEL, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    serial_number = ResourceAttribute(
        attribute_names.SERIAL_NUMBER, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    model_name = ResourceAttribute(
        attribute_names.MODEL_NAME, ResourceAttribute.NAMESPACE.FAMILY_NAME
    )

    def connect_module(self, module):
        """Connect module sub resource.

        :param AbstractResource module:
        """
        self._add_sub_resource_with_type_restrictions(module, [GenericModule])

    def connect_power_port(self, power_port):
        """Connect power_port sub resource.

        :param AbstractResource power_port:
        """
        self._add_sub_resource_with_type_restrictions(power_port, [GenericPowerPort])

    def connect_port(self, port):
        """Connect port sub resource.

        :param AbstractResource port:
        """
        self._add_sub_resource_with_type_restrictions(port, [GenericPort])


class GenericModule(AbstractResource):
    _RELATIVE_ADDRESS_PREFIX = "M"
    _NAME_TEMPLATE = "Module {}"
    _FAMILY_NAME = "CS_Module"
    _RESOURCE_MODEL = "GenericModule"

    # Attributes
    model = ResourceAttribute(
        attribute_names.MODEL, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    version = ResourceAttribute(
        attribute_names.VERSION, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    serial_number = ResourceAttribute(
        attribute_names.SERIAL_NUMBER, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    model_name = ResourceAttribute(
        attribute_names.MODEL_NAME, ResourceAttribute.NAMESPACE.FAMILY_NAME
    )

    def connect_sub_module(self, sub_module):
        """Connect sub_module sub resource.

        :param AbstractResource sub_module:
        """
        self._add_sub_resource_with_type_restrictions(sub_module, [GenericSubModule])

    def connect_port(self, port):
        """Connect port sub resource.

        :param AbstractResource port:
        """
        self._add_sub_resource_with_type_restrictions(port, [GenericPort])


class GenericSubModule(AbstractResource):
    _RELATIVE_ADDRESS_PREFIX = "SM"
    _NAME_TEMPLATE = "SubModule {}"
    _FAMILY_NAME = "CS_SubModule"
    _RESOURCE_MODEL = "GenericSubModule"

    # Attributes
    model = ResourceAttribute(
        attribute_names.MODEL, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    version = ResourceAttribute(
        attribute_names.VERSION, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    serial_number = ResourceAttribute(
        attribute_names.SERIAL_NUMBER, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    model_name = ResourceAttribute(
        attribute_names.MODEL_NAME, ResourceAttribute.NAMESPACE.FAMILY_NAME
    )

    def connect_port(self, port):
        """Connect port sub resource.

        :param AbstractResource port:
        """
        self._add_sub_resource_with_type_restrictions(port, [BasePort])


class BasePort(AbstractResource):
    _RELATIVE_ADDRESS_PREFIX = "P"
    _NAME_TEMPLATE = "Port {}"
    _FAMILY_NAME = "CS_Port"
    _RESOURCE_MODEL = "GenericPort"

    # Attributes
    model_name = ResourceAttribute(
        attribute_names.MODEL_NAME, ResourceAttribute.NAMESPACE.FAMILY_NAME
    )
    ipv4_address = ResourceAttribute(
        attribute_names.IPV4_ADDRESS, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    ipv6_address = ResourceAttribute(
        attribute_names.IPV6_ADDRESS, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    mac_address = ResourceAttribute(
        attribute_names.MAC_ADDRESS, ResourceAttribute.NAMESPACE.SHELL_NAME
    )


class ResourcePort(BasePort):
    port_speed = ResourceAttribute(
        attribute_names.PORT_SPEED, ResourceAttribute.NAMESPACE.SHELL_NAME, 0
    )


class GenericPort(BasePort):
    # Attributes
    port_description = ResourceAttribute(
        attribute_names.PORT_DESCRIPTION, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    auto_negotiation = ResourceAttribute(
        attribute_names.AUTO_NEGOTIATION, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    bandwidth = ResourceAttribute(
        attribute_names.BANDWIDTH, ResourceAttribute.NAMESPACE.SHELL_NAME, 0
    )
    duplex = ResourceAttribute(
        attribute_names.DUPLEX, ResourceAttribute.NAMESPACE.SHELL_NAME, "Half"
    )
    l2_protocol_type = ResourceAttribute(
        attribute_names.L2_PROTOCOL_TYPE, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    mtu = ResourceAttribute(
        attribute_names.MTU, ResourceAttribute.NAMESPACE.SHELL_NAME, 0
    )
    adjacent = ResourceAttribute(
        attribute_names.ADJACENT, ResourceAttribute.NAMESPACE.SHELL_NAME
    )


class GenericPowerPort(AbstractResource):
    _RESOURCE_MODEL = "GenericPowerPort"
    _RELATIVE_ADDRESS_PREFIX = "PP"
    _NAME_TEMPLATE = "Power Port {}"
    _FAMILY_NAME = "CS_PowerPort"

    # Attributes
    model = ResourceAttribute(
        attribute_names.MODEL, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    model_name = ResourceAttribute(
        attribute_names.MODEL_NAME, ResourceAttribute.NAMESPACE.FAMILY_NAME
    )
    port_description = ResourceAttribute(
        attribute_names.PORT_DESCRIPTION, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    serial_number = ResourceAttribute(
        attribute_names.SERIAL_NUMBER, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    version = ResourceAttribute(
        attribute_names.VERSION, ResourceAttribute.NAMESPACE.SHELL_NAME
    )


class GenericPortChannel(AbstractResource):
    _RESOURCE_MODEL = "GenericPortChannel"
    _RELATIVE_ADDRESS_PREFIX = "PC"
    _NAME_TEMPLATE = "Port Channel{}"
    _FAMILY_NAME = "CS_PortChannel"

    # Attributes
    model_name = ResourceAttribute(
        attribute_names.MODEL_NAME, ResourceAttribute.NAMESPACE.FAMILY_NAME
    )
    associated_ports = ResourceAttribute(
        attribute_names.ASSOCIATED_PORTS, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    ipv4_address = ResourceAttribute(
        attribute_names.IPV4_ADDRESS, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    ipv6_address = ResourceAttribute(
        attribute_names.IPV6_ADDRESS, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
    port_description = ResourceAttribute(
        attribute_names.PORT_DESCRIPTION, ResourceAttribute.NAMESPACE.SHELL_NAME
    )
