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

__all__ = ['MLServicesCluster']


class MLServicesCluster(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_version: Optional[pulumi.Input[str]] = None,
                 gateway: Optional[pulumi.Input[pulumi.InputType['MLServicesClusterGatewayArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 roles: Optional[pulumi.Input[pulumi.InputType['MLServicesClusterRolesArgs']]] = None,
                 rstudio: Optional[pulumi.Input[bool]] = None,
                 storage_accounts: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['MLServicesClusterStorageAccountArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tier: Optional[pulumi.Input[str]] = None,
                 tls_min_version: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Create a MLServicesCluster resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_version: Specifies the Version of HDInsights which should be used for this Cluster. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['MLServicesClusterGatewayArgs']] gateway: A `gateway` block as defined below.
        :param pulumi.Input[str] location: Specifies the Azure Region which this HDInsight ML Services Cluster should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name for this HDInsight ML Services Cluster. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group in which this HDInsight ML Services Cluster should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['MLServicesClusterRolesArgs']] roles: A `roles` block as defined below.
        :param pulumi.Input[bool] rstudio: Should R Studio community edition for ML Services be installed? Changing this forces a new resource to be created.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['MLServicesClusterStorageAccountArgs']]]] storage_accounts: One or more `storage_account` block as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of Tags which should be assigned to this HDInsight ML Services Cluster.
        :param pulumi.Input[str] tier: Specifies the Tier which should be used for this HDInsight ML Services Cluster. Possible values are `Standard` or `Premium`. Changing this forces a new resource to be created.
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

            if cluster_version is None:
                raise TypeError("Missing required property 'cluster_version'")
            __props__['cluster_version'] = cluster_version
            if gateway is None:
                raise TypeError("Missing required property 'gateway'")
            __props__['gateway'] = gateway
            __props__['location'] = location
            __props__['name'] = name
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if roles is None:
                raise TypeError("Missing required property 'roles'")
            __props__['roles'] = roles
            if rstudio is None:
                raise TypeError("Missing required property 'rstudio'")
            __props__['rstudio'] = rstudio
            __props__['storage_accounts'] = storage_accounts
            __props__['tags'] = tags
            if tier is None:
                raise TypeError("Missing required property 'tier'")
            __props__['tier'] = tier
            __props__['tls_min_version'] = tls_min_version
            __props__['edge_ssh_endpoint'] = None
            __props__['https_endpoint'] = None
            __props__['ssh_endpoint'] = None
        super(MLServicesCluster, __self__).__init__(
            'azure:hdinsight/mLServicesCluster:MLServicesCluster',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cluster_version: Optional[pulumi.Input[str]] = None,
            edge_ssh_endpoint: Optional[pulumi.Input[str]] = None,
            gateway: Optional[pulumi.Input[pulumi.InputType['MLServicesClusterGatewayArgs']]] = None,
            https_endpoint: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            roles: Optional[pulumi.Input[pulumi.InputType['MLServicesClusterRolesArgs']]] = None,
            rstudio: Optional[pulumi.Input[bool]] = None,
            ssh_endpoint: Optional[pulumi.Input[str]] = None,
            storage_accounts: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['MLServicesClusterStorageAccountArgs']]]]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tier: Optional[pulumi.Input[str]] = None,
            tls_min_version: Optional[pulumi.Input[str]] = None) -> 'MLServicesCluster':
        """
        Get an existing MLServicesCluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_version: Specifies the Version of HDInsights which should be used for this Cluster. Changing this forces a new resource to be created.
        :param pulumi.Input[str] edge_ssh_endpoint: The SSH Connectivity Endpoint for the Edge Node of the HDInsight ML Cluster.
        :param pulumi.Input[pulumi.InputType['MLServicesClusterGatewayArgs']] gateway: A `gateway` block as defined below.
        :param pulumi.Input[str] https_endpoint: The HTTPS Connectivity Endpoint for this HDInsight ML Services Cluster.
        :param pulumi.Input[str] location: Specifies the Azure Region which this HDInsight ML Services Cluster should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name for this HDInsight ML Services Cluster. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group in which this HDInsight ML Services Cluster should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['MLServicesClusterRolesArgs']] roles: A `roles` block as defined below.
        :param pulumi.Input[bool] rstudio: Should R Studio community edition for ML Services be installed? Changing this forces a new resource to be created.
        :param pulumi.Input[str] ssh_endpoint: The SSH Connectivity Endpoint for this HDInsight ML Services Cluster.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['MLServicesClusterStorageAccountArgs']]]] storage_accounts: One or more `storage_account` block as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of Tags which should be assigned to this HDInsight ML Services Cluster.
        :param pulumi.Input[str] tier: Specifies the Tier which should be used for this HDInsight ML Services Cluster. Possible values are `Standard` or `Premium`. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["cluster_version"] = cluster_version
        __props__["edge_ssh_endpoint"] = edge_ssh_endpoint
        __props__["gateway"] = gateway
        __props__["https_endpoint"] = https_endpoint
        __props__["location"] = location
        __props__["name"] = name
        __props__["resource_group_name"] = resource_group_name
        __props__["roles"] = roles
        __props__["rstudio"] = rstudio
        __props__["ssh_endpoint"] = ssh_endpoint
        __props__["storage_accounts"] = storage_accounts
        __props__["tags"] = tags
        __props__["tier"] = tier
        __props__["tls_min_version"] = tls_min_version
        return MLServicesCluster(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clusterVersion")
    def cluster_version(self) -> pulumi.Output[str]:
        """
        Specifies the Version of HDInsights which should be used for this Cluster. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "cluster_version")

    @property
    @pulumi.getter(name="edgeSshEndpoint")
    def edge_ssh_endpoint(self) -> pulumi.Output[str]:
        """
        The SSH Connectivity Endpoint for the Edge Node of the HDInsight ML Cluster.
        """
        return pulumi.get(self, "edge_ssh_endpoint")

    @property
    @pulumi.getter
    def gateway(self) -> pulumi.Output['outputs.MLServicesClusterGateway']:
        """
        A `gateway` block as defined below.
        """
        return pulumi.get(self, "gateway")

    @property
    @pulumi.getter(name="httpsEndpoint")
    def https_endpoint(self) -> pulumi.Output[str]:
        """
        The HTTPS Connectivity Endpoint for this HDInsight ML Services Cluster.
        """
        return pulumi.get(self, "https_endpoint")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Specifies the Azure Region which this HDInsight ML Services Cluster should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name for this HDInsight ML Services Cluster. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Resource Group in which this HDInsight ML Services Cluster should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def roles(self) -> pulumi.Output['outputs.MLServicesClusterRoles']:
        """
        A `roles` block as defined below.
        """
        return pulumi.get(self, "roles")

    @property
    @pulumi.getter
    def rstudio(self) -> pulumi.Output[bool]:
        """
        Should R Studio community edition for ML Services be installed? Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "rstudio")

    @property
    @pulumi.getter(name="sshEndpoint")
    def ssh_endpoint(self) -> pulumi.Output[str]:
        """
        The SSH Connectivity Endpoint for this HDInsight ML Services Cluster.
        """
        return pulumi.get(self, "ssh_endpoint")

    @property
    @pulumi.getter(name="storageAccounts")
    def storage_accounts(self) -> pulumi.Output[Optional[List['outputs.MLServicesClusterStorageAccount']]]:
        """
        One or more `storage_account` block as defined below.
        """
        return pulumi.get(self, "storage_accounts")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of Tags which should be assigned to this HDInsight ML Services Cluster.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def tier(self) -> pulumi.Output[str]:
        """
        Specifies the Tier which should be used for this HDInsight ML Services Cluster. Possible values are `Standard` or `Premium`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "tier")

    @property
    @pulumi.getter(name="tlsMinVersion")
    def tls_min_version(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "tls_min_version")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

