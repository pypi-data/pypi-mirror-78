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

__all__ = ['WindowsFileSystem']


class WindowsFileSystem(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 active_directory_id: Optional[pulumi.Input[str]] = None,
                 automatic_backup_retention_days: Optional[pulumi.Input[float]] = None,
                 copy_tags_to_backups: Optional[pulumi.Input[bool]] = None,
                 daily_automatic_backup_start_time: Optional[pulumi.Input[str]] = None,
                 deployment_type: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 preferred_subnet_id: Optional[pulumi.Input[str]] = None,
                 security_group_ids: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 self_managed_active_directory: Optional[pulumi.Input[pulumi.InputType['WindowsFileSystemSelfManagedActiveDirectoryArgs']]] = None,
                 skip_final_backup: Optional[pulumi.Input[bool]] = None,
                 storage_capacity: Optional[pulumi.Input[float]] = None,
                 storage_type: Optional[pulumi.Input[str]] = None,
                 subnet_ids: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 throughput_capacity: Optional[pulumi.Input[float]] = None,
                 weekly_maintenance_start_time: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Manages a FSx Windows File System. See the [FSx Windows Guide](https://docs.aws.amazon.com/fsx/latest/WindowsGuide/what-is.html) for more information.

        > **NOTE:** Either the `active_directory_id` argument or `self_managed_active_directory` configuration block must be specified.

        ## Example Usage
        ### Using AWS Directory Service

        Additional information for using AWS Directory Service with Windows File Systems can be found in the [FSx Windows Guide](https://docs.aws.amazon.com/fsx/latest/WindowsGuide/fsx-aws-managed-ad.html).

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.fsx.WindowsFileSystem("example",
            active_directory_id=aws_directory_service_directory["example"]["id"],
            kms_key_id=aws_kms_key["example"]["arn"],
            storage_capacity=300,
            subnet_ids=[aws_subnet["example"]["id"]],
            throughput_capacity=1024)
        ```
        ### Using a Self-Managed Microsoft Active Directory

        Additional information for using AWS Directory Service with Windows File Systems can be found in the [FSx Windows Guide](https://docs.aws.amazon.com/fsx/latest/WindowsGuide/self-managed-AD.html).

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.fsx.WindowsFileSystem("example",
            kms_key_id=aws_kms_key["example"]["arn"],
            storage_capacity=300,
            subnet_ids=[aws_subnet["example"]["id"]],
            throughput_capacity=1024,
            self_managed_active_directory=aws.fsx.WindowsFileSystemSelfManagedActiveDirectoryArgs(
                dns_ips=[
                    "10.0.0.111",
                    "10.0.0.222",
                ],
                domain_name="corp.example.com",
                password="avoid-plaintext-passwords",
                username="Admin",
            ))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] active_directory_id: The ID for an existing Microsoft Active Directory instance that the file system should join when it's created. Cannot be specified with `self_managed_active_directory`.
        :param pulumi.Input[float] automatic_backup_retention_days: The number of days to retain automatic backups. Minimum of `0` and maximum of `35`. Defaults to `7`. Set to `0` to disable.
        :param pulumi.Input[bool] copy_tags_to_backups: A boolean flag indicating whether tags on the file system should be copied to backups. Defaults to `false`.
        :param pulumi.Input[str] daily_automatic_backup_start_time: The preferred time (in `HH:MM` format) to take daily automatic backups, in the UTC time zone.
        :param pulumi.Input[str] deployment_type: Specifies the file system deployment type, valid values are `MULTI_AZ_1` and `SINGLE_AZ_1`. Default value is `SINGLE_AZ_1`.
        :param pulumi.Input[str] kms_key_id: ARN for the KMS Key to encrypt the file system at rest. Defaults to an AWS managed KMS Key.
        :param pulumi.Input[str] preferred_subnet_id: Specifies the subnet in which you want the preferred file server to be located. Required for when deployment type is `MULTI_AZ_1`.
        :param pulumi.Input[List[pulumi.Input[str]]] security_group_ids: A list of IDs for the security groups that apply to the specified network interfaces created for file system access. These security groups will apply to all network interfaces.
        :param pulumi.Input[pulumi.InputType['WindowsFileSystemSelfManagedActiveDirectoryArgs']] self_managed_active_directory: Configuration block that Amazon FSx uses to join the Windows File Server instance to your self-managed (including on-premises) Microsoft Active Directory (AD) directory. Cannot be specified with `active_directory_id`. Detailed below.
        :param pulumi.Input[bool] skip_final_backup: When enabled, will skip the default final backup taken when the file system is deleted. This configuration must be applied separately before attempting to delete the resource to have the desired behavior. Defaults to `false`.
        :param pulumi.Input[float] storage_capacity: Storage capacity (GiB) of the file system. Minimum of 32 and maximum of 65536. If the storage type is set to `HDD` the minimum value is 2000.
        :param pulumi.Input[str] storage_type: Specifies the storage type, Valid values are `SSD` and `HDD`. `HDD` is supported on `SINGLE_AZ_1` and `MULTI_AZ_1` Windows file system deployment types. Default value is `SSD`.
        :param pulumi.Input[List[pulumi.Input[str]]] subnet_ids: A list of IDs for the subnets that the file system will be accessible from. To specify more than a single subnet set `deployment_type` to `MULTI_AZ_1`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the file system.
        :param pulumi.Input[float] throughput_capacity: Throughput (megabytes per second) of the file system in power of 2 increments. Minimum of `8` and maximum of `2048`.
        :param pulumi.Input[str] weekly_maintenance_start_time: The preferred start time (in `d:HH:MM` format) to perform weekly maintenance, in the UTC time zone.
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

            __props__['active_directory_id'] = active_directory_id
            __props__['automatic_backup_retention_days'] = automatic_backup_retention_days
            __props__['copy_tags_to_backups'] = copy_tags_to_backups
            __props__['daily_automatic_backup_start_time'] = daily_automatic_backup_start_time
            __props__['deployment_type'] = deployment_type
            __props__['kms_key_id'] = kms_key_id
            __props__['preferred_subnet_id'] = preferred_subnet_id
            __props__['security_group_ids'] = security_group_ids
            __props__['self_managed_active_directory'] = self_managed_active_directory
            __props__['skip_final_backup'] = skip_final_backup
            if storage_capacity is None:
                raise TypeError("Missing required property 'storage_capacity'")
            __props__['storage_capacity'] = storage_capacity
            __props__['storage_type'] = storage_type
            if subnet_ids is None:
                raise TypeError("Missing required property 'subnet_ids'")
            __props__['subnet_ids'] = subnet_ids
            __props__['tags'] = tags
            if throughput_capacity is None:
                raise TypeError("Missing required property 'throughput_capacity'")
            __props__['throughput_capacity'] = throughput_capacity
            __props__['weekly_maintenance_start_time'] = weekly_maintenance_start_time
            __props__['arn'] = None
            __props__['dns_name'] = None
            __props__['network_interface_ids'] = None
            __props__['owner_id'] = None
            __props__['preferred_file_server_ip'] = None
            __props__['remote_administration_endpoint'] = None
            __props__['vpc_id'] = None
        super(WindowsFileSystem, __self__).__init__(
            'aws:fsx/windowsFileSystem:WindowsFileSystem',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            active_directory_id: Optional[pulumi.Input[str]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            automatic_backup_retention_days: Optional[pulumi.Input[float]] = None,
            copy_tags_to_backups: Optional[pulumi.Input[bool]] = None,
            daily_automatic_backup_start_time: Optional[pulumi.Input[str]] = None,
            deployment_type: Optional[pulumi.Input[str]] = None,
            dns_name: Optional[pulumi.Input[str]] = None,
            kms_key_id: Optional[pulumi.Input[str]] = None,
            network_interface_ids: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            owner_id: Optional[pulumi.Input[str]] = None,
            preferred_file_server_ip: Optional[pulumi.Input[str]] = None,
            preferred_subnet_id: Optional[pulumi.Input[str]] = None,
            remote_administration_endpoint: Optional[pulumi.Input[str]] = None,
            security_group_ids: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            self_managed_active_directory: Optional[pulumi.Input[pulumi.InputType['WindowsFileSystemSelfManagedActiveDirectoryArgs']]] = None,
            skip_final_backup: Optional[pulumi.Input[bool]] = None,
            storage_capacity: Optional[pulumi.Input[float]] = None,
            storage_type: Optional[pulumi.Input[str]] = None,
            subnet_ids: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            throughput_capacity: Optional[pulumi.Input[float]] = None,
            vpc_id: Optional[pulumi.Input[str]] = None,
            weekly_maintenance_start_time: Optional[pulumi.Input[str]] = None) -> 'WindowsFileSystem':
        """
        Get an existing WindowsFileSystem resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] active_directory_id: The ID for an existing Microsoft Active Directory instance that the file system should join when it's created. Cannot be specified with `self_managed_active_directory`.
        :param pulumi.Input[str] arn: Amazon Resource Name of the file system.
        :param pulumi.Input[float] automatic_backup_retention_days: The number of days to retain automatic backups. Minimum of `0` and maximum of `35`. Defaults to `7`. Set to `0` to disable.
        :param pulumi.Input[bool] copy_tags_to_backups: A boolean flag indicating whether tags on the file system should be copied to backups. Defaults to `false`.
        :param pulumi.Input[str] daily_automatic_backup_start_time: The preferred time (in `HH:MM` format) to take daily automatic backups, in the UTC time zone.
        :param pulumi.Input[str] deployment_type: Specifies the file system deployment type, valid values are `MULTI_AZ_1` and `SINGLE_AZ_1`. Default value is `SINGLE_AZ_1`.
        :param pulumi.Input[str] dns_name: DNS name for the file system, e.g. `fs-12345678.corp.example.com` (domain name matching the Active Directory domain name)
        :param pulumi.Input[str] kms_key_id: ARN for the KMS Key to encrypt the file system at rest. Defaults to an AWS managed KMS Key.
        :param pulumi.Input[List[pulumi.Input[str]]] network_interface_ids: Set of Elastic Network Interface identifiers from which the file system is accessible.
        :param pulumi.Input[str] owner_id: AWS account identifier that created the file system.
        :param pulumi.Input[str] preferred_file_server_ip: The IP address of the primary, or preferred, file server.
        :param pulumi.Input[str] preferred_subnet_id: Specifies the subnet in which you want the preferred file server to be located. Required for when deployment type is `MULTI_AZ_1`.
        :param pulumi.Input[str] remote_administration_endpoint: For `MULTI_AZ_1` deployment types, use this endpoint when performing administrative tasks on the file system using Amazon FSx Remote PowerShell. For `SINGLE_AZ_1` deployment types, this is the DNS name of the file system.
        :param pulumi.Input[List[pulumi.Input[str]]] security_group_ids: A list of IDs for the security groups that apply to the specified network interfaces created for file system access. These security groups will apply to all network interfaces.
        :param pulumi.Input[pulumi.InputType['WindowsFileSystemSelfManagedActiveDirectoryArgs']] self_managed_active_directory: Configuration block that Amazon FSx uses to join the Windows File Server instance to your self-managed (including on-premises) Microsoft Active Directory (AD) directory. Cannot be specified with `active_directory_id`. Detailed below.
        :param pulumi.Input[bool] skip_final_backup: When enabled, will skip the default final backup taken when the file system is deleted. This configuration must be applied separately before attempting to delete the resource to have the desired behavior. Defaults to `false`.
        :param pulumi.Input[float] storage_capacity: Storage capacity (GiB) of the file system. Minimum of 32 and maximum of 65536. If the storage type is set to `HDD` the minimum value is 2000.
        :param pulumi.Input[str] storage_type: Specifies the storage type, Valid values are `SSD` and `HDD`. `HDD` is supported on `SINGLE_AZ_1` and `MULTI_AZ_1` Windows file system deployment types. Default value is `SSD`.
        :param pulumi.Input[List[pulumi.Input[str]]] subnet_ids: A list of IDs for the subnets that the file system will be accessible from. To specify more than a single subnet set `deployment_type` to `MULTI_AZ_1`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the file system.
        :param pulumi.Input[float] throughput_capacity: Throughput (megabytes per second) of the file system in power of 2 increments. Minimum of `8` and maximum of `2048`.
        :param pulumi.Input[str] vpc_id: Identifier of the Virtual Private Cloud for the file system.
        :param pulumi.Input[str] weekly_maintenance_start_time: The preferred start time (in `d:HH:MM` format) to perform weekly maintenance, in the UTC time zone.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["active_directory_id"] = active_directory_id
        __props__["arn"] = arn
        __props__["automatic_backup_retention_days"] = automatic_backup_retention_days
        __props__["copy_tags_to_backups"] = copy_tags_to_backups
        __props__["daily_automatic_backup_start_time"] = daily_automatic_backup_start_time
        __props__["deployment_type"] = deployment_type
        __props__["dns_name"] = dns_name
        __props__["kms_key_id"] = kms_key_id
        __props__["network_interface_ids"] = network_interface_ids
        __props__["owner_id"] = owner_id
        __props__["preferred_file_server_ip"] = preferred_file_server_ip
        __props__["preferred_subnet_id"] = preferred_subnet_id
        __props__["remote_administration_endpoint"] = remote_administration_endpoint
        __props__["security_group_ids"] = security_group_ids
        __props__["self_managed_active_directory"] = self_managed_active_directory
        __props__["skip_final_backup"] = skip_final_backup
        __props__["storage_capacity"] = storage_capacity
        __props__["storage_type"] = storage_type
        __props__["subnet_ids"] = subnet_ids
        __props__["tags"] = tags
        __props__["throughput_capacity"] = throughput_capacity
        __props__["vpc_id"] = vpc_id
        __props__["weekly_maintenance_start_time"] = weekly_maintenance_start_time
        return WindowsFileSystem(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="activeDirectoryId")
    def active_directory_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID for an existing Microsoft Active Directory instance that the file system should join when it's created. Cannot be specified with `self_managed_active_directory`.
        """
        return pulumi.get(self, "active_directory_id")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name of the file system.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="automaticBackupRetentionDays")
    def automatic_backup_retention_days(self) -> pulumi.Output[Optional[float]]:
        """
        The number of days to retain automatic backups. Minimum of `0` and maximum of `35`. Defaults to `7`. Set to `0` to disable.
        """
        return pulumi.get(self, "automatic_backup_retention_days")

    @property
    @pulumi.getter(name="copyTagsToBackups")
    def copy_tags_to_backups(self) -> pulumi.Output[Optional[bool]]:
        """
        A boolean flag indicating whether tags on the file system should be copied to backups. Defaults to `false`.
        """
        return pulumi.get(self, "copy_tags_to_backups")

    @property
    @pulumi.getter(name="dailyAutomaticBackupStartTime")
    def daily_automatic_backup_start_time(self) -> pulumi.Output[str]:
        """
        The preferred time (in `HH:MM` format) to take daily automatic backups, in the UTC time zone.
        """
        return pulumi.get(self, "daily_automatic_backup_start_time")

    @property
    @pulumi.getter(name="deploymentType")
    def deployment_type(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the file system deployment type, valid values are `MULTI_AZ_1` and `SINGLE_AZ_1`. Default value is `SINGLE_AZ_1`.
        """
        return pulumi.get(self, "deployment_type")

    @property
    @pulumi.getter(name="dnsName")
    def dns_name(self) -> pulumi.Output[str]:
        """
        DNS name for the file system, e.g. `fs-12345678.corp.example.com` (domain name matching the Active Directory domain name)
        """
        return pulumi.get(self, "dns_name")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> pulumi.Output[str]:
        """
        ARN for the KMS Key to encrypt the file system at rest. Defaults to an AWS managed KMS Key.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="networkInterfaceIds")
    def network_interface_ids(self) -> pulumi.Output[List[str]]:
        """
        Set of Elastic Network Interface identifiers from which the file system is accessible.
        """
        return pulumi.get(self, "network_interface_ids")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> pulumi.Output[str]:
        """
        AWS account identifier that created the file system.
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter(name="preferredFileServerIp")
    def preferred_file_server_ip(self) -> pulumi.Output[str]:
        """
        The IP address of the primary, or preferred, file server.
        """
        return pulumi.get(self, "preferred_file_server_ip")

    @property
    @pulumi.getter(name="preferredSubnetId")
    def preferred_subnet_id(self) -> pulumi.Output[str]:
        """
        Specifies the subnet in which you want the preferred file server to be located. Required for when deployment type is `MULTI_AZ_1`.
        """
        return pulumi.get(self, "preferred_subnet_id")

    @property
    @pulumi.getter(name="remoteAdministrationEndpoint")
    def remote_administration_endpoint(self) -> pulumi.Output[str]:
        """
        For `MULTI_AZ_1` deployment types, use this endpoint when performing administrative tasks on the file system using Amazon FSx Remote PowerShell. For `SINGLE_AZ_1` deployment types, this is the DNS name of the file system.
        """
        return pulumi.get(self, "remote_administration_endpoint")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> pulumi.Output[Optional[List[str]]]:
        """
        A list of IDs for the security groups that apply to the specified network interfaces created for file system access. These security groups will apply to all network interfaces.
        """
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="selfManagedActiveDirectory")
    def self_managed_active_directory(self) -> pulumi.Output[Optional['outputs.WindowsFileSystemSelfManagedActiveDirectory']]:
        """
        Configuration block that Amazon FSx uses to join the Windows File Server instance to your self-managed (including on-premises) Microsoft Active Directory (AD) directory. Cannot be specified with `active_directory_id`. Detailed below.
        """
        return pulumi.get(self, "self_managed_active_directory")

    @property
    @pulumi.getter(name="skipFinalBackup")
    def skip_final_backup(self) -> pulumi.Output[Optional[bool]]:
        """
        When enabled, will skip the default final backup taken when the file system is deleted. This configuration must be applied separately before attempting to delete the resource to have the desired behavior. Defaults to `false`.
        """
        return pulumi.get(self, "skip_final_backup")

    @property
    @pulumi.getter(name="storageCapacity")
    def storage_capacity(self) -> pulumi.Output[float]:
        """
        Storage capacity (GiB) of the file system. Minimum of 32 and maximum of 65536. If the storage type is set to `HDD` the minimum value is 2000.
        """
        return pulumi.get(self, "storage_capacity")

    @property
    @pulumi.getter(name="storageType")
    def storage_type(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the storage type, Valid values are `SSD` and `HDD`. `HDD` is supported on `SINGLE_AZ_1` and `MULTI_AZ_1` Windows file system deployment types. Default value is `SSD`.
        """
        return pulumi.get(self, "storage_type")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> pulumi.Output[List[str]]:
        """
        A list of IDs for the subnets that the file system will be accessible from. To specify more than a single subnet set `deployment_type` to `MULTI_AZ_1`.
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the file system.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="throughputCapacity")
    def throughput_capacity(self) -> pulumi.Output[float]:
        """
        Throughput (megabytes per second) of the file system in power of 2 increments. Minimum of `8` and maximum of `2048`.
        """
        return pulumi.get(self, "throughput_capacity")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Output[str]:
        """
        Identifier of the Virtual Private Cloud for the file system.
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="weeklyMaintenanceStartTime")
    def weekly_maintenance_start_time(self) -> pulumi.Output[str]:
        """
        The preferred start time (in `d:HH:MM` format) to perform weekly maintenance, in the UTC time zone.
        """
        return pulumi.get(self, "weekly_maintenance_start_time")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

