# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['Assignment']


class Assignment(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['AssignmentIdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 lock_exclude_principals: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 lock_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parameter_values: Optional[pulumi.Input[str]] = None,
                 resource_groups: Optional[pulumi.Input[str]] = None,
                 target_subscription_id: Optional[pulumi.Input[str]] = None,
                 version_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Create a Assignment resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The Azure location of the Assignment.
        :param pulumi.Input[List[pulumi.Input[str]]] lock_exclude_principals: a list of up to 5 Principal IDs that are permitted to bypass the locks applied by the Blueprint.
        :param pulumi.Input[str] lock_mode: The locking mode of the Blueprint Assignment.  One of `None` (Default), `AllResourcesReadOnly`, or `AlResourcesDoNotDelete`.
        :param pulumi.Input[str] name: The name of the Blueprint Assignment
        :param pulumi.Input[str] parameter_values: a JSON string to supply Blueprint Assignment parameter values.
        :param pulumi.Input[str] resource_groups: a JSON string to supply the Blueprint Resource Group information.
        :param pulumi.Input[str] target_subscription_id: The Subscription ID the Blueprint Published Version is to be applied to.
        :param pulumi.Input[str] version_id: The ID of the Published Version of the blueprint to be assigned.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['identity'] = identity
            __props__['location'] = location
            __props__['lock_exclude_principals'] = lock_exclude_principals
            __props__['lock_mode'] = lock_mode
            __props__['name'] = name
            __props__['parameter_values'] = parameter_values
            __props__['resource_groups'] = resource_groups
            if target_subscription_id is None:
                raise TypeError("Missing required property 'target_subscription_id'")
            __props__['target_subscription_id'] = target_subscription_id
            if version_id is None:
                raise TypeError("Missing required property 'version_id'")
            __props__['version_id'] = version_id
            __props__['blueprint_name'] = None
            __props__['description'] = None
            __props__['display_name'] = None
            __props__['type'] = None
        super(Assignment, __self__).__init__(
            'azure:blueprint/assignment:Assignment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            blueprint_name: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            identity: Optional[pulumi.Input[pulumi.InputType['AssignmentIdentityArgs']]] = None,
            location: Optional[pulumi.Input[str]] = None,
            lock_exclude_principals: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            lock_mode: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            parameter_values: Optional[pulumi.Input[str]] = None,
            resource_groups: Optional[pulumi.Input[str]] = None,
            target_subscription_id: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None,
            version_id: Optional[pulumi.Input[str]] = None) -> 'Assignment':
        """
        Get an existing Assignment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] blueprint_name: The name of the blueprint assigned
        :param pulumi.Input[str] description: The Description on the Blueprint
        :param pulumi.Input[str] display_name: The display name of the blueprint
        :param pulumi.Input[str] location: The Azure location of the Assignment.
        :param pulumi.Input[List[pulumi.Input[str]]] lock_exclude_principals: a list of up to 5 Principal IDs that are permitted to bypass the locks applied by the Blueprint.
        :param pulumi.Input[str] lock_mode: The locking mode of the Blueprint Assignment.  One of `None` (Default), `AllResourcesReadOnly`, or `AlResourcesDoNotDelete`.
        :param pulumi.Input[str] name: The name of the Blueprint Assignment
        :param pulumi.Input[str] parameter_values: a JSON string to supply Blueprint Assignment parameter values.
        :param pulumi.Input[str] resource_groups: a JSON string to supply the Blueprint Resource Group information.
        :param pulumi.Input[str] target_subscription_id: The Subscription ID the Blueprint Published Version is to be applied to.
        :param pulumi.Input[str] type: The Identity type for the Managed Service Identity. Currently only `UserAssigned` is supported.
        :param pulumi.Input[str] version_id: The ID of the Published Version of the blueprint to be assigned.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["blueprint_name"] = blueprint_name
        __props__["description"] = description
        __props__["display_name"] = display_name
        __props__["identity"] = identity
        __props__["location"] = location
        __props__["lock_exclude_principals"] = lock_exclude_principals
        __props__["lock_mode"] = lock_mode
        __props__["name"] = name
        __props__["parameter_values"] = parameter_values
        __props__["resource_groups"] = resource_groups
        __props__["target_subscription_id"] = target_subscription_id
        __props__["type"] = type
        __props__["version_id"] = version_id
        return Assignment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="blueprintName")
    def blueprint_name(self) -> pulumi.Output[str]:
        """
        The name of the blueprint assigned
        """
        return pulumi.get(self, "blueprint_name")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        The Description on the Blueprint
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        The display name of the blueprint
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.AssignmentIdentity']]:
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The Azure location of the Assignment.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="lockExcludePrincipals")
    def lock_exclude_principals(self) -> pulumi.Output[Optional[List[str]]]:
        """
        a list of up to 5 Principal IDs that are permitted to bypass the locks applied by the Blueprint.
        """
        return pulumi.get(self, "lock_exclude_principals")

    @property
    @pulumi.getter(name="lockMode")
    def lock_mode(self) -> pulumi.Output[Optional[str]]:
        """
        The locking mode of the Blueprint Assignment.  One of `None` (Default), `AllResourcesReadOnly`, or `AlResourcesDoNotDelete`.
        """
        return pulumi.get(self, "lock_mode")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the Blueprint Assignment
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="parameterValues")
    def parameter_values(self) -> pulumi.Output[Optional[str]]:
        """
        a JSON string to supply Blueprint Assignment parameter values.
        """
        return pulumi.get(self, "parameter_values")

    @property
    @pulumi.getter(name="resourceGroups")
    def resource_groups(self) -> pulumi.Output[Optional[str]]:
        """
        a JSON string to supply the Blueprint Resource Group information.
        """
        return pulumi.get(self, "resource_groups")

    @property
    @pulumi.getter(name="targetSubscriptionId")
    def target_subscription_id(self) -> pulumi.Output[str]:
        """
        The Subscription ID the Blueprint Published Version is to be applied to.
        """
        return pulumi.get(self, "target_subscription_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The Identity type for the Managed Service Identity. Currently only `UserAssigned` is supported.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="versionId")
    def version_id(self) -> pulumi.Output[str]:
        """
        The ID of the Published Version of the blueprint to be assigned.
        """
        return pulumi.get(self, "version_id")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

