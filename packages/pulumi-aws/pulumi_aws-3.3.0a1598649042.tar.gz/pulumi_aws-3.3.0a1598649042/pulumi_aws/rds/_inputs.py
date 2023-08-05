# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'ClusterParameterGroupParameterArgs',
    'ClusterS3ImportArgs',
    'ClusterScalingConfigurationArgs',
    'GlobalClusterGlobalClusterMemberArgs',
    'InstanceS3ImportArgs',
    'OptionGroupOptionArgs',
    'OptionGroupOptionOptionSettingArgs',
    'ParameterGroupParameterArgs',
    'SecurityGroupIngressArgs',
]

@pulumi.input_type
class ClusterParameterGroupParameterArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 value: pulumi.Input[str],
                 apply_method: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] name: The name of the DB parameter.
        :param pulumi.Input[str] value: The value of the DB parameter.
        :param pulumi.Input[str] apply_method: "immediate" (default), or "pending-reboot". Some
               engines can't apply some parameters without a reboot, and you will need to
               specify "pending-reboot" here.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)
        if apply_method is not None:
            pulumi.set(__self__, "apply_method", apply_method)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the DB parameter.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value of the DB parameter.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)

    @property
    @pulumi.getter(name="applyMethod")
    def apply_method(self) -> Optional[pulumi.Input[str]]:
        """
        "immediate" (default), or "pending-reboot". Some
        engines can't apply some parameters without a reboot, and you will need to
        specify "pending-reboot" here.
        """
        return pulumi.get(self, "apply_method")

    @apply_method.setter
    def apply_method(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "apply_method", value)


@pulumi.input_type
class ClusterS3ImportArgs:
    def __init__(__self__, *,
                 bucket_name: pulumi.Input[str],
                 ingestion_role: pulumi.Input[str],
                 source_engine: pulumi.Input[str],
                 source_engine_version: pulumi.Input[str],
                 bucket_prefix: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] bucket_name: The bucket name where your backup is stored
        :param pulumi.Input[str] ingestion_role: Role applied to load the data.
        :param pulumi.Input[str] source_engine: Source engine for the backup
        :param pulumi.Input[str] source_engine_version: Version of the source engine used to make the backup
        :param pulumi.Input[str] bucket_prefix: Can be blank, but is the path to your backup
        """
        pulumi.set(__self__, "bucket_name", bucket_name)
        pulumi.set(__self__, "ingestion_role", ingestion_role)
        pulumi.set(__self__, "source_engine", source_engine)
        pulumi.set(__self__, "source_engine_version", source_engine_version)
        if bucket_prefix is not None:
            pulumi.set(__self__, "bucket_prefix", bucket_prefix)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> pulumi.Input[str]:
        """
        The bucket name where your backup is stored
        """
        return pulumi.get(self, "bucket_name")

    @bucket_name.setter
    def bucket_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket_name", value)

    @property
    @pulumi.getter(name="ingestionRole")
    def ingestion_role(self) -> pulumi.Input[str]:
        """
        Role applied to load the data.
        """
        return pulumi.get(self, "ingestion_role")

    @ingestion_role.setter
    def ingestion_role(self, value: pulumi.Input[str]):
        pulumi.set(self, "ingestion_role", value)

    @property
    @pulumi.getter(name="sourceEngine")
    def source_engine(self) -> pulumi.Input[str]:
        """
        Source engine for the backup
        """
        return pulumi.get(self, "source_engine")

    @source_engine.setter
    def source_engine(self, value: pulumi.Input[str]):
        pulumi.set(self, "source_engine", value)

    @property
    @pulumi.getter(name="sourceEngineVersion")
    def source_engine_version(self) -> pulumi.Input[str]:
        """
        Version of the source engine used to make the backup
        """
        return pulumi.get(self, "source_engine_version")

    @source_engine_version.setter
    def source_engine_version(self, value: pulumi.Input[str]):
        pulumi.set(self, "source_engine_version", value)

    @property
    @pulumi.getter(name="bucketPrefix")
    def bucket_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Can be blank, but is the path to your backup
        """
        return pulumi.get(self, "bucket_prefix")

    @bucket_prefix.setter
    def bucket_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket_prefix", value)


