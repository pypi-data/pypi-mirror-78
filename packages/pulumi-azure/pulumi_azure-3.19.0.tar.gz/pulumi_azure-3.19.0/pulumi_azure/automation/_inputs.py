# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'ModuleModuleLinkArgs',
    'ModuleModuleLinkHashArgs',
    'RunBookJobScheduleArgs',
    'RunBookPublishContentLinkArgs',
    'RunBookPublishContentLinkHashArgs',
    'ScheduleMonthlyOccurrenceArgs',
]

@pulumi.input_type
class ModuleModuleLinkArgs:
    def __init__(__self__, *,
                 uri: pulumi.Input[str],
                 hash: Optional[pulumi.Input['ModuleModuleLinkHashArgs']] = None):
        """
        :param pulumi.Input[str] uri: The uri of the module content (zip or nupkg).
        """
        pulumi.set(__self__, "uri", uri)
        if hash is not None:
            pulumi.set(__self__, "hash", hash)

    @property
    @pulumi.getter
    def uri(self) -> pulumi.Input[str]:
        """
        The uri of the module content (zip or nupkg).
        """
        return pulumi.get(self, "uri")

    @uri.setter
    def uri(self, value: pulumi.Input[str]):
        pulumi.set(self, "uri", value)

    @property
    @pulumi.getter
    def hash(self) -> Optional[pulumi.Input['ModuleModuleLinkHashArgs']]:
        return pulumi.get(self, "hash")

    @hash.setter
    def hash(self, value: Optional[pulumi.Input['ModuleModuleLinkHashArgs']]):
        pulumi.set(self, "hash", value)


@pulumi.input_type
class ModuleModuleLinkHashArgs:
    def __init__(__self__, *,
                 algorithm: pulumi.Input[str],
                 value: pulumi.Input[str]):
        pulumi.set(__self__, "algorithm", algorithm)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def algorithm(self) -> pulumi.Input[str]:
        return pulumi.get(self, "algorithm")

    @algorithm.setter
    def algorithm(self, value: pulumi.Input[str]):
        pulumi.set(self, "algorithm", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class RunBookJobScheduleArgs:
    def __init__(__self__, *,
                 schedule_name: pulumi.Input[str],
                 job_schedule_id: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 run_on: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "schedule_name", schedule_name)
        if job_schedule_id is not None:
            pulumi.set(__self__, "job_schedule_id", job_schedule_id)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if run_on is not None:
            pulumi.set(__self__, "run_on", run_on)

    @property
    @pulumi.getter(name="scheduleName")
    def schedule_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "schedule_name")

    @schedule_name.setter
    def schedule_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "schedule_name", value)

    @property
    @pulumi.getter(name="jobScheduleId")
    def job_schedule_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "job_schedule_id")

    @job_schedule_id.setter
    def job_schedule_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "job_schedule_id", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "parameters", value)

    @property
    @pulumi.getter(name="runOn")
    def run_on(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "run_on")

    @run_on.setter
    def run_on(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "run_on", value)


@pulumi.input_type
class RunBookPublishContentLinkArgs:
    def __init__(__self__, *,
                 uri: pulumi.Input[str],
                 hash: Optional[pulumi.Input['RunBookPublishContentLinkHashArgs']] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] uri: The uri of the runbook content.
        """
        pulumi.set(__self__, "uri", uri)
        if hash is not None:
            pulumi.set(__self__, "hash", hash)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def uri(self) -> pulumi.Input[str]:
        """
        The uri of the runbook content.
        """
        return pulumi.get(self, "uri")

    @uri.setter
    def uri(self, value: pulumi.Input[str]):
        pulumi.set(self, "uri", value)

    @property
    @pulumi.getter
    def hash(self) -> Optional[pulumi.Input['RunBookPublishContentLinkHashArgs']]:
        return pulumi.get(self, "hash")

    @hash.setter
    def hash(self, value: Optional[pulumi.Input['RunBookPublishContentLinkHashArgs']]):
        pulumi.set(self, "hash", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class RunBookPublishContentLinkHashArgs:
    def __init__(__self__, *,
                 algorithm: pulumi.Input[str],
                 value: pulumi.Input[str]):
        pulumi.set(__self__, "algorithm", algorithm)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def algorithm(self) -> pulumi.Input[str]:
        return pulumi.get(self, "algorithm")

    @algorithm.setter
    def algorithm(self, value: pulumi.Input[str]):
        pulumi.set(self, "algorithm", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class ScheduleMonthlyOccurrenceArgs:
    def __init__(__self__, *,
                 day: pulumi.Input[str],
                 occurrence: pulumi.Input[float]):
        """
        :param pulumi.Input[str] day: Day of the occurrence. Must be one of `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `Saturday`, `Sunday`.
        :param pulumi.Input[float] occurrence: Occurrence of the week within the month. Must be between `1` and `5`. `-1` for last week within the month.
        """
        pulumi.set(__self__, "day", day)
        pulumi.set(__self__, "occurrence", occurrence)

    @property
    @pulumi.getter
    def day(self) -> pulumi.Input[str]:
        """
        Day of the occurrence. Must be one of `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `Saturday`, `Sunday`.
        """
        return pulumi.get(self, "day")

    @day.setter
    def day(self, value: pulumi.Input[str]):
        pulumi.set(self, "day", value)

    @property
    @pulumi.getter
    def occurrence(self) -> pulumi.Input[float]:
        """
        Occurrence of the week within the month. Must be between `1` and `5`. `-1` for last week within the month.
        """
        return pulumi.get(self, "occurrence")

    @occurrence.setter
    def occurrence(self, value: pulumi.Input[float]):
        pulumi.set(self, "occurrence", value)


