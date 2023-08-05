# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'DefinitionPermission',
    'GetRoleDefinitionPermissionResult',
]

@pulumi.output_type
class DefinitionPermission(dict):
    def __init__(__self__, *,
                 actions: Optional[List[str]] = None,
                 data_actions: Optional[List[str]] = None,
                 not_actions: Optional[List[str]] = None,
                 not_data_actions: Optional[List[str]] = None):
        """
        :param List[str] actions: One or more Allowed Actions, such as `*`, `Microsoft.Resources/subscriptions/resourceGroups/read`. See ['Azure Resource Manager resource provider operations'](https://docs.microsoft.com/en-us/azure/role-based-access-control/resource-provider-operations) for details.
        :param List[str] data_actions: One or more Allowed Data Actions, such as `*`, `Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read`. See ['Azure Resource Manager resource provider operations'](https://docs.microsoft.com/en-us/azure/role-based-access-control/resource-provider-operations) for details.
        :param List[str] not_actions: One or more Disallowed Actions, such as `*`, `Microsoft.Resources/subscriptions/resourceGroups/read`. See ['Azure Resource Manager resource provider operations'](https://docs.microsoft.com/en-us/azure/role-based-access-control/resource-provider-operations) for details.
        :param List[str] not_data_actions: One or more Disallowed Data Actions, such as `*`, `Microsoft.Resources/subscriptions/resourceGroups/read`. See ['Azure Resource Manager resource provider operations'](https://docs.microsoft.com/en-us/azure/role-based-access-control/resource-provider-operations) for details.
        """
        if actions is not None:
            pulumi.set(__self__, "actions", actions)
        if data_actions is not None:
            pulumi.set(__self__, "data_actions", data_actions)
        if not_actions is not None:
            pulumi.set(__self__, "not_actions", not_actions)
        if not_data_actions is not None:
            pulumi.set(__self__, "not_data_actions", not_data_actions)

    @property
    @pulumi.getter
    def actions(self) -> Optional[List[str]]:
        """
        One or more Allowed Actions, such as `*`, `Microsoft.Resources/subscriptions/resourceGroups/read`. See ['Azure Resource Manager resource provider operations'](https://docs.microsoft.com/en-us/azure/role-based-access-control/resource-provider-operations) for details.
        """
        return pulumi.get(self, "actions")

    @property
    @pulumi.getter(name="dataActions")
    def data_actions(self) -> Optional[List[str]]:
        """
        One or more Allowed Data Actions, such as `*`, `Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read`. See ['Azure Resource Manager resource provider operations'](https://docs.microsoft.com/en-us/azure/role-based-access-control/resource-provider-operations) for details.
        """
        return pulumi.get(self, "data_actions")

    @property
    @pulumi.getter(name="notActions")
    def not_actions(self) -> Optional[List[str]]:
        """
        One or more Disallowed Actions, such as `*`, `Microsoft.Resources/subscriptions/resourceGroups/read`. See ['Azure Resource Manager resource provider operations'](https://docs.microsoft.com/en-us/azure/role-based-access-control/resource-provider-operations) for details.
        """
        return pulumi.get(self, "not_actions")

    @property
    @pulumi.getter(name="notDataActions")
    def not_data_actions(self) -> Optional[List[str]]:
        """
        One or more Disallowed Data Actions, such as `*`, `Microsoft.Resources/subscriptions/resourceGroups/read`. See ['Azure Resource Manager resource provider operations'](https://docs.microsoft.com/en-us/azure/role-based-access-control/resource-provider-operations) for details.
        """
        return pulumi.get(self, "not_data_actions")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class GetRoleDefinitionPermissionResult(dict):
    def __init__(__self__, *,
                 actions: List[str],
                 not_actions: List[str],
                 data_actions: Optional[List[str]] = None,
                 not_data_actions: Optional[List[str]] = None):
        pulumi.set(__self__, "actions", actions)
        pulumi.set(__self__, "not_actions", not_actions)
        if data_actions is not None:
            pulumi.set(__self__, "data_actions", data_actions)
        if not_data_actions is not None:
            pulumi.set(__self__, "not_data_actions", not_data_actions)

    @property
    @pulumi.getter
    def actions(self) -> List[str]:
        return pulumi.get(self, "actions")

    @property
    @pulumi.getter(name="notActions")
    def not_actions(self) -> List[str]:
        return pulumi.get(self, "not_actions")

    @property
    @pulumi.getter(name="dataActions")
    def data_actions(self) -> Optional[List[str]]:
        return pulumi.get(self, "data_actions")

    @property
    @pulumi.getter(name="notDataActions")
    def not_data_actions(self) -> Optional[List[str]]:
        return pulumi.get(self, "not_data_actions")


