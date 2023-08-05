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

__all__ = ['Database']


class Database(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_pause_delay_in_minutes: Optional[pulumi.Input[float]] = None,
                 collation: Optional[pulumi.Input[str]] = None,
                 create_mode: Optional[pulumi.Input[str]] = None,
                 creation_source_database_id: Optional[pulumi.Input[str]] = None,
                 elastic_pool_id: Optional[pulumi.Input[str]] = None,
                 extended_auditing_policy: Optional[pulumi.Input[pulumi.InputType['DatabaseExtendedAuditingPolicyArgs']]] = None,
                 license_type: Optional[pulumi.Input[str]] = None,
                 max_size_gb: Optional[pulumi.Input[float]] = None,
                 min_capacity: Optional[pulumi.Input[float]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 read_replica_count: Optional[pulumi.Input[float]] = None,
                 read_scale: Optional[pulumi.Input[bool]] = None,
                 restore_point_in_time: Optional[pulumi.Input[str]] = None,
                 sample_name: Optional[pulumi.Input[str]] = None,
                 server_id: Optional[pulumi.Input[str]] = None,
                 sku_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 threat_detection_policy: Optional[pulumi.Input[pulumi.InputType['DatabaseThreatDetectionPolicyArgs']]] = None,
                 zone_redundant: Optional[pulumi.Input[bool]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Manages a MS SQL Database.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS")
        example_sql_server = azure.sql.SqlServer("exampleSqlServer",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            version="12.0",
            administrator_login="4dm1n157r470r",
            administrator_login_password="4-v3ry-53cr37-p455w0rd")
        test = azure.mssql.Database("test",
            server_id=example_sql_server.id,
            collation="SQL_Latin1_General_CP1_CI_AS",
            license_type="LicenseIncluded",
            max_size_gb=4,
            read_scale=True,
            sku_name="BC_Gen5_2",
            zone_redundant=True,
            extended_auditing_policy=azure.mssql.DatabaseExtendedAuditingPolicyArgs(
                storage_endpoint=example_account.primary_blob_endpoint,
                storage_account_access_key=example_account.primary_access_key,
                storage_account_access_key_is_secondary=True,
                retention_in_days=6,
            ),
            tags={
                "foo": "bar",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] auto_pause_delay_in_minutes: Time in minutes after which database is automatically paused. A value of `-1` means that automatic pause is disabled. This property is only settable for General Purpose Serverless databases.
        :param pulumi.Input[str] collation: Specifies the collation of the database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] create_mode: The create mode of the database. Possible values are `Copy`, `Default`, `OnlineSecondary`, `PointInTimeRestore`, `Restore`, `RestoreExternalBackup`, `RestoreExternalBackupSecondary`, `RestoreLongTermRetentionBackup` and `Secondary`.
        :param pulumi.Input[str] creation_source_database_id: The id of the source database to be referred to create the new database. This should only be used for databases with `create_mode` values that use another database as reference. Changing this forces a new resource to be created.
        :param pulumi.Input[str] elastic_pool_id: Specifies the ID of the elastic pool containing this database.
        :param pulumi.Input[pulumi.InputType['DatabaseExtendedAuditingPolicyArgs']] extended_auditing_policy: A `extended_auditing_policy` block as defined below.
        :param pulumi.Input[str] license_type: Specifies the license type applied to this database. Possible values are `LicenseIncluded` and `BasePrice`.
        :param pulumi.Input[float] max_size_gb: The max size of the database in gigabytes.
        :param pulumi.Input[float] min_capacity: Minimal capacity that database will always have allocated, if not paused. This property is only settable for General Purpose Serverless databases.
        :param pulumi.Input[str] name: The name of the Ms SQL Database. Changing this forces a new resource to be created.
        :param pulumi.Input[float] read_replica_count: The number of readonly secondary replicas associated with the database to which readonly application intent connections may be routed. This property is only settable for Hyperscale edition databases.
        :param pulumi.Input[bool] read_scale: If enabled, connections that have application intent set to readonly in their connection string may be routed to a readonly secondary replica. This property is only settable for Premium and Business Critical databases.
        :param pulumi.Input[str] restore_point_in_time: Specifies the point in time (ISO8601 format) of the source database that will be restored to create the new database. This property is only settable for `create_mode`= `PointInTimeRestore`  databases.
        :param pulumi.Input[str] sample_name: Specifies the name of the sample schema to apply when creating this database. Possible value is `AdventureWorksLT`.
        :param pulumi.Input[str] server_id: The id of the Ms SQL Server on which to create the database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sku_name: Specifies the name of the sku used by the database. Only changing this from tier `Hyperscale` to another tier will force a new resource to be created. For example, `GP_S_Gen5_2`,`HS_Gen4_1`,`BC_Gen5_2`, `ElasticPool`, `Basic`,`S0`, `P2` ,`DW100c`, `DS100`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[pulumi.InputType['DatabaseThreatDetectionPolicyArgs']] threat_detection_policy: Threat detection policy configuration. The `threat_detection_policy` block supports fields documented below.
        :param pulumi.Input[bool] zone_redundant: Whether or not this database is zone redundant, which means the replicas of this database will be spread across multiple availability zones. This property is only settable for Premium and Business Critical databases.
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

            __props__['auto_pause_delay_in_minutes'] = auto_pause_delay_in_minutes
            __props__['collation'] = collation
            __props__['create_mode'] = create_mode
            __props__['creation_source_database_id'] = creation_source_database_id
            __props__['elastic_pool_id'] = elastic_pool_id
            __props__['extended_auditing_policy'] = extended_auditing_policy
            __props__['license_type'] = license_type
            __props__['max_size_gb'] = max_size_gb
            __props__['min_capacity'] = min_capacity
            __props__['name'] = name
            __props__['read_replica_count'] = read_replica_count
            __props__['read_scale'] = read_scale
            __props__['restore_point_in_time'] = restore_point_in_time
            __props__['sample_name'] = sample_name
            if server_id is None:
                raise TypeError("Missing required property 'server_id'")
            __props__['server_id'] = server_id
            __props__['sku_name'] = sku_name
            __props__['tags'] = tags
            __props__['threat_detection_policy'] = threat_detection_policy
            __props__['zone_redundant'] = zone_redundant
        super(Database, __self__).__init__(
            'azure:mssql/database:Database',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            auto_pause_delay_in_minutes: Optional[pulumi.Input[float]] = None,
            collation: Optional[pulumi.Input[str]] = None,
            create_mode: Optional[pulumi.Input[str]] = None,
            creation_source_database_id: Optional[pulumi.Input[str]] = None,
            elastic_pool_id: Optional[pulumi.Input[str]] = None,
            extended_auditing_policy: Optional[pulumi.Input[pulumi.InputType['DatabaseExtendedAuditingPolicyArgs']]] = None,
            license_type: Optional[pulumi.Input[str]] = None,
            max_size_gb: Optional[pulumi.Input[float]] = None,
            min_capacity: Optional[pulumi.Input[float]] = None,
            name: Optional[pulumi.Input[str]] = None,
            read_replica_count: Optional[pulumi.Input[float]] = None,
            read_scale: Optional[pulumi.Input[bool]] = None,
            restore_point_in_time: Optional[pulumi.Input[str]] = None,
            sample_name: Optional[pulumi.Input[str]] = None,
            server_id: Optional[pulumi.Input[str]] = None,
            sku_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            threat_detection_policy: Optional[pulumi.Input[pulumi.InputType['DatabaseThreatDetectionPolicyArgs']]] = None,
            zone_redundant: Optional[pulumi.Input[bool]] = None) -> 'Database':
        """
        Get an existing Database resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] auto_pause_delay_in_minutes: Time in minutes after which database is automatically paused. A value of `-1` means that automatic pause is disabled. This property is only settable for General Purpose Serverless databases.
        :param pulumi.Input[str] collation: Specifies the collation of the database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] create_mode: The create mode of the database. Possible values are `Copy`, `Default`, `OnlineSecondary`, `PointInTimeRestore`, `Restore`, `RestoreExternalBackup`, `RestoreExternalBackupSecondary`, `RestoreLongTermRetentionBackup` and `Secondary`.
        :param pulumi.Input[str] creation_source_database_id: The id of the source database to be referred to create the new database. This should only be used for databases with `create_mode` values that use another database as reference. Changing this forces a new resource to be created.
        :param pulumi.Input[str] elastic_pool_id: Specifies the ID of the elastic pool containing this database.
        :param pulumi.Input[pulumi.InputType['DatabaseExtendedAuditingPolicyArgs']] extended_auditing_policy: A `extended_auditing_policy` block as defined below.
        :param pulumi.Input[str] license_type: Specifies the license type applied to this database. Possible values are `LicenseIncluded` and `BasePrice`.
        :param pulumi.Input[float] max_size_gb: The max size of the database in gigabytes.
        :param pulumi.Input[float] min_capacity: Minimal capacity that database will always have allocated, if not paused. This property is only settable for General Purpose Serverless databases.
        :param pulumi.Input[str] name: The name of the Ms SQL Database. Changing this forces a new resource to be created.
        :param pulumi.Input[float] read_replica_count: The number of readonly secondary replicas associated with the database to which readonly application intent connections may be routed. This property is only settable for Hyperscale edition databases.
        :param pulumi.Input[bool] read_scale: If enabled, connections that have application intent set to readonly in their connection string may be routed to a readonly secondary replica. This property is only settable for Premium and Business Critical databases.
        :param pulumi.Input[str] restore_point_in_time: Specifies the point in time (ISO8601 format) of the source database that will be restored to create the new database. This property is only settable for `create_mode`= `PointInTimeRestore`  databases.
        :param pulumi.Input[str] sample_name: Specifies the name of the sample schema to apply when creating this database. Possible value is `AdventureWorksLT`.
        :param pulumi.Input[str] server_id: The id of the Ms SQL Server on which to create the database. Changing this forces a new resource to be created.
        :param pulumi.Input[str] sku_name: Specifies the name of the sku used by the database. Only changing this from tier `Hyperscale` to another tier will force a new resource to be created. For example, `GP_S_Gen5_2`,`HS_Gen4_1`,`BC_Gen5_2`, `ElasticPool`, `Basic`,`S0`, `P2` ,`DW100c`, `DS100`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[pulumi.InputType['DatabaseThreatDetectionPolicyArgs']] threat_detection_policy: Threat detection policy configuration. The `threat_detection_policy` block supports fields documented below.
        :param pulumi.Input[bool] zone_redundant: Whether or not this database is zone redundant, which means the replicas of this database will be spread across multiple availability zones. This property is only settable for Premium and Business Critical databases.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["auto_pause_delay_in_minutes"] = auto_pause_delay_in_minutes
        __props__["collation"] = collation
        __props__["create_mode"] = create_mode
        __props__["creation_source_database_id"] = creation_source_database_id
        __props__["elastic_pool_id"] = elastic_pool_id
        __props__["extended_auditing_policy"] = extended_auditing_policy
        __props__["license_type"] = license_type
        __props__["max_size_gb"] = max_size_gb
        __props__["min_capacity"] = min_capacity
        __props__["name"] = name
        __props__["read_replica_count"] = read_replica_count
        __props__["read_scale"] = read_scale
        __props__["restore_point_in_time"] = restore_point_in_time
        __props__["sample_name"] = sample_name
        __props__["server_id"] = server_id
        __props__["sku_name"] = sku_name
        __props__["tags"] = tags
        __props__["threat_detection_policy"] = threat_detection_policy
        __props__["zone_redundant"] = zone_redundant
        return Database(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="autoPauseDelayInMinutes")
    def auto_pause_delay_in_minutes(self) -> pulumi.Output[float]:
        """
        Time in minutes after which database is automatically paused. A value of `-1` means that automatic pause is disabled. This property is only settable for General Purpose Serverless databases.
        """
        return pulumi.get(self, "auto_pause_delay_in_minutes")

    @property
    @pulumi.getter
    def collation(self) -> pulumi.Output[str]:
        """
        Specifies the collation of the database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "collation")

    @property
    @pulumi.getter(name="createMode")
    def create_mode(self) -> pulumi.Output[str]:
        """
        The create mode of the database. Possible values are `Copy`, `Default`, `OnlineSecondary`, `PointInTimeRestore`, `Restore`, `RestoreExternalBackup`, `RestoreExternalBackupSecondary`, `RestoreLongTermRetentionBackup` and `Secondary`.
        """
        return pulumi.get(self, "create_mode")

    @property
    @pulumi.getter(name="creationSourceDatabaseId")
    def creation_source_database_id(self) -> pulumi.Output[str]:
        """
        The id of the source database to be referred to create the new database. This should only be used for databases with `create_mode` values that use another database as reference. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "creation_source_database_id")

    @property
    @pulumi.getter(name="elasticPoolId")
    def elastic_pool_id(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the ID of the elastic pool containing this database.
        """
        return pulumi.get(self, "elastic_pool_id")

    @property
    @pulumi.getter(name="extendedAuditingPolicy")
    def extended_auditing_policy(self) -> pulumi.Output[Optional['outputs.DatabaseExtendedAuditingPolicy']]:
        """
        A `extended_auditing_policy` block as defined below.
        """
        return pulumi.get(self, "extended_auditing_policy")

    @property
    @pulumi.getter(name="licenseType")
    def license_type(self) -> pulumi.Output[str]:
        """
        Specifies the license type applied to this database. Possible values are `LicenseIncluded` and `BasePrice`.
        """
        return pulumi.get(self, "license_type")

    @property
    @pulumi.getter(name="maxSizeGb")
    def max_size_gb(self) -> pulumi.Output[float]:
        """
        The max size of the database in gigabytes.
        """
        return pulumi.get(self, "max_size_gb")

    @property
    @pulumi.getter(name="minCapacity")
    def min_capacity(self) -> pulumi.Output[float]:
        """
        Minimal capacity that database will always have allocated, if not paused. This property is only settable for General Purpose Serverless databases.
        """
        return pulumi.get(self, "min_capacity")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the Ms SQL Database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="readReplicaCount")
    def read_replica_count(self) -> pulumi.Output[float]:
        """
        The number of readonly secondary replicas associated with the database to which readonly application intent connections may be routed. This property is only settable for Hyperscale edition databases.
        """
        return pulumi.get(self, "read_replica_count")

    @property
    @pulumi.getter(name="readScale")
    def read_scale(self) -> pulumi.Output[bool]:
        """
        If enabled, connections that have application intent set to readonly in their connection string may be routed to a readonly secondary replica. This property is only settable for Premium and Business Critical databases.
        """
        return pulumi.get(self, "read_scale")

    @property
    @pulumi.getter(name="restorePointInTime")
    def restore_point_in_time(self) -> pulumi.Output[str]:
        """
        Specifies the point in time (ISO8601 format) of the source database that will be restored to create the new database. This property is only settable for `create_mode`= `PointInTimeRestore`  databases.
        """
        return pulumi.get(self, "restore_point_in_time")

    @property
    @pulumi.getter(name="sampleName")
    def sample_name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the sample schema to apply when creating this database. Possible value is `AdventureWorksLT`.
        """
        return pulumi.get(self, "sample_name")

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> pulumi.Output[str]:
        """
        The id of the Ms SQL Server on which to create the database. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "server_id")

    @property
    @pulumi.getter(name="skuName")
    def sku_name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the sku used by the database. Only changing this from tier `Hyperscale` to another tier will force a new resource to be created. For example, `GP_S_Gen5_2`,`HS_Gen4_1`,`BC_Gen5_2`, `ElasticPool`, `Basic`,`S0`, `P2` ,`DW100c`, `DS100`.
        """
        return pulumi.get(self, "sku_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="threatDetectionPolicy")
    def threat_detection_policy(self) -> pulumi.Output['outputs.DatabaseThreatDetectionPolicy']:
        """
        Threat detection policy configuration. The `threat_detection_policy` block supports fields documented below.
        """
        return pulumi.get(self, "threat_detection_policy")

    @property
    @pulumi.getter(name="zoneRedundant")
    def zone_redundant(self) -> pulumi.Output[bool]:
        """
        Whether or not this database is zone redundant, which means the replicas of this database will be spread across multiple availability zones. This property is only settable for Premium and Business Critical databases.
        """
        return pulumi.get(self, "zone_redundant")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