@pulumi.input_type
class ClusterScalingConfigurationArgs:
    def __init__(__self__, *,
                 auto_pause: Optional[pulumi.Input[bool]] = None,
                 max_capacity: Optional[pulumi.Input[float]] = None,
                 min_capacity: Optional[pulumi.Input[float]] = None,
                 seconds_until_auto_pause: Optional[pulumi.Input[float]] = None,
                 timeout_action: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[bool] auto_pause: Whether to enable automatic pause. A DB cluster can be paused only when it's idle (it has no connections). If a DB cluster is paused for more than seven days, the DB cluster might be backed up with a snapshot. In this case, the DB cluster is restored when there is a request to connect to it. Defaults to `true`.
        :param pulumi.Input[float] max_capacity: The maximum capacity. The maximum capacity must be greater than or equal to the minimum capacity. Valid capacity values are `1`, `2`, `4`, `8`, `16`, `32`, `64`, `128`, and `256`. Defaults to `16`.
        :param pulumi.Input[float] min_capacity: The minimum capacity. The minimum capacity must be lesser than or equal to the maximum capacity. Valid capacity values are `1`, `2`, `4`, `8`, `16`, `32`, `64`, `128`, and `256`. Defaults to `1`.
        :param pulumi.Input[float] seconds_until_auto_pause: The time, in seconds, before an Aurora DB cluster in serverless mode is paused. Valid values are `300` through `86400`. Defaults to `300`.
        :param pulumi.Input[str] timeout_action: The action to take when the timeout is reached. Valid values: `ForceApplyCapacityChange`, `RollbackCapacityChange`. Defaults to `RollbackCapacityChange`. See [documentation](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless.how-it-works.html#aurora-serverless.how-it-works.timeout-action).
        """
        if auto_pause is not None:
            pulumi.set(__self__, "auto_pause", auto_pause)
        if max_capacity is not None:
            pulumi.set(__self__, "max_capacity", max_capacity)
        if min_capacity is not None:
            pulumi.set(__self__, "min_capacity", min_capacity)
        if seconds_until_auto_pause is not None:
            pulumi.set(__self__, "seconds_until_auto_pause", seconds_until_auto_pause)
        if timeout_action is not None:
            pulumi.set(__self__, "timeout_action", timeout_action)

    @property
    @pulumi.getter(name="autoPause")
    def auto_pause(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to enable automatic pause. A DB cluster can be paused only when it's idle (it has no connections). If a DB cluster is paused for more than seven days, the DB cluster might be backed up with a snapshot. In this case, the DB cluster is restored when there is a request to connect to it. Defaults to `true`.
        """
        return pulumi.get(self, "auto_pause")

    @auto_pause.setter
    def auto_pause(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_pause", value)

    @property
    @pulumi.getter(name="maxCapacity")
    def max_capacity(self) -> Optional[pulumi.Input[float]]:
        """
        The maximum capacity. The maximum capacity must be greater than or equal to the minimum capacity. Valid capacity values are `1`, `2`, `4`, `8`, `16`, `32`, `64`, `128`, and `256`. Defaults to `16`.
        """
        return pulumi.get(self, "max_capacity")

    @max_capacity.setter
    def max_capacity(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "max_capacity", value)

    @property
    @pulumi.getter(name="minCapacity")
    def min_capacity(self) -> Optional[pulumi.Input[float]]:
        """
        The minimum capacity. The minimum capacity must be lesser than or equal to the maximum capacity. Valid capacity values are `1`, `2`, `4`, `8`, `16`, `32`, `64`, `128`, and `256`. Defaults to `1`.
        """
        return pulumi.get(self, "min_capacity")

    @min_capacity.setter
    def min_capacity(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "min_capacity", value)

    @property
    @pulumi.getter(name="secondsUntilAutoPause")
    def seconds_until_auto_pause(self) -> Optional[pulumi.Input[float]]:
        """
        The time, in seconds, before an Aurora DB cluster in serverless mode is paused. Valid values are `300` through `86400`. Defaults to `300`.
        """
        return pulumi.get(self, "seconds_until_auto_pause")

    @seconds_until_auto_pause.setter
    def seconds_until_auto_pause(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "seconds_until_auto_pause", value)

    @property
    @pulumi.getter(name="timeoutAction")
    def timeout_action(self) -> Optional[pulumi.Input[str]]:
        """
        The action to take when the timeout is reached. Valid values: `ForceApplyCapacityChange`, `RollbackCapacityChange`. Defaults to `RollbackCapacityChange`. See [documentation](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless.how-it-works.html#aurora-serverless.how-it-works.timeout-action).
        """
        return pulumi.get(self, "timeout_action")

    @timeout_action.setter
    def timeout_action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "timeout_action", value)


@pulumi.input_type
class GlobalClusterGlobalClusterMemberArgs:
    def __init__(__self__, *,
                 db_cluster_arn: Optional[pulumi.Input[str]] = None,
                 is_writer: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[str] db_cluster_arn: Amazon Resource Name (ARN) of member DB Cluster
        :param pulumi.Input[bool] is_writer: Whether the member is the primary DB Cluster
        """
        if db_cluster_arn is not None:
            pulumi.set(__self__, "db_cluster_arn", db_cluster_arn)
        if is_writer is not None:
            pulumi.set(__self__, "is_writer", is_writer)

    @property
    @pulumi.getter(name="dbClusterArn")
    def db_cluster_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of member DB Cluster
        """
        return pulumi.get(self, "db_cluster_arn")

    @db_cluster_arn.setter
    def db_cluster_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "db_cluster_arn", value)

    @property
    @pulumi.getter(name="isWriter")
    def is_writer(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the member is the primary DB Cluster
        """
        return pulumi.get(self, "is_writer")

    @is_writer.setter
    def is_writer(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_writer", value)


@pulumi.input_type
class InstanceS3ImportArgs:
    def __init__(__self__, *,
                 bucket_name: pulumi.Input[str],
                 ingestion_role: pulumi.Input[str],
                 source_engine: pulumi.Input[str],
                 source_engine_version: pulumi.Input[str],
                 bucket_prefix: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] bucket_name: The bucket name where your backup is stored
        :param pulumi.Input[str] ingestion_role: Role applied to load the data.
        :param pulumi.Input[str] source_engine: Source engine for the backup
        :param pulumi.Input[str] source_engine_version: Version of the source engine used to make the backup
        :param pulumi.Input[str] bucket_prefix: Can be blank, but is the path to your backup
        """
        pulumi.set(__self__, "bucket_name", bucket_name)
        pulumi.set(__self__, "ingestion_role", ingestion_role)
        pulumi.set(__self__, "source_engine", source_engine)
        pulumi.set(__self__, "source_engine_version", source_engine_version)
        if bucket_prefix is not None:
            pulumi.set(__self__, "bucket_prefix", bucket_prefix)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> pulumi.Input[str]:
        """
        The bucket name where your backup is stored
        """
        return pulumi.get(self, "bucket_name")

    @bucket_name.setter
    def bucket_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket_name", value)

    @property
    @pulumi.getter(name="ingestionRole")
    def ingestion_role(self) -> pulumi.Input[str]:
        """
        Role applied to load the data.
        """
        return pulumi.get(self, "ingestion_role")

    @ingestion_role.setter
    def ingestion_role(self, value: pulumi.Input[str]):
        pulumi.set(self, "ingestion_role", value)

    @property
    @pulumi.getter(name="sourceEngine")
    def source_engine(self) -> pulumi.Input[str]:
        """
        Source engine for the backup
        """
        return pulumi.get(self, "source_engine")

    @source_engine.setter
    def source_engine(self, value: pulumi.Input[str]):
        pulumi.set(self, "source_engine", value)

    @property
    @pulumi.getter(name="sourceEngineVersion")
    def source_engine_version(self) -> pulumi.Input[str]:
        """
        Version of the source engine used to make the backup
        """
        return pulumi.get(self, "source_engine_version")

    @source_engine_version.setter
    def source_engine_version(self, value: pulumi.Input[str]):
        pulumi.set(self, "source_engine_version", value)

    @property
    @pulumi.getter(name="bucketPrefix")
    def bucket_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Can be blank, but is the path to your backup
        """
        return pulumi.get(self, "bucket_prefix")

    @bucket_prefix.setter
    def bucket_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket_prefix", value)


@pulumi.input_type
class OptionGroupOptionArgs:
    def __init__(__self__, *,
                 option_name: pulumi.Input[str],
                 db_security_group_memberships: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 option_settings: Optional[pulumi.Input[List[pulumi.Input['OptionGroupOptionOptionSettingArgs']]]] = None,
                 port: Optional[pulumi.Input[float]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 vpc_security_group_memberships: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] option_name: The Name of the Option (e.g. MEMCACHED).
        :param pulumi.Input[List[pulumi.Input[str]]] db_security_group_memberships: A list of DB Security Groups for which the option is enabled.
        :param pulumi.Input[List[pulumi.Input['OptionGroupOptionOptionSettingArgs']]] option_settings: A list of option settings to apply.
        :param pulumi.Input[float] port: The Port number when connecting to the Option (e.g. 11211).
        :param pulumi.Input[str] version: The version of the option (e.g. 13.1.0.0).
        :param pulumi.Input[List[pulumi.Input[str]]] vpc_security_group_memberships: A list of VPC Security Groups for which the option is enabled.
        """
        pulumi.set(__self__, "option_name", option_name)
        if db_security_group_memberships is not None:
            pulumi.set(__self__, "db_security_group_memberships", db_security_group_memberships)
        if option_settings is not None:
            pulumi.set(__self__, "option_settings", option_settings)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if version is not None:
            pulumi.set(__self__, "version", version)
        if vpc_security_group_memberships is not None:
            pulumi.set(__self__, "vpc_security_group_memberships", vpc_security_group_memberships)

    @property
    @pulumi.getter(name="optionName")
    def option_name(self) -> pulumi.Input[str]:
        """
        The Name of the Option (e.g. MEMCACHED).
        """
        return pulumi.get(self, "option_name")

    @option_name.setter
    def option_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "option_name", value)

    @property
    @pulumi.getter(name="dbSecurityGroupMemberships")
    def db_security_group_memberships(self) -> Optional[pulumi.Input[List[pulumi.Input[str]]]]:
        """
        A list of DB Security Groups for which the option is enabled.
        """
        return pulumi.get(self, "db_security_group_memberships")

    @db_security_group_memberships.setter
    def db_security_group_memberships(self, value: Optional[pulumi.Input[List[pulumi.Input[str]]]]):
        pulumi.set(self, "db_security_group_memberships", value)

    @property
    @pulumi.getter(name="optionSettings")
    def option_settings(self) -> Optional[pulumi.Input[List[pulumi.Input['OptionGroupOptionOptionSettingArgs']]]]:
        """
        A list of option settings to apply.
        """
        return pulumi.get(self, "option_settings")

    @option_settings.setter
    def option_settings(self, value: Optional[pulumi.Input[List[pulumi.Input['OptionGroupOptionOptionSettingArgs']]]]):
        pulumi.set(self, "option_settings", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[float]]:
        """
        The Port number when connecting to the Option (e.g. 11211).
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of the option (e.g. 13.1.0.0).
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)

    @property
    @pulumi.getter(name="vpcSecurityGroupMemberships")
    def vpc_security_group_memberships(self) -> Optional[pulumi.Input[List[pulumi.Input[str]]]]:
        """
        A list of VPC Security Groups for which the option is enabled.
        """
        return pulumi.get(self, "vpc_security_group_memberships")

    @vpc_security_group_memberships.setter
    def vpc_security_group_memberships(self, value: Optional[pulumi.Input[List[pulumi.Input[str]]]]):
        pulumi.set(self, "vpc_security_group_memberships", value)


@pulumi.input_type
class OptionGroupOptionOptionSettingArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] name: The Name of the setting.
        :param pulumi.Input[str] value: The Value of the setting.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The Name of the setting.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The Value of the setting.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class ParameterGroupParameterArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 value: pulumi.Input[str],
                 apply_method: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] name: The name of the DB parameter.
        :param pulumi.Input[str] value: The value of the DB parameter.
        :param pulumi.Input[str] apply_method: "immediate" (default), or "pending-reboot". Some
               engines can't apply some parameters without a reboot, and you will need to
               specify "pending-reboot" here.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)
        if apply_method is not None:
            pulumi.set(__self__, "apply_method", apply_method)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the DB parameter.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value of the DB parameter.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)

    @property
    @pulumi.getter(name="applyMethod")
    def apply_method(self) -> Optional[pulumi.Input[str]]:
        """
        "immediate" (default), or "pending-reboot". Some
        engines can't apply some parameters without a reboot, and you will need to
        specify "pending-reboot" here.
        """
        return pulumi.get(self, "apply_method")

    @apply_method.setter
    def apply_method(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "apply_method", value)


@pulumi.input_type
class SecurityGroupIngressArgs:
    def __init__(__self__, *,
                 cidr: Optional[pulumi.Input[str]] = None,
                 security_group_id: Optional[pulumi.Input[str]] = None,
                 security_group_name: Optional[pulumi.Input[str]] = None,
                 security_group_owner_id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] cidr: The CIDR block to accept
        :param pulumi.Input[str] security_group_id: The ID of the security group to authorize
        :param pulumi.Input[str] security_group_name: The name of the security group to authorize
        :param pulumi.Input[str] security_group_owner_id: The owner Id of the security group provided
               by `security_group_name`.
        """
        if cidr is not None:
            pulumi.set(__self__, "cidr", cidr)
        if security_group_id is not None:
            pulumi.set(__self__, "security_group_id", security_group_id)
        if security_group_name is not None:
            pulumi.set(__self__, "security_group_name", security_group_name)
        if security_group_owner_id is not None:
            pulumi.set(__self__, "security_group_owner_id", security_group_owner_id)

    @property
    @pulumi.getter
    def cidr(self) -> Optional[pulumi.Input[str]]:
        """
        The CIDR block to accept
        """
        return pulumi.get(self, "cidr")

    @cidr.setter
    def cidr(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cidr", value)

    @property
    @pulumi.getter(name="securityGroupId")
    def security_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the security group to authorize
        """
        return pulumi.get(self, "security_group_id")

    @security_group_id.setter
    def security_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "security_group_id", value)

    @property
    @pulumi.getter(name="securityGroupName")
    def security_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the security group to authorize
        """
        return pulumi.get(self, "security_group_name")

    @security_group_name.setter
    def security_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "security_group_name", value)

    @property
    @pulumi.getter(name="securityGroupOwnerId")
    def security_group_owner_id(self) -> Optional[pulumi.Input[str]]:
        """
        The owner Id of the security group provided
        by `security_group_name`.
        """
        return pulumi.get(self, "security_group_owner_id")

    @security_group_owner_id.setter
    def security_group_owner_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "security_group_owner_id", value)


