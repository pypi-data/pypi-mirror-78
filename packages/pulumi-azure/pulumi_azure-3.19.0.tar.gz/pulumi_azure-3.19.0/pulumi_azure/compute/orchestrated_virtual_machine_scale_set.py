# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = ['OrchestratedVirtualMachineScaleSet']


class OrchestratedVirtualMachineScaleSet(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 platform_fault_domain_count: Optional[pulumi.Input[float]] = None,
                 proximity_placement_group_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 single_placement_group: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 zones: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Manages an Orchestrated Virtual Machine Scale Set.

        > **Note:** Orchestrated Virtual Machine Scale Sets are in Public Preview and it may receive breaking changes - [more details can be found in the Azure Documentation](https://docs.microsoft.com/en-us/azure/virtual-machine-scale-sets/orchestration-modes).

        > **Note:** Azure is planning to deprecate the `single_placement_group` attribute in the Orchestrated Virtual Machine Scale Set starting from api-version `2019-12-01` and there will be a breaking change in the Orchestrated Virtual Machine Scale Set.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_orchestrated_virtual_machine_scale_set = azure.compute.OrchestratedVirtualMachineScaleSet("exampleOrchestratedVirtualMachineScaleSet",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            platform_fault_domain_count=1,
            zones=["1"])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The Azure location where the Orchestrated Virtual Machine Scale Set should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Orchestrated Virtual Machine Scale Set. Changing this forces a new resource to be created.
        :param pulumi.Input[float] platform_fault_domain_count: Specifies the number of fault domains that are used by this Orchestrated Virtual Machine Scale Set. Changing this forces a new resource to be created.
        :param pulumi.Input[str] proximity_placement_group_id: The ID of the Proximity Placement Group which the Virtual Machine should be assigned to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the Orchestrated Virtual Machine Scale Set should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] single_placement_group: Should the Orchestrated Virtual Machine Scale Set use single placement group? Defaults to `false`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to this Orchestrated Virtual Machine Scale Set.
        :param pulumi.Input[str] zones: A list of Availability Zones in which the Virtual Machines in this Scale Set should be created in. Changing this forces a new resource to be created.
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

            __props__['location'] = location
            __props__['name'] = name
            if platform_fault_domain_count is None:
                raise TypeError("Missing required property 'platform_fault_domain_count'")
            __props__['platform_fault_domain_count'] = platform_fault_domain_count
            __props__['proximity_placement_group_id'] = proximity_placement_group_id
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['single_placement_group'] = single_placement_group
            __props__['tags'] = tags
            __props__['zones'] = zones
            __props__['unique_id'] = None
        super(OrchestratedVirtualMachineScaleSet, __self__).__init__(
            'azure:compute/orchestratedVirtualMachineScaleSet:OrchestratedVirtualMachineScaleSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            platform_fault_domain_count: Optional[pulumi.Input[float]] = None,
            proximity_placement_group_id: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            single_placement_group: Optional[pulumi.Input[bool]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            unique_id: Optional[pulumi.Input[str]] = None,
            zones: Optional[pulumi.Input[str]] = None) -> 'OrchestratedVirtualMachineScaleSet':
        """
        Get an existing OrchestratedVirtualMachineScaleSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The Azure location where the Orchestrated Virtual Machine Scale Set should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Orchestrated Virtual Machine Scale Set. Changing this forces a new resource to be created.
        :param pulumi.Input[float] platform_fault_domain_count: Specifies the number of fault domains that are used by this Orchestrated Virtual Machine Scale Set. Changing this forces a new resource to be created.
        :param pulumi.Input[str] proximity_placement_group_id: The ID of the Proximity Placement Group which the Virtual Machine should be assigned to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the Orchestrated Virtual Machine Scale Set should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] single_placement_group: Should the Orchestrated Virtual Machine Scale Set use single placement group? Defaults to `false`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to this Orchestrated Virtual Machine Scale Set.
        :param pulumi.Input[str] unique_id: The Unique ID for the Orchestrated Virtual Machine Scale Set.
        :param pulumi.Input[str] zones: A list of Availability Zones in which the Virtual Machines in this Scale Set should be created in. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["location"] = location
        __props__["name"] = name
        __props__["platform_fault_domain_count"] = platform_fault_domain_count
        __props__["proximity_placement_group_id"] = proximity_placement_group_id
        __props__["resource_group_name"] = resource_group_name
        __props__["single_placement_group"] = single_placement_group
        __props__["tags"] = tags
        __props__["unique_id"] = unique_id
        __props__["zones"] = zones
        return OrchestratedVirtualMachineScaleSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The Azure location where the Orchestrated Virtual Machine Scale Set should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the Orchestrated Virtual Machine Scale Set. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="platformFaultDomainCount")
    def platform_fault_domain_count(self) -> pulumi.Output[float]:
        """
        Specifies the number of fault domains that are used by this Orchestrated Virtual Machine Scale Set. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "platform_fault_domain_count")

    @property
    @pulumi.getter(name="proximityPlacementGroupId")
    def proximity_placement_group_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the Proximity Placement Group which the Virtual Machine should be assigned to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "proximity_placement_group_id")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group in which the Orchestrated Virtual Machine Scale Set should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="singlePlacementGroup")
    def single_placement_group(self) -> pulumi.Output[Optional[bool]]:
        """
        Should the Orchestrated Virtual Machine Scale Set use single placement group? Defaults to `false`.
        """
        return pulumi.get(self, "single_placement_group")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags which should be assigned to this Orchestrated Virtual Machine Scale Set.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="uniqueId")
    def unique_id(self) -> pulumi.Output[str]:
        """
        The Unique ID for the Orchestrated Virtual Machine Scale Set.
        """
        return pulumi.get(self, "unique_id")

    @property
    @pulumi.getter
    def zones(self) -> pulumi.Output[Optional[str]]:
        """
        A list of Availability Zones in which the Virtual Machines in this Scale Set should be created in. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "zones")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

