# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = ['MountTarget']


class MountTarget(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 file_system_id: Optional[pulumi.Input[str]] = None,
                 ip_address: Optional[pulumi.Input[str]] = None,
                 security_groups: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides an Elastic File System (EFS) mount target.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        foo = aws.ec2.Vpc("foo", cidr_block="10.0.0.0/16")
        alpha_subnet = aws.ec2.Subnet("alphaSubnet",
            vpc_id=foo.id,
            availability_zone="us-west-2a",
            cidr_block="10.0.1.0/24")
        alpha_mount_target = aws.efs.MountTarget("alphaMountTarget",
            file_system_id=aws_efs_file_system["foo"]["id"],
            subnet_id=alpha_subnet.id)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] file_system_id: The ID of the file system for which the mount target is intended.
        :param pulumi.Input[str] ip_address: The address (within the address range of the specified subnet) at
               which the file system may be mounted via the mount target.
        :param pulumi.Input[List[pulumi.Input[str]]] security_groups: A list of up to 5 VPC security group IDs (that must
               be for the same VPC as subnet specified) in effect for the mount target.
        :param pulumi.Input[str] subnet_id: The ID of the subnet to add the mount target in.
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

            if file_system_id is None:
                raise TypeError("Missing required property 'file_system_id'")
            __props__['file_system_id'] = file_system_id
            __props__['ip_address'] = ip_address
            __props__['security_groups'] = security_groups
            if subnet_id is None:
                raise TypeError("Missing required property 'subnet_id'")
            __props__['subnet_id'] = subnet_id
            __props__['availability_zone_id'] = None
            __props__['availability_zone_name'] = None
            __props__['dns_name'] = None
            __props__['file_system_arn'] = None
            __props__['mount_target_dns_name'] = None
            __props__['network_interface_id'] = None
            __props__['owner_id'] = None
        super(MountTarget, __self__).__init__(
            'aws:efs/mountTarget:MountTarget',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            availability_zone_id: Optional[pulumi.Input[str]] = None,
            availability_zone_name: Optional[pulumi.Input[str]] = None,
            dns_name: Optional[pulumi.Input[str]] = None,
            file_system_arn: Optional[pulumi.Input[str]] = None,
            file_system_id: Optional[pulumi.Input[str]] = None,
            ip_address: Optional[pulumi.Input[str]] = None,
            mount_target_dns_name: Optional[pulumi.Input[str]] = None,
            network_interface_id: Optional[pulumi.Input[str]] = None,
            owner_id: Optional[pulumi.Input[str]] = None,
            security_groups: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            subnet_id: Optional[pulumi.Input[str]] = None) -> 'MountTarget':
        """
        Get an existing MountTarget resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] availability_zone_id: The unique and consistent identifier of the Availability Zone (AZ) that the mount target resides in.
        :param pulumi.Input[str] availability_zone_name: The name of the Availability Zone (AZ) that the mount target resides in.
        :param pulumi.Input[str] dns_name: The DNS name for the EFS file system.
        :param pulumi.Input[str] file_system_arn: Amazon Resource Name of the file system.
        :param pulumi.Input[str] file_system_id: The ID of the file system for which the mount target is intended.
        :param pulumi.Input[str] ip_address: The address (within the address range of the specified subnet) at
               which the file system may be mounted via the mount target.
        :param pulumi.Input[str] mount_target_dns_name: The DNS name for the given subnet/AZ per [documented convention](http://docs.aws.amazon.com/efs/latest/ug/mounting-fs-mount-cmd-dns-name.html).
        :param pulumi.Input[str] network_interface_id: The ID of the network interface that Amazon EFS created when it created the mount target.
        :param pulumi.Input[str] owner_id: AWS account ID that owns the resource.
        :param pulumi.Input[List[pulumi.Input[str]]] security_groups: A list of up to 5 VPC security group IDs (that must
               be for the same VPC as subnet specified) in effect for the mount target.
        :param pulumi.Input[str] subnet_id: The ID of the subnet to add the mount target in.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["availability_zone_id"] = availability_zone_id
        __props__["availability_zone_name"] = availability_zone_name
        __props__["dns_name"] = dns_name
        __props__["file_system_arn"] = file_system_arn
        __props__["file_system_id"] = file_system_id
        __props__["ip_address"] = ip_address
        __props__["mount_target_dns_name"] = mount_target_dns_name
        __props__["network_interface_id"] = network_interface_id
        __props__["owner_id"] = owner_id
        __props__["security_groups"] = security_groups
        __props__["subnet_id"] = subnet_id
        return MountTarget(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="availabilityZoneId")
    def availability_zone_id(self) -> pulumi.Output[str]:
        """
        The unique and consistent identifier of the Availability Zone (AZ) that the mount target resides in.
        """
        return pulumi.get(self, "availability_zone_id")

    @property
    @pulumi.getter(name="availabilityZoneName")
    def availability_zone_name(self) -> pulumi.Output[str]:
        """
        The name of the Availability Zone (AZ) that the mount target resides in.
        """
        return pulumi.get(self, "availability_zone_name")

    @property
    @pulumi.getter(name="dnsName")
    def dns_name(self) -> pulumi.Output[str]:
        """
        The DNS name for the EFS file system.
        """
        return pulumi.get(self, "dns_name")

    @property
    @pulumi.getter(name="fileSystemArn")
    def file_system_arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name of the file system.
        """
        return pulumi.get(self, "file_system_arn")

    @property
    @pulumi.getter(name="fileSystemId")
    def file_system_id(self) -> pulumi.Output[str]:
        """
        The ID of the file system for which the mount target is intended.
        """
        return pulumi.get(self, "file_system_id")

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> pulumi.Output[str]:
        """
        The address (within the address range of the specified subnet) at
        which the file system may be mounted via the mount target.
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter(name="mountTargetDnsName")
    def mount_target_dns_name(self) -> pulumi.Output[str]:
        """
        The DNS name for the given subnet/AZ per [documented convention](http://docs.aws.amazon.com/efs/latest/ug/mounting-fs-mount-cmd-dns-name.html).
        """
        return pulumi.get(self, "mount_target_dns_name")

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> pulumi.Output[str]:
        """
        The ID of the network interface that Amazon EFS created when it created the mount target.
        """
        return pulumi.get(self, "network_interface_id")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> pulumi.Output[str]:
        """
        AWS account ID that owns the resource.
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter(name="securityGroups")
    def security_groups(self) -> pulumi.Output[List[str]]:
        """
        A list of up to 5 VPC security group IDs (that must
        be for the same VPC as subnet specified) in effect for the mount target.
        """
        return pulumi.get(self, "security_groups")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Output[str]:
        """
        The ID of the subnet to add the mount target in.
        """
        return pulumi.get(self, "subnet_id")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

