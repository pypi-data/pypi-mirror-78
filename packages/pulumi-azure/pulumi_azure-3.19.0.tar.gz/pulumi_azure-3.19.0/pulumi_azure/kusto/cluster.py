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

__all__ = ['Cluster']


class Cluster(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enable_disk_encryption: Optional[pulumi.Input[bool]] = None,
                 enable_purge: Optional[pulumi.Input[bool]] = None,
                 enable_streaming_ingest: Optional[pulumi.Input[bool]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ClusterIdentityArgs']]] = None,
                 language_extensions: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 optimized_auto_scale: Optional[pulumi.Input[pulumi.InputType['ClusterOptimizedAutoScaleArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['ClusterSkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 trusted_external_tenants: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 virtual_network_configuration: Optional[pulumi.Input[pulumi.InputType['ClusterVirtualNetworkConfigurationArgs']]] = None,
                 zones: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Manages a Kusto (also known as Azure Data Explorer) Cluster

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        rg = azure.core.ResourceGroup("rg", location="East US")
        example = azure.kusto.Cluster("example",
            location=rg.location,
            resource_group_name=rg.name,
            sku=azure.kusto.ClusterSkuArgs(
                name="Standard_D13_v2",
                capacity=2,
            ),
            tags={
                "Environment": "Production",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enable_disk_encryption: Specifies if the cluster's disks are encrypted.
        :param pulumi.Input[bool] enable_purge: Specifies if the purge operations are enabled.
        :param pulumi.Input[bool] enable_streaming_ingest: Specifies if the streaming ingest is enabled.
        :param pulumi.Input[pulumi.InputType['ClusterIdentityArgs']] identity: A identity block.
        :param pulumi.Input[List[pulumi.Input[str]]] language_extensions: An list of `language_extensions` to enable. Valid values are: `PYTHON` and `R`.
        :param pulumi.Input[str] location: The location where the Kusto Cluster should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Kusto Cluster to create. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['ClusterOptimizedAutoScaleArgs']] optimized_auto_scale: An `optimized_auto_scale` block as defined below.
        :param pulumi.Input[str] resource_group_name: Specifies the Resource Group where the Kusto Cluster should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['ClusterSkuArgs']] sku: A `sku` block as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[List[pulumi.Input[str]]] trusted_external_tenants: Specifies a list of tenant IDs that are trusted by the cluster.
        :param pulumi.Input[pulumi.InputType['ClusterVirtualNetworkConfigurationArgs']] virtual_network_configuration: A `virtual_network_configuration` block as defined below.
        :param pulumi.Input[List[pulumi.Input[str]]] zones: A list of Availability Zones in which the cluster instances should be created in. Changing this forces a new resource to be created.
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

            __props__['enable_disk_encryption'] = enable_disk_encryption
            __props__['enable_purge'] = enable_purge
            __props__['enable_streaming_ingest'] = enable_streaming_ingest
            __props__['identity'] = identity
            __props__['language_extensions'] = language_extensions
            __props__['location'] = location
            __props__['name'] = name
            __props__['optimized_auto_scale'] = optimized_auto_scale
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if sku is None:
                raise TypeError("Missing required property 'sku'")
            __props__['sku'] = sku
            __props__['tags'] = tags
            __props__['trusted_external_tenants'] = trusted_external_tenants
            __props__['virtual_network_configuration'] = virtual_network_configuration
            __props__['zones'] = zones
            __props__['data_ingestion_uri'] = None
            __props__['uri'] = None
        super(Cluster, __self__).__init__(
            'azure:kusto/cluster:Cluster',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            data_ingestion_uri: Optional[pulumi.Input[str]] = None,
            enable_disk_encryption: Optional[pulumi.Input[bool]] = None,
            enable_purge: Optional[pulumi.Input[bool]] = None,
            enable_streaming_ingest: Optional[pulumi.Input[bool]] = None,
            identity: Optional[pulumi.Input[pulumi.InputType['ClusterIdentityArgs']]] = None,
            language_extensions: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            optimized_auto_scale: Optional[pulumi.Input[pulumi.InputType['ClusterOptimizedAutoScaleArgs']]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            sku: Optional[pulumi.Input[pulumi.InputType['ClusterSkuArgs']]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            trusted_external_tenants: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            uri: Optional[pulumi.Input[str]] = None,
            virtual_network_configuration: Optional[pulumi.Input[pulumi.InputType['ClusterVirtualNetworkConfigurationArgs']]] = None,
            zones: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None) -> 'Cluster':
        """
        Get an existing Cluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] data_ingestion_uri: The Kusto Cluster URI to be used for data ingestion.
        :param pulumi.Input[bool] enable_disk_encryption: Specifies if the cluster's disks are encrypted.
        :param pulumi.Input[bool] enable_purge: Specifies if the purge operations are enabled.
        :param pulumi.Input[bool] enable_streaming_ingest: Specifies if the streaming ingest is enabled.
        :param pulumi.Input[pulumi.InputType['ClusterIdentityArgs']] identity: A identity block.
        :param pulumi.Input[List[pulumi.Input[str]]] language_extensions: An list of `language_extensions` to enable. Valid values are: `PYTHON` and `R`.
        :param pulumi.Input[str] location: The location where the Kusto Cluster should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Kusto Cluster to create. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['ClusterOptimizedAutoScaleArgs']] optimized_auto_scale: An `optimized_auto_scale` block as defined below.
        :param pulumi.Input[str] resource_group_name: Specifies the Resource Group where the Kusto Cluster should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['ClusterSkuArgs']] sku: A `sku` block as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[List[pulumi.Input[str]]] trusted_external_tenants: Specifies a list of tenant IDs that are trusted by the cluster.
        :param pulumi.Input[str] uri: The FQDN of the Azure Kusto Cluster.
        :param pulumi.Input[pulumi.InputType['ClusterVirtualNetworkConfigurationArgs']] virtual_network_configuration: A `virtual_network_configuration` block as defined below.
        :param pulumi.Input[List[pulumi.Input[str]]] zones: A list of Availability Zones in which the cluster instances should be created in. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["data_ingestion_uri"] = data_ingestion_uri
        __props__["enable_disk_encryption"] = enable_disk_encryption
        __props__["enable_purge"] = enable_purge
        __props__["enable_streaming_ingest"] = enable_streaming_ingest
        __props__["identity"] = identity
        __props__["language_extensions"] = language_extensions
        __props__["location"] = location
        __props__["name"] = name
        __props__["optimized_auto_scale"] = optimized_auto_scale
        __props__["resource_group_name"] = resource_group_name
        __props__["sku"] = sku
        __props__["tags"] = tags
        __props__["trusted_external_tenants"] = trusted_external_tenants
        __props__["uri"] = uri
        __props__["virtual_network_configuration"] = virtual_network_configuration
        __props__["zones"] = zones
        return Cluster(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dataIngestionUri")
    def data_ingestion_uri(self) -> pulumi.Output[str]:
        """
        The Kusto Cluster URI to be used for data ingestion.
        """
        return pulumi.get(self, "data_ingestion_uri")

    @property
    @pulumi.getter(name="enableDiskEncryption")
    def enable_disk_encryption(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies if the cluster's disks are encrypted.
        """
        return pulumi.get(self, "enable_disk_encryption")

    @property
    @pulumi.getter(name="enablePurge")
    def enable_purge(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies if the purge operations are enabled.
        """
        return pulumi.get(self, "enable_purge")

    @property
    @pulumi.getter(name="enableStreamingIngest")
    def enable_streaming_ingest(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies if the streaming ingest is enabled.
        """
        return pulumi.get(self, "enable_streaming_ingest")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output['outputs.ClusterIdentity']:
        """
        A identity block.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="languageExtensions")
    def language_extensions(self) -> pulumi.Output[Optional[List[str]]]:
        """
        An list of `language_extensions` to enable. Valid values are: `PYTHON` and `R`.
        """
        return pulumi.get(self, "language_extensions")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location where the Kusto Cluster should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the Kusto Cluster to create. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="optimizedAutoScale")
    def optimized_auto_scale(self) -> pulumi.Output[Optional['outputs.ClusterOptimizedAutoScale']]:
        """
        An `optimized_auto_scale` block as defined below.
        """
        return pulumi.get(self, "optimized_auto_scale")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        Specifies the Resource Group where the Kusto Cluster should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output['outputs.ClusterSku']:
        """
        A `sku` block as defined below.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="trustedExternalTenants")
    def trusted_external_tenants(self) -> pulumi.Output[List[str]]:
        """
        Specifies a list of tenant IDs that are trusted by the cluster.
        """
        return pulumi.get(self, "trusted_external_tenants")

    @property
    @pulumi.getter
    def uri(self) -> pulumi.Output[str]:
        """
        The FQDN of the Azure Kusto Cluster.
        """
        return pulumi.get(self, "uri")

    @property
    @pulumi.getter(name="virtualNetworkConfiguration")
    def virtual_network_configuration(self) -> pulumi.Output[Optional['outputs.ClusterVirtualNetworkConfiguration']]:
        """
        A `virtual_network_configuration` block as defined below.
        """
        return pulumi.get(self, "virtual_network_configuration")

    @property
    @pulumi.getter
    def zones(self) -> pulumi.Output[Optional[List[str]]]:
        """
        A list of Availability Zones in which the cluster instances should be created in. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "zones")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

