# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = ['Assignment']


class Assignment(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 role_definition_id: Optional[pulumi.Input[str]] = None,
                 role_definition_name: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 skip_service_principal_aad_check: Optional[pulumi.Input[bool]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Assigns a given Principal (User or Group) to a given Role.

        ## Example Usage
        ### Using A Built-In Role)

        ```python
        import pulumi
        import pulumi_azure as azure

        primary = azure.core.get_subscription()
        example_client_config = azure.core.get_client_config()
        example_assignment = azure.authorization.Assignment("exampleAssignment",
            scope=primary.id,
            role_definition_name="Reader",
            principal_id=example_client_config.object_id)
        ```
        ### Custom Role & Service Principal)

        ```python
        import pulumi
        import pulumi_azure as azure

        primary = azure.core.get_subscription()
        example_client_config = azure.core.get_client_config()
        example_role_definition = azure.authorization.RoleDefinition("exampleRoleDefinition",
            role_definition_id="00000000-0000-0000-0000-000000000000",
            scope=primary.id,
            permissions=[azure.authorization.RoleDefinitionPermissionArgs(
                actions=["Microsoft.Resources/subscriptions/resourceGroups/read"],
                not_actions=[],
            )],
            assignable_scopes=[primary.id])
        example_assignment = azure.authorization.Assignment("exampleAssignment",
            name="00000000-0000-0000-0000-000000000000",
            scope=primary.id,
            role_definition_id=example_role_definition.id,
            principal_id=example_client_config.object_id)
        ```
        ### Custom Role & User)

        ```python
        import pulumi
        import pulumi_azure as azure

        primary = azure.core.get_subscription()
        example_client_config = azure.core.get_client_config()
        example_role_definition = azure.authorization.RoleDefinition("exampleRoleDefinition",
            role_definition_id="00000000-0000-0000-0000-000000000000",
            scope=primary.id,
            permissions=[azure.authorization.RoleDefinitionPermissionArgs(
                actions=["Microsoft.Resources/subscriptions/resourceGroups/read"],
                not_actions=[],
            )],
            assignable_scopes=[primary.id])
        example_assignment = azure.authorization.Assignment("exampleAssignment",
            name="00000000-0000-0000-0000-000000000000",
            scope=primary.id,
            role_definition_id=example_role_definition.id,
            principal_id=example_client_config.client_id)
        ```
        ### Custom Role & Management Group)

        ```python
        import pulumi
        import pulumi_azure as azure

        primary = azure.core.get_subscription()
        example_client_config = azure.core.get_client_config()
        example_group = azure.management.get_group()
        example_role_definition = azure.authorization.RoleDefinition("exampleRoleDefinition",
            role_definition_id="00000000-0000-0000-0000-000000000000",
            scope=primary.id,
            permissions=[azure.authorization.RoleDefinitionPermissionArgs(
                actions=["Microsoft.Resources/subscriptions/resourceGroups/read"],
                not_actions=[],
            )],
            assignable_scopes=[primary.id])
        example_assignment = azure.authorization.Assignment("exampleAssignment",
            name="00000000-0000-0000-0000-000000000000",
            scope=data["azurerm_management_group"]["primary"]["id"],
            role_definition_id=example_role_definition.id,
            principal_id=example_client_config.client_id)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: A unique UUID/GUID for this Role Assignment - one will be generated if not specified. Changing this forces a new resource to be created.
        :param pulumi.Input[str] principal_id: The ID of the Principal (User, Group or Service Principal) to assign the Role Definition to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] role_definition_id: The Scoped-ID of the Role Definition. Changing this forces a new resource to be created. Conflicts with `role_definition_name`.
        :param pulumi.Input[str] role_definition_name: The name of a built-in Role. Changing this forces a new resource to be created. Conflicts with `role_definition_id`.
        :param pulumi.Input[str] scope: The scope at which the Role Assignment applies to, such as `/subscriptions/0b1f6471-1bf0-4dda-aec3-111122223333`, `/subscriptions/0b1f6471-1bf0-4dda-aec3-111122223333/resourceGroups/myGroup`, or `/subscriptions/0b1f6471-1bf0-4dda-aec3-111122223333/resourceGroups/myGroup/providers/Microsoft.Compute/virtualMachines/myVM`, or `/providers/Microsoft.Management/managementGroups/myMG`. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] skip_service_principal_aad_check: If the `principal_id` is a newly provisioned `Service Principal` set this value to `true` to skip the `Azure Active Directory` check which may fail due to replication lag. This argument is only valid if the `principal_id` is a `Service Principal` identity. If it is not a `Service Principal` identity it will cause the role assignment to fail. Defaults to `false`.
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

            __props__['name'] = name
            if principal_id is None:
                raise TypeError("Missing required property 'principal_id'")
            __props__['principal_id'] = principal_id
            __props__['role_definition_id'] = role_definition_id
            __props__['role_definition_name'] = role_definition_name
            if scope is None:
                raise TypeError("Missing required property 'scope'")
            __props__['scope'] = scope
            __props__['skip_service_principal_aad_check'] = skip_service_principal_aad_check
            __props__['principal_type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure:role/assignment:Assignment")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Assignment, __self__).__init__(
            'azure:authorization/assignment:Assignment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            principal_id: Optional[pulumi.Input[str]] = None,
            principal_type: Optional[pulumi.Input[str]] = None,
            role_definition_id: Optional[pulumi.Input[str]] = None,
            role_definition_name: Optional[pulumi.Input[str]] = None,
            scope: Optional[pulumi.Input[str]] = None,
            skip_service_principal_aad_check: Optional[pulumi.Input[bool]] = None) -> 'Assignment':
        """
        Get an existing Assignment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: A unique UUID/GUID for this Role Assignment - one will be generated if not specified. Changing this forces a new resource to be created.
        :param pulumi.Input[str] principal_id: The ID of the Principal (User, Group or Service Principal) to assign the Role Definition to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] principal_type: The type of the `principal_id`, e.g. User, Group, Service Principal, Application, etc.
        :param pulumi.Input[str] role_definition_id: The Scoped-ID of the Role Definition. Changing this forces a new resource to be created. Conflicts with `role_definition_name`.
        :param pulumi.Input[str] role_definition_name: The name of a built-in Role. Changing this forces a new resource to be created. Conflicts with `role_definition_id`.
        :param pulumi.Input[str] scope: The scope at which the Role Assignment applies to, such as `/subscriptions/0b1f6471-1bf0-4dda-aec3-111122223333`, `/subscriptions/0b1f6471-1bf0-4dda-aec3-111122223333/resourceGroups/myGroup`, or `/subscriptions/0b1f6471-1bf0-4dda-aec3-111122223333/resourceGroups/myGroup/providers/Microsoft.Compute/virtualMachines/myVM`, or `/providers/Microsoft.Management/managementGroups/myMG`. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] skip_service_principal_aad_check: If the `principal_id` is a newly provisioned `Service Principal` set this value to `true` to skip the `Azure Active Directory` check which may fail due to replication lag. This argument is only valid if the `principal_id` is a `Service Principal` identity. If it is not a `Service Principal` identity it will cause the role assignment to fail. Defaults to `false`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["name"] = name
        __props__["principal_id"] = principal_id
        __props__["principal_type"] = principal_type
        __props__["role_definition_id"] = role_definition_id
        __props__["role_definition_name"] = role_definition_name
        __props__["scope"] = scope
        __props__["skip_service_principal_aad_check"] = skip_service_principal_aad_check
        return Assignment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A unique UUID/GUID for this Role Assignment - one will be generated if not specified. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> pulumi.Output[str]:
        """
        The ID of the Principal (User, Group or Service Principal) to assign the Role Definition to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="principalType")
    def principal_type(self) -> pulumi.Output[str]:
        """
        The type of the `principal_id`, e.g. User, Group, Service Principal, Application, etc.
        """
        return pulumi.get(self, "principal_type")

    @property
    @pulumi.getter(name="roleDefinitionId")
    def role_definition_id(self) -> pulumi.Output[str]:
        """
        The Scoped-ID of the Role Definition. Changing this forces a new resource to be created. Conflicts with `role_definition_name`.
        """
        return pulumi.get(self, "role_definition_id")

    @property
    @pulumi.getter(name="roleDefinitionName")
    def role_definition_name(self) -> pulumi.Output[str]:
        """
        The name of a built-in Role. Changing this forces a new resource to be created. Conflicts with `role_definition_id`.
        """
        return pulumi.get(self, "role_definition_name")

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Output[str]:
        """
        The scope at which the Role Assignment applies to, such as `/subscriptions/0b1f6471-1bf0-4dda-aec3-111122223333`, `/subscriptions/0b1f6471-1bf0-4dda-aec3-111122223333/resourceGroups/myGroup`, or `/subscriptions/0b1f6471-1bf0-4dda-aec3-111122223333/resourceGroups/myGroup/providers/Microsoft.Compute/virtualMachines/myVM`, or `/providers/Microsoft.Management/managementGroups/myMG`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter(name="skipServicePrincipalAadCheck")
    def skip_service_principal_aad_check(self) -> pulumi.Output[bool]:
        """
        If the `principal_id` is a newly provisioned `Service Principal` set this value to `true` to skip the `Azure Active Directory` check which may fail due to replication lag. This argument is only valid if the `principal_id` is a `Service Principal` identity. If it is not a `Service Principal` identity it will cause the role assignment to fail. Defaults to `false`.
        """
        return pulumi.get(self, "skip_service_principal_aad_check")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

