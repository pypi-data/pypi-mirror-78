# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = ['ApiKey']


class ApiKey(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_insights_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 read_permissions: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 write_permissions: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Manages an Application Insights API key.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_insights = azure.appinsights.Insights("exampleInsights",
            location="West Europe",
            resource_group_name=example_resource_group.name,
            application_type="web")
        read_telemetry = azure.appinsights.ApiKey("readTelemetry",
            application_insights_id=example_insights.id,
            read_permissions=[
                "aggregate",
                "api",
                "draft",
                "extendqueries",
                "search",
            ])
        write_annotations = azure.appinsights.ApiKey("writeAnnotations",
            application_insights_id=example_insights.id,
            write_permissions=["annotations"])
        authenticate_sdk_control_channel_api_key = azure.appinsights.ApiKey("authenticateSdkControlChannelApiKey",
            application_insights_id=example_insights.id,
            read_permissions=["agentconfig"])
        full_permissions = azure.appinsights.ApiKey("fullPermissions",
            application_insights_id=example_insights.id,
            read_permissions=[
                "agentconfig",
                "aggregate",
                "api",
                "draft",
                "extendqueries",
                "search",
            ],
            write_permissions=["annotations"])
        pulumi.export("readTelemetryApiKey", read_telemetry.api_key)
        pulumi.export("writeAnnotationsApiKey", write_annotations.api_key)
        pulumi.export("authenticateSdkControlChannel", authenticate_sdk_control_channel_api_key.api_key)
        pulumi.export("fullPermissionsApiKey", full_permissions.api_key)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_insights_id: The ID of the Application Insights component on which the API key operates. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Application Insights API key. Changing this forces a
               new resource to be created.
        :param pulumi.Input[List[pulumi.Input[str]]] read_permissions: Specifies the list of read permissions granted to the API key. Valid values are `agentconfig`, `aggregate`, `api`, `draft`, `extendqueries`, `search`. Please note these values are case sensitive. Changing this forces a new resource to be created.
        :param pulumi.Input[List[pulumi.Input[str]]] write_permissions: Specifies the list of write permissions granted to the API key. Valid values are `annotations`. Please note these values are case sensitive. Changing this forces a new resource to be created.
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

            if application_insights_id is None:
                raise TypeError("Missing required property 'application_insights_id'")
            __props__['application_insights_id'] = application_insights_id
            __props__['name'] = name
            __props__['read_permissions'] = read_permissions
            __props__['write_permissions'] = write_permissions
            __props__['api_key'] = None
        super(ApiKey, __self__).__init__(
            'azure:appinsights/apiKey:ApiKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            api_key: Optional[pulumi.Input[str]] = None,
            application_insights_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            read_permissions: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            write_permissions: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None) -> 'ApiKey':
        """
        Get an existing ApiKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_key: The API Key secret (Sensitive).
        :param pulumi.Input[str] application_insights_id: The ID of the Application Insights component on which the API key operates. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Application Insights API key. Changing this forces a
               new resource to be created.
        :param pulumi.Input[List[pulumi.Input[str]]] read_permissions: Specifies the list of read permissions granted to the API key. Valid values are `agentconfig`, `aggregate`, `api`, `draft`, `extendqueries`, `search`. Please note these values are case sensitive. Changing this forces a new resource to be created.
        :param pulumi.Input[List[pulumi.Input[str]]] write_permissions: Specifies the list of write permissions granted to the API key. Valid values are `annotations`. Please note these values are case sensitive. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["api_key"] = api_key
        __props__["application_insights_id"] = application_insights_id
        __props__["name"] = name
        __props__["read_permissions"] = read_permissions
        __props__["write_permissions"] = write_permissions
        return ApiKey(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiKey")
    def api_key(self) -> pulumi.Output[str]:
        """
        The API Key secret (Sensitive).
        """
        return pulumi.get(self, "api_key")

    @property
    @pulumi.getter(name="applicationInsightsId")
    def application_insights_id(self) -> pulumi.Output[str]:
        """
        The ID of the Application Insights component on which the API key operates. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "application_insights_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Application Insights API key. Changing this forces a
        new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="readPermissions")
    def read_permissions(self) -> pulumi.Output[Optional[List[str]]]:
        """
        Specifies the list of read permissions granted to the API key. Valid values are `agentconfig`, `aggregate`, `api`, `draft`, `extendqueries`, `search`. Please note these values are case sensitive. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "read_permissions")

    @property
    @pulumi.getter(name="writePermissions")
    def write_permissions(self) -> pulumi.Output[Optional[List[str]]]:
        """
        Specifies the list of write permissions granted to the API key. Valid values are `annotations`. Please note these values are case sensitive. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "write_permissions")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

