# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'CachePatchSchedule',
    'CacheRedisConfiguration',
    'GetCachePatchScheduleResult',
    'GetCacheRedisConfigurationResult',
]

@pulumi.output_type
class CachePatchSchedule(dict):
    def __init__(__self__, *,
                 day_of_week: str,
                 start_hour_utc: Optional[float] = None):
        pulumi.set(__self__, "day_of_week", day_of_week)
        if start_hour_utc is not None:
            pulumi.set(__self__, "start_hour_utc", start_hour_utc)

    @property
    @pulumi.getter(name="dayOfWeek")
    def day_of_week(self) -> str:
        return pulumi.get(self, "day_of_week")

    @property
    @pulumi.getter(name="startHourUtc")
    def start_hour_utc(self) -> Optional[float]:
        return pulumi.get(self, "start_hour_utc")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class CacheRedisConfiguration(dict):
    def __init__(__self__, *,
                 aof_backup_enabled: Optional[bool] = None,
                 aof_storage_connection_string0: Optional[str] = None,
                 aof_storage_connection_string1: Optional[str] = None,
                 enable_authentication: Optional[bool] = None,
                 maxclients: Optional[float] = None,
                 maxfragmentationmemory_reserved: Optional[float] = None,
                 maxmemory_delta: Optional[float] = None,
                 maxmemory_policy: Optional[str] = None,
                 maxmemory_reserved: Optional[float] = None,
                 notify_keyspace_events: Optional[str] = None,
                 rdb_backup_enabled: Optional[bool] = None,
                 rdb_backup_frequency: Optional[float] = None,
                 rdb_backup_max_snapshot_count: Optional[float] = None,
                 rdb_storage_connection_string: Optional[str] = None):
        """
        :param bool enable_authentication: If set to `false`, the Redis instance will be accessible without authentication. Defaults to `true`.
        :param float maxclients: Returns the max number of connected clients at the same time.
        :param float maxfragmentationmemory_reserved: Value in megabytes reserved to accommodate for memory fragmentation. Defaults are shown below.
        :param float maxmemory_delta: The max-memory delta for this Redis instance. Defaults are shown below.
        :param str maxmemory_policy: How Redis will select what to remove when `maxmemory` is reached. Defaults are shown below.
        :param float maxmemory_reserved: Value in megabytes reserved for non-cache usage e.g. failover. Defaults are shown below.
        :param str notify_keyspace_events: Keyspace notifications allows clients to subscribe to Pub/Sub channels in order to receive events affecting the Redis data set in some way. [Reference](https://redis.io/topics/notifications#configuration)
        :param bool rdb_backup_enabled: Is Backup Enabled? Only supported on Premium SKU's.
        :param float rdb_backup_frequency: The Backup Frequency in Minutes. Only supported on Premium SKU's. Possible values are: `15`, `30`, `60`, `360`, `720` and `1440`.
        :param float rdb_backup_max_snapshot_count: The maximum number of snapshots to create as a backup. Only supported for Premium SKU's.
        :param str rdb_storage_connection_string: The Connection String to the Storage Account. Only supported for Premium SKU's. In the format: `DefaultEndpointsProtocol=https;BlobEndpoint=${azurerm_storage_account.example.primary_blob_endpoint};AccountName=${azurerm_storage_account.example.name};AccountKey=${azurerm_storage_account.example.primary_access_key}`.
        """
        if aof_backup_enabled is not None:
            pulumi.set(__self__, "aof_backup_enabled", aof_backup_enabled)
        if aof_storage_connection_string0 is not None:
            pulumi.set(__self__, "aof_storage_connection_string0", aof_storage_connection_string0)
        if aof_storage_connection_string1 is not None:
            pulumi.set(__self__, "aof_storage_connection_string1", aof_storage_connection_string1)
        if enable_authentication is not None:
            pulumi.set(__self__, "enable_authentication", enable_authentication)
        if maxclients is not None:
            pulumi.set(__self__, "maxclients", maxclients)
        if maxfragmentationmemory_reserved is not None:
            pulumi.set(__self__, "maxfragmentationmemory_reserved", maxfragmentationmemory_reserved)
        if maxmemory_delta is not None:
            pulumi.set(__self__, "maxmemory_delta", maxmemory_delta)
        if maxmemory_policy is not None:
            pulumi.set(__self__, "maxmemory_policy", maxmemory_policy)
        if maxmemory_reserved is not None:
            pulumi.set(__self__, "maxmemory_reserved", maxmemory_reserved)
        if notify_keyspace_events is not None:
            pulumi.set(__self__, "notify_keyspace_events", notify_keyspace_events)
        if rdb_backup_enabled is not None:
            pulumi.set(__self__, "rdb_backup_enabled", rdb_backup_enabled)
        if rdb_backup_frequency is not None:
            pulumi.set(__self__, "rdb_backup_frequency", rdb_backup_frequency)
        if rdb_backup_max_snapshot_count is not None:
            pulumi.set(__self__, "rdb_backup_max_snapshot_count", rdb_backup_max_snapshot_count)
        if rdb_storage_connection_string is not None:
            pulumi.set(__self__, "rdb_storage_connection_string", rdb_storage_connection_string)

    @property
    @pulumi.getter(name="aofBackupEnabled")
    def aof_backup_enabled(self) -> Optional[bool]:
        return pulumi.get(self, "aof_backup_enabled")

    @property
    @pulumi.getter(name="aofStorageConnectionString0")
    def aof_storage_connection_string0(self) -> Optional[str]:
        return pulumi.get(self, "aof_storage_connection_string0")

    @property
    @pulumi.getter(name="aofStorageConnectionString1")
    def aof_storage_connection_string1(self) -> Optional[str]:
        return pulumi.get(self, "aof_storage_connection_string1")

    @property
    @pulumi.getter(name="enableAuthentication")
    def enable_authentication(self) -> Optional[bool]:
        """
        If set to `false`, the Redis instance will be accessible without authentication. Defaults to `true`.
        """
        return pulumi.get(self, "enable_authentication")

    @property
    @pulumi.getter
    def maxclients(self) -> Optional[float]:
        """
        Returns the max number of connected clients at the same time.
        """
        return pulumi.get(self, "maxclients")

    @property
    @pulumi.getter(name="maxfragmentationmemoryReserved")
    def maxfragmentationmemory_reserved(self) -> Optional[float]:
        """
        Value in megabytes reserved to accommodate for memory fragmentation. Defaults are shown below.
        """
        return pulumi.get(self, "maxfragmentationmemory_reserved")

    @property
    @pulumi.getter(name="maxmemoryDelta")
    def maxmemory_delta(self) -> Optional[float]:
        """
        The max-memory delta for this Redis instance. Defaults are shown below.
        """
        return pulumi.get(self, "maxmemory_delta")

    @property
    @pulumi.getter(name="maxmemoryPolicy")
    def maxmemory_policy(self) -> Optional[str]:
        """
        How Redis will select what to remove when `maxmemory` is reached. Defaults are shown below.
        """
        return pulumi.get(self, "maxmemory_policy")

    @property
    @pulumi.getter(name="maxmemoryReserved")
    def maxmemory_reserved(self) -> Optional[float]:
        """
        Value in megabytes reserved for non-cache usage e.g. failover. Defaults are shown below.
        """
        return pulumi.get(self, "maxmemory_reserved")

    @property
    @pulumi.getter(name="notifyKeyspaceEvents")
    def notify_keyspace_events(self) -> Optional[str]:
        """
        Keyspace notifications allows clients to subscribe to Pub/Sub channels in order to receive events affecting the Redis data set in some way. [Reference](https://redis.io/topics/notifications#configuration)
        """
        return pulumi.get(self, "notify_keyspace_events")

    @property
    @pulumi.getter(name="rdbBackupEnabled")
    def rdb_backup_enabled(self) -> Optional[bool]:
        """
        Is Backup Enabled? Only supported on Premium SKU's.
        """
        return pulumi.get(self, "rdb_backup_enabled")

    @property
    @pulumi.getter(name="rdbBackupFrequency")
    def rdb_backup_frequency(self) -> Optional[float]:
        """
        The Backup Frequency in Minutes. Only supported on Premium SKU's. Possible values are: `15`, `30`, `60`, `360`, `720` and `1440`.
        """
        return pulumi.get(self, "rdb_backup_frequency")

    @property
    @pulumi.getter(name="rdbBackupMaxSnapshotCount")
    def rdb_backup_max_snapshot_count(self) -> Optional[float]:
        """
        The maximum number of snapshots to create as a backup. Only supported for Premium SKU's.
        """
        return pulumi.get(self, "rdb_backup_max_snapshot_count")

    @property
    @pulumi.getter(name="rdbStorageConnectionString")
    def rdb_storage_connection_string(self) -> Optional[str]:
        """
        The Connection String to the Storage Account. Only supported for Premium SKU's. In the format: `DefaultEndpointsProtocol=https;BlobEndpoint=${azurerm_storage_account.example.primary_blob_endpoint};AccountName=${azurerm_storage_account.example.name};AccountKey=${azurerm_storage_account.example.primary_access_key}`.
        """
        return pulumi.get(self, "rdb_storage_connection_string")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class GetCachePatchScheduleResult(dict):
    def __init__(__self__, *,
                 day_of_week: str,
                 start_hour_utc: float):
        """
        :param str day_of_week: the Weekday name for the patch item
        :param float start_hour_utc: The Start Hour for maintenance in UTC
        """
        pulumi.set(__self__, "day_of_week", day_of_week)
        pulumi.set(__self__, "start_hour_utc", start_hour_utc)

    @property
    @pulumi.getter(name="dayOfWeek")
    def day_of_week(self) -> str:
        """
        the Weekday name for the patch item
        """
        return pulumi.get(self, "day_of_week")

    @property
    @pulumi.getter(name="startHourUtc")
    def start_hour_utc(self) -> float:
        """
        The Start Hour for maintenance in UTC
        """
        return pulumi.get(self, "start_hour_utc")


