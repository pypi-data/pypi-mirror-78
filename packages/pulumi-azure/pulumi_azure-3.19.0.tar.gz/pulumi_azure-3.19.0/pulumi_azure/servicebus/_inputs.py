# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'NamespaceNetworkRuleSetNetworkRuleArgs',
    'SubscriptionRuleCorrelationFilterArgs',
]

@pulumi.input_type
class NamespaceNetworkRuleSetNetworkRuleArgs:
    def __init__(__self__, *,
                 subnet_id: pulumi.Input[str],
                 ignore_missing_vnet_service_endpoint: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[str] subnet_id: The Subnet ID which should be able to access this ServiceBus Namespace.
        :param pulumi.Input[bool] ignore_missing_vnet_service_endpoint: Should the ServiceBus Namespace Network Rule Set ignore missing Virtual Network Service Endpoint option in the Subnet? Defaults to `false`.
        """
        pulumi.set(__self__, "subnet_id", subnet_id)
        if ignore_missing_vnet_service_endpoint is not None:
            pulumi.set(__self__, "ignore_missing_vnet_service_endpoint", ignore_missing_vnet_service_endpoint)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Input[str]:
        """
        The Subnet ID which should be able to access this ServiceBus Namespace.
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "subnet_id", value)

    @property
    @pulumi.getter(name="ignoreMissingVnetServiceEndpoint")
    def ignore_missing_vnet_service_endpoint(self) -> Optional[pulumi.Input[bool]]:
        """
        Should the ServiceBus Namespace Network Rule Set ignore missing Virtual Network Service Endpoint option in the Subnet? Defaults to `false`.
        """
        return pulumi.get(self, "ignore_missing_vnet_service_endpoint")

    @ignore_missing_vnet_service_endpoint.setter
    def ignore_missing_vnet_service_endpoint(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ignore_missing_vnet_service_endpoint", value)


@pulumi.input_type
class SubscriptionRuleCorrelationFilterArgs:
    def __init__(__self__, *,
                 content_type: Optional[pulumi.Input[str]] = None,
                 correlation_id: Optional[pulumi.Input[str]] = None,
                 label: Optional[pulumi.Input[str]] = None,
                 message_id: Optional[pulumi.Input[str]] = None,
                 reply_to: Optional[pulumi.Input[str]] = None,
                 reply_to_session_id: Optional[pulumi.Input[str]] = None,
                 session_id: Optional[pulumi.Input[str]] = None,
                 to: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] content_type: Content type of the message.
        :param pulumi.Input[str] correlation_id: Identifier of the correlation.
        :param pulumi.Input[str] label: Application specific label.
        :param pulumi.Input[str] message_id: Identifier of the message.
        :param pulumi.Input[str] reply_to: Address of the queue to reply to.
        :param pulumi.Input[str] reply_to_session_id: Session identifier to reply to.
        :param pulumi.Input[str] session_id: Session identifier.
        :param pulumi.Input[str] to: Address to send to.
        """
        if content_type is not None:
            pulumi.set(__self__, "content_type", content_type)
        if correlation_id is not None:
            pulumi.set(__self__, "correlation_id", correlation_id)
        if label is not None:
            pulumi.set(__self__, "label", label)
        if message_id is not None:
            pulumi.set(__self__, "message_id", message_id)
        if reply_to is not None:
            pulumi.set(__self__, "reply_to", reply_to)
        if reply_to_session_id is not None:
            pulumi.set(__self__, "reply_to_session_id", reply_to_session_id)
        if session_id is not None:
            pulumi.set(__self__, "session_id", session_id)
        if to is not None:
            pulumi.set(__self__, "to", to)

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> Optional[pulumi.Input[str]]:
        """
        Content type of the message.
        """
        return pulumi.get(self, "content_type")

    @content_type.setter
    def content_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_type", value)

    @property
    @pulumi.getter(name="correlationId")
    def correlation_id(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier of the correlation.
        """
        return pulumi.get(self, "correlation_id")

    @correlation_id.setter
    def correlation_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "correlation_id", value)

    @property
    @pulumi.getter
    def label(self) -> Optional[pulumi.Input[str]]:
        """
        Application specific label.
        """
        return pulumi.get(self, "label")

    @label.setter
    def label(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "label", value)

    @property
    @pulumi.getter(name="messageId")
    def message_id(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier of the message.
        """
        return pulumi.get(self, "message_id")

    @message_id.setter
    def message_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "message_id", value)

    @property
    @pulumi.getter(name="replyTo")
    def reply_to(self) -> Optional[pulumi.Input[str]]:
        """
        Address of the queue to reply to.
        """
        return pulumi.get(self, "reply_to")

    @reply_to.setter
    def reply_to(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "reply_to", value)

    @property
    @pulumi.getter(name="replyToSessionId")
    def reply_to_session_id(self) -> Optional[pulumi.Input[str]]:
        """
        Session identifier to reply to.
        """
        return pulumi.get(self, "reply_to_session_id")

    @reply_to_session_id.setter
    def reply_to_session_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "reply_to_session_id", value)

    @property
    @pulumi.getter(name="sessionId")
    def session_id(self) -> Optional[pulumi.Input[str]]:
        """
        Session identifier.
        """
        return pulumi.get(self, "session_id")

    @session_id.setter
    def session_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "session_id", value)

    @property
    @pulumi.getter
    def to(self) -> Optional[pulumi.Input[str]]:
        """
        Address to send to.
        """
        return pulumi.get(self, "to")

    @to.setter
    def to(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "to", value)


