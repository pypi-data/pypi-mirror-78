# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'ClusterLoggingArgs',
    'ClusterSnapshotCopyArgs',
    'ParameterGroupParameterArgs',
    'SecurityGroupIngressArgs',
]

@pulumi.input_type
class ClusterLoggingArgs:
    def __init__(__self__, *,
                 enable: pulumi.Input[bool],
                 bucket_name: Optional[pulumi.Input[str]] = None,
                 s3_key_prefix: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[bool] enable: Enables logging information such as queries and connection attempts, for the specified Amazon Redshift cluster.
        :param pulumi.Input[str] bucket_name: The name of an existing S3 bucket where the log files are to be stored. Must be in the same region as the cluster and the cluster must have read bucket and put object permissions.
               For more information on the permissions required for the bucket, please read the AWS [documentation](http://docs.aws.amazon.com/redshift/latest/mgmt/db-auditing.html#db-auditing-enable-logging)
        :param pulumi.Input[str] s3_key_prefix: The prefix applied to the log file names.
        """
        pulumi.set(__self__, "enable", enable)
        if bucket_name is not None:
            pulumi.set(__self__, "bucket_name", bucket_name)
        if s3_key_prefix is not None:
            pulumi.set(__self__, "s3_key_prefix", s3_key_prefix)

    @property
    @pulumi.getter
    def enable(self) -> pulumi.Input[bool]:
        """
        Enables logging information such as queries and connection attempts, for the specified Amazon Redshift cluster.
        """
        return pulumi.get(self, "enable")

    @enable.setter
    def enable(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enable", value)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of an existing S3 bucket where the log files are to be stored. Must be in the same region as the cluster and the cluster must have read bucket and put object permissions.
        For more information on the permissions required for the bucket, please read the AWS [documentation](http://docs.aws.amazon.com/redshift/latest/mgmt/db-auditing.html#db-auditing-enable-logging)
        """
        return pulumi.get(self, "bucket_name")

    @bucket_name.setter
    def bucket_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket_name", value)

    @property
    @pulumi.getter(name="s3KeyPrefix")
    def s3_key_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        The prefix applied to the log file names.
        """
        return pulumi.get(self, "s3_key_prefix")

    @s3_key_prefix.setter
    def s3_key_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "s3_key_prefix", value)


@pulumi.input_type
class ClusterSnapshotCopyArgs:
    def __init__(__self__, *,
                 destination_region: pulumi.Input[str],
                 grant_name: Optional[pulumi.Input[str]] = None,
                 retention_period: Optional[pulumi.Input[float]] = None):
        """
        :param pulumi.Input[str] destination_region: The destination region that you want to copy snapshots to.
        :param pulumi.Input[str] grant_name: The name of the snapshot copy grant to use when snapshots of an AWS KMS-encrypted cluster are copied to the destination region.
        :param pulumi.Input[float] retention_period: The number of days to retain automated snapshots in the destination region after they are copied from the source region. Defaults to `7`.
        """
        pulumi.set(__self__, "destination_region", destination_region)
        if grant_name is not None:
            pulumi.set(__self__, "grant_name", grant_name)
        if retention_period is not None:
            pulumi.set(__self__, "retention_period", retention_period)

    @property
    @pulumi.getter(name="destinationRegion")
    def destination_region(self) -> pulumi.Input[str]:
        """
        The destination region that you want to copy snapshots to.
        """
        return pulumi.get(self, "destination_region")

    @destination_region.setter
    def destination_region(self, value: pulumi.Input[str]):
        pulumi.set(self, "destination_region", value)

    @property
    @pulumi.getter(name="grantName")
    def grant_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the snapshot copy grant to use when snapshots of an AWS KMS-encrypted cluster are copied to the destination region.
        """
        return pulumi.get(self, "grant_name")

    @grant_name.setter
    def grant_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "grant_name", value)

    @property
    @pulumi.getter(name="retentionPeriod")
    def retention_period(self) -> Optional[pulumi.Input[float]]:
        """
        The number of days to retain automated snapshots in the destination region after they are copied from the source region. Defaults to `7`.
        """
        return pulumi.get(self, "retention_period")

    @retention_period.setter
    def retention_period(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "retention_period", value)


@pulumi.input_type
class ParameterGroupParameterArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] name: The name of the Redshift parameter.
        :param pulumi.Input[str] value: The value of the Redshift parameter.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the Redshift parameter.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value of the Redshift parameter.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class SecurityGroupIngressArgs:
    def __init__(__self__, *,
                 cidr: Optional[pulumi.Input[str]] = None,
                 security_group_name: Optional[pulumi.Input[str]] = None,
                 security_group_owner_id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] cidr: The CIDR block to accept
        :param pulumi.Input[str] security_group_name: The name of the security group to authorize
        :param pulumi.Input[str] security_group_owner_id: The owner Id of the security group provided
               by `security_group_name`.
        """
        if cidr is not None:
            pulumi.set(__self__, "cidr", cidr)
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


