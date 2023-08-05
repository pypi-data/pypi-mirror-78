# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'GetGroupResult',
    'AwaitableGetGroupResult',
    'get_group',
]

@pulumi.output_type
class GetGroupResult:
    """
    A collection of values returned by getGroup.
    """
    def __init__(__self__, arn=None, availability_zones=None, default_cooldown=None, desired_capacity=None, health_check_grace_period=None, health_check_type=None, id=None, launch_configuration=None, load_balancers=None, max_size=None, min_size=None, name=None, new_instances_protected_from_scale_in=None, placement_group=None, service_linked_role_arn=None, status=None, target_group_arns=None, termination_policies=None, vpc_zone_identifier=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if availability_zones and not isinstance(availability_zones, list):
            raise TypeError("Expected argument 'availability_zones' to be a list")
        pulumi.set(__self__, "availability_zones", availability_zones)
        if default_cooldown and not isinstance(default_cooldown, float):
            raise TypeError("Expected argument 'default_cooldown' to be a float")
        pulumi.set(__self__, "default_cooldown", default_cooldown)
        if desired_capacity and not isinstance(desired_capacity, float):
            raise TypeError("Expected argument 'desired_capacity' to be a float")
        pulumi.set(__self__, "desired_capacity", desired_capacity)
        if health_check_grace_period and not isinstance(health_check_grace_period, float):
            raise TypeError("Expected argument 'health_check_grace_period' to be a float")
        pulumi.set(__self__, "health_check_grace_period", health_check_grace_period)
        if health_check_type and not isinstance(health_check_type, str):
            raise TypeError("Expected argument 'health_check_type' to be a str")
        pulumi.set(__self__, "health_check_type", health_check_type)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if launch_configuration and not isinstance(launch_configuration, str):
            raise TypeError("Expected argument 'launch_configuration' to be a str")
        pulumi.set(__self__, "launch_configuration", launch_configuration)
        if load_balancers and not isinstance(load_balancers, list):
            raise TypeError("Expected argument 'load_balancers' to be a list")
        pulumi.set(__self__, "load_balancers", load_balancers)
        if max_size and not isinstance(max_size, float):
            raise TypeError("Expected argument 'max_size' to be a float")
        pulumi.set(__self__, "max_size", max_size)
        if min_size and not isinstance(min_size, float):
            raise TypeError("Expected argument 'min_size' to be a float")
        pulumi.set(__self__, "min_size", min_size)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if new_instances_protected_from_scale_in and not isinstance(new_instances_protected_from_scale_in, bool):
            raise TypeError("Expected argument 'new_instances_protected_from_scale_in' to be a bool")
        pulumi.set(__self__, "new_instances_protected_from_scale_in", new_instances_protected_from_scale_in)
        if placement_group and not isinstance(placement_group, str):
            raise TypeError("Expected argument 'placement_group' to be a str")
        pulumi.set(__self__, "placement_group", placement_group)
        if service_linked_role_arn and not isinstance(service_linked_role_arn, str):
            raise TypeError("Expected argument 'service_linked_role_arn' to be a str")
        pulumi.set(__self__, "service_linked_role_arn", service_linked_role_arn)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if target_group_arns and not isinstance(target_group_arns, list):
            raise TypeError("Expected argument 'target_group_arns' to be a list")
        pulumi.set(__self__, "target_group_arns", target_group_arns)
        if termination_policies and not isinstance(termination_policies, list):
            raise TypeError("Expected argument 'termination_policies' to be a list")
        pulumi.set(__self__, "termination_policies", termination_policies)
        if vpc_zone_identifier and not isinstance(vpc_zone_identifier, str):
            raise TypeError("Expected argument 'vpc_zone_identifier' to be a str")
        pulumi.set(__self__, "vpc_zone_identifier", vpc_zone_identifier)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of the Auto Scaling group.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="availabilityZones")
    def availability_zones(self) -> List[str]:
        """
        One or more Availability Zones for the group.
        """
        return pulumi.get(self, "availability_zones")

    @property
    @pulumi.getter(name="defaultCooldown")
    def default_cooldown(self) -> float:
        return pulumi.get(self, "default_cooldown")

    @property
    @pulumi.getter(name="desiredCapacity")
    def desired_capacity(self) -> float:
        """
        The desired size of the group.
        """
        return pulumi.get(self, "desired_capacity")

    @property
    @pulumi.getter(name="healthCheckGracePeriod")
    def health_check_grace_period(self) -> float:
        """
        The amount of time, in seconds, that Amazon EC2 Auto Scaling waits before checking the health status of an EC2 instance that has come into service.
        """
        return pulumi.get(self, "health_check_grace_period")

    @property
    @pulumi.getter(name="healthCheckType")
    def health_check_type(self) -> str:
        """
        The service to use for the health checks. The valid values are EC2 and ELB.
        """
        return pulumi.get(self, "health_check_type")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="launchConfiguration")
    def launch_configuration(self) -> str:
        """
        The name of the associated launch configuration.
        """
        return pulumi.get(self, "launch_configuration")

    @property
    @pulumi.getter(name="loadBalancers")
    def load_balancers(self) -> List[str]:
        """
        One or more load balancers associated with the group.
        """
        return pulumi.get(self, "load_balancers")

    @property
    @pulumi.getter(name="maxSize")
    def max_size(self) -> float:
        """
        The maximum size of the group.
        """
        return pulumi.get(self, "max_size")

    @property
    @pulumi.getter(name="minSize")
    def min_size(self) -> float:
        """
        The minimum size of the group.
        """
        return pulumi.get(self, "min_size")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the Auto Scaling group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="newInstancesProtectedFromScaleIn")
    def new_instances_protected_from_scale_in(self) -> bool:
        return pulumi.get(self, "new_instances_protected_from_scale_in")

    @property
    @pulumi.getter(name="placementGroup")
    def placement_group(self) -> str:
        """
        The name of the placement group into which to launch your instances, if any. For more information, see Placement Groups (http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html) in the Amazon Elastic Compute Cloud User Guide.
        """
        return pulumi.get(self, "placement_group")

    @property
    @pulumi.getter(name="serviceLinkedRoleArn")
    def service_linked_role_arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of the service-linked role that the Auto Scaling group uses to call other AWS services on your behalf.
        """
        return pulumi.get(self, "service_linked_role_arn")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The current state of the group when DeleteAutoScalingGroup is in progress.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="targetGroupArns")
    def target_group_arns(self) -> List[str]:
        """
        The Amazon Resource Names (ARN) of the target groups for your load balancer.
        """
        return pulumi.get(self, "target_group_arns")

    @property
    @pulumi.getter(name="terminationPolicies")
    def termination_policies(self) -> List[str]:
        """
        The termination policies for the group.
        """
        return pulumi.get(self, "termination_policies")

    @property
    @pulumi.getter(name="vpcZoneIdentifier")
    def vpc_zone_identifier(self) -> str:
        """
        VPC ID for the group.
        """
        return pulumi.get(self, "vpc_zone_identifier")


class AwaitableGetGroupResult(GetGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGroupResult(
            arn=self.arn,
            availability_zones=self.availability_zones,
            default_cooldown=self.default_cooldown,
            desired_capacity=self.desired_capacity,
            health_check_grace_period=self.health_check_grace_period,
            health_check_type=self.health_check_type,
            id=self.id,
            launch_configuration=self.launch_configuration,
            load_balancers=self.load_balancers,
            max_size=self.max_size,
            min_size=self.min_size,
            name=self.name,
            new_instances_protected_from_scale_in=self.new_instances_protected_from_scale_in,
            placement_group=self.placement_group,
            service_linked_role_arn=self.service_linked_role_arn,
            status=self.status,
            target_group_arns=self.target_group_arns,
            termination_policies=self.termination_policies,
            vpc_zone_identifier=self.vpc_zone_identifier)


def get_group(name: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGroupResult:
    """
    Use this data source to get information on an existing autoscaling group.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    foo = aws.autoscaling.get_group(name="foo")
    ```


    :param str name: Specify the exact name of the desired autoscaling group.
    """
    __args__ = dict()
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:autoscaling/getGroup:getGroup', __args__, opts=opts, typ=GetGroupResult).value

    return AwaitableGetGroupResult(
        arn=__ret__.arn,
        availability_zones=__ret__.availability_zones,
        default_cooldown=__ret__.default_cooldown,
        desired_capacity=__ret__.desired_capacity,
        health_check_grace_period=__ret__.health_check_grace_period,
        health_check_type=__ret__.health_check_type,
        id=__ret__.id,
        launch_configuration=__ret__.launch_configuration,
        load_balancers=__ret__.load_balancers,
        max_size=__ret__.max_size,
        min_size=__ret__.min_size,
        name=__ret__.name,
        new_instances_protected_from_scale_in=__ret__.new_instances_protected_from_scale_in,
        placement_group=__ret__.placement_group,
        service_linked_role_arn=__ret__.service_linked_role_arn,
        status=__ret__.status,
        target_group_arns=__ret__.target_group_arns,
        termination_policies=__ret__.termination_policies,
        vpc_zone_identifier=__ret__.vpc_zone_identifier)
