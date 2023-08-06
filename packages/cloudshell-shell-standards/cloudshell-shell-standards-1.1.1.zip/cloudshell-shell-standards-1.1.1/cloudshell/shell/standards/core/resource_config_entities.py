#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from cloudshell.shell.standards.exceptions import ResourceConfigException

if sys.version_info >= (3, 0):
    from functools import lru_cache
else:
    from functools32 import lru_cache


class ResourceAttrRO(object):
    class NAMESPACE(object):
        SHELL_NAME = "shell_name"
        FAMILY_NAME = "family_name"

    def __init__(self, name, namespace, default=None):
        """Resource Attribute read-only.

        :param str name:
        :param str namespace:
        :param str default:
        """
        self.name = name
        self.namespace = namespace
        self.default = default

    def get_key(self, instance):
        """Get key.

        :param GenericResourceConfig instance:
        :rtype: str
        """
        return "{}.{}".format(getattr(instance, self.namespace), self.name)

    def __get__(self, instance, owner):
        """Getter.

        :param GenericResourceConfig instance:
        :rtype: str
        """
        if instance is None:
            return self

        return instance.attributes.get(self.get_key(instance), self.default)


class PasswordAttrRO(ResourceAttrRO):
    @lru_cache()
    def _decrypt_password(self, api, attr_value):
        """Decrypt password.

        :param cloudshell.api.cloudshell_api.CloudShellAPISession api:
        :param str attr_value:
        :return:
        """
        if api:
            return api.DecryptPassword(attr_value).Value
        raise ResourceConfigException("Cannot decrypt password, API is not defined")

    def __get__(self, instance, owner):
        """Getter.

        :param GenericResourceConfig instance:
        :rtype: str
        """
        val = super(PasswordAttrRO, self).__get__(instance, owner)
        if val is self or val is self.default:
            return val
        return self._decrypt_password(instance.api, val)


class ResourceListAttrRO(ResourceAttrRO):
    def __init__(self, name, namespace, sep=";", default=None):
        if default is None:
            default = []
        super(ResourceListAttrRO, self).__init__(name, namespace, default)
        self._sep = sep

    def __get__(self, instance, owner):
        """Getter.

        :param GenericResourceConfig instance:
        :rtype: list[str]
        """
        val = super(ResourceListAttrRO, self).__get__(instance, owner)
        if val is self or val is self.default or not isinstance(val, str):
            return val
        return list(filter(bool, map(str.strip, val.split(self._sep))))


class ResourceBoolAttrRO(ResourceAttrRO):
    TRUE_VALUES = {"true", "yes", "y"}
    FALSE_VALUES = {"false", "no", "n"}

    def __init__(self, name, namespace, default=False):
        super(ResourceBoolAttrRO, self).__init__(name, namespace, default)

    def __get__(self, instance, owner):
        """Getter.

        :param GenericResourceConfig instance:
        :rtype: bool
        """
        val = super(ResourceBoolAttrRO, self).__get__(instance, owner)
        if val is self or val is self.default or not isinstance(val, str):
            return val
        if val.lower() in self.TRUE_VALUES:
            return True
        if val.lower() in self.FALSE_VALUES:
            return False
        raise ValueError("{} is boolean attr, but value is {}".format(self.name, val))


class GenericResourceConfig(object):
    def __init__(
        self,
        shell_name=None,
        name=None,
        fullname=None,
        address=None,
        family_name=None,
        attributes=None,
        supported_os=None,
        api=None,
    ):
        """Init method.

        :param str shell_name: Shell Name
        :param str name: Resource Name
        :param list supported_os: list of supported OS
        """
        self.attributes = attributes or {}
        self.shell_name = shell_name
        self.name = name
        self.supported_os = supported_os or []
        self.fullname = fullname
        self.address = address  # The IP address of the resource
        self.family_name = family_name  # The resource family
        self.namespace_prefix = "{}".format(self.shell_name)
        self.api = api

        if not shell_name:
            raise DeprecationWarning("1gen Shells doesn't supported")

    @classmethod
    def from_context(cls, shell_name, context, api=None, supported_os=None):
        """Creates an instance of a Resource by given context.

        :param str shell_name: Shell Name
        :param list supported_os: list of supported OS
        :param cloudshell.shell.core.driver_context.ResourceCommandContext context:
        :param cloudshell.api.cloudshell_api.CloudShellAPISession api:
        :rtype: GenericResourceConfig
        """
        return cls(
            shell_name=shell_name,
            name=context.resource.name,
            fullname=context.resource.fullname,
            address=context.resource.address,
            family_name=context.resource.family,
            attributes=dict(context.resource.attributes),
            supported_os=supported_os,
            api=api,
        )