@pulumi.output_type
class GetCacheRedisConfigurationResult(dict):
    def __init__(__self__, *,
                 aof_backup_enabled: bool,
                 aof_storage_connection_string0: str,
                 aof_storage_connection_string1: str,
                 enable_authentication: bool,
                 maxclients: float,
                 maxfragmentationmemory_reserved: float,
                 maxmemory_delta: float,
                 maxmemory_policy: str,
                 maxmemory_reserved: float,
                 notify_keyspace_events: str,
                 rdb_backup_enabled: bool,
                 rdb_backup_frequency: float,
                 rdb_backup_max_snapshot_count: float,
                 rdb_storage_connection_string: str):
        """
        :param bool enable_authentication: Specifies if authentication is enabled
        :param float maxfragmentationmemory_reserved: Value in megabytes reserved to accommodate for memory fragmentation.
        :param float maxmemory_delta: The max-memory delta for this Redis instance.
        :param str maxmemory_policy: How Redis will select what to remove when `maxmemory` is reached.
        :param float maxmemory_reserved: The value in megabytes reserved for non-cache usage e.g. failover
        :param bool rdb_backup_enabled: Is Backup Enabled? Only supported on Premium SKU's.
        :param float rdb_backup_frequency: The Backup Frequency in Minutes. Only supported on Premium SKU's.
        :param float rdb_backup_max_snapshot_count: The maximum number of snapshots that can be created as a backup.
        :param str rdb_storage_connection_string: The Connection String to the Storage Account. Only supported for Premium SKU's.
        """
        pulumi.set(__self__, "aof_backup_enabled", aof_backup_enabled)
        pulumi.set(__self__, "aof_storage_connection_string0", aof_storage_connection_string0)
        pulumi.set(__self__, "aof_storage_connection_string1", aof_storage_connection_string1)
        pulumi.set(__self__, "enable_authentication", enable_authentication)
        pulumi.set(__self__, "maxclients", maxclients)
        pulumi.set(__self__, "maxfragmentationmemory_reserved", maxfragmentationmemory_reserved)
        pulumi.set(__self__, "maxmemory_delta", maxmemory_delta)
        pulumi.set(__self__, "maxmemory_policy", maxmemory_policy)
        pulumi.set(__self__, "maxmemory_reserved", maxmemory_reserved)
        pulumi.set(__self__, "notify_keyspace_events", notify_keyspace_events)
        pulumi.set(__self__, "rdb_backup_enabled", rdb_backup_enabled)
        pulumi.set(__self__, "rdb_backup_frequency", rdb_backup_frequency)
        pulumi.set(__self__, "rdb_backup_max_snapshot_count", rdb_backup_max_snapshot_count)
        pulumi.set(__self__, "rdb_storage_connection_string", rdb_storage_connection_string)

    @property
    @pulumi.getter(name="aofBackupEnabled")
    def aof_backup_enabled(self) -> bool:
        return pulumi.get(self, "aof_backup_enabled")

    @property
    @pulumi.getter(name="aofStorageConnectionString0")
    def aof_storage_connection_string0(self) -> str:
        return pulumi.get(self, "aof_storage_connection_string0")

    @property
    @pulumi.getter(name="aofStorageConnectionString1")
    def aof_storage_connection_string1(self) -> str:
        return pulumi.get(self, "aof_storage_connection_string1")

    @property
    @pulumi.getter(name="enableAuthentication")
    def enable_authentication(self) -> bool:
        """
        Specifies if authentication is enabled
        """
        return pulumi.get(self, "enable_authentication")

    @property
    @pulumi.getter
    def maxclients(self) -> float:
        return pulumi.get(self, "maxclients")

    @property
    @pulumi.getter(name="maxfragmentationmemoryReserved")
    def maxfragmentationmemory_reserved(self) -> float:
        """
        Value in megabytes reserved to accommodate for memory fragmentation.
        """
        return pulumi.get(self, "maxfragmentationmemory_reserved")

    @property
    @pulumi.getter(name="maxmemoryDelta")
    def maxmemory_delta(self) -> float:
        """
        The max-memory delta for this Redis instance.
        """
        return pulumi.get(self, "maxmemory_delta")

    @property
    @pulumi.getter(name="maxmemoryPolicy")
    def maxmemory_policy(self) -> str:
        """
        How Redis will select what to remove when `maxmemory` is reached.
        """
        return pulumi.get(self, "maxmemory_policy")

    @property
    @pulumi.getter(name="maxmemoryReserved")
    def maxmemory_reserved(self) -> float:
        """
        The value in megabytes reserved for non-cache usage e.g. failover
        """
        return pulumi.get(self, "maxmemory_reserved")

    @property
    @pulumi.getter(name="notifyKeyspaceEvents")
    def notify_keyspace_events(self) -> str:
        return pulumi.get(self, "notify_keyspace_events")

    @property
    @pulumi.getter(name="rdbBackupEnabled")
    def rdb_backup_enabled(self) -> bool:
        """
        Is Backup Enabled? Only supported on Premium SKU's.
        """
        return pulumi.get(self, "rdb_backup_enabled")

    @property
    @pulumi.getter(name="rdbBackupFrequency")
    def rdb_backup_frequency(self) -> float:
        """
        The Backup Frequency in Minutes. Only supported on Premium SKU's.
        """
        return pulumi.get(self, "rdb_backup_frequency")

    @property
    @pulumi.getter(name="rdbBackupMaxSnapshotCount")
    def rdb_backup_max_snapshot_count(self) -> float:
        """
        The maximum number of snapshots that can be created as a backup.
        """
        return pulumi.get(self, "rdb_backup_max_snapshot_count")

    @property
    @pulumi.getter(name="rdbStorageConnectionString")
    def rdb_storage_connection_string(self) -> str:
        """
        The Connection String to the Storage Account. Only supported for Premium SKU's.
        """
        return pulumi.get(self, "rdb_storage_connection_string")


