# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'GroupInitialLifecycleHookArgs',
    'GroupLaunchTemplateArgs',
    'GroupMixedInstancesPolicyArgs',
    'GroupMixedInstancesPolicyInstancesDistributionArgs',
    'GroupMixedInstancesPolicyLaunchTemplateArgs',
    'GroupMixedInstancesPolicyLaunchTemplateLaunchTemplateSpecificationArgs',
    'GroupMixedInstancesPolicyLaunchTemplateOverrideArgs',
    'GroupTagArgs',
    'PolicyStepAdjustmentArgs',
    'PolicyTargetTrackingConfigurationArgs',
    'PolicyTargetTrackingConfigurationCustomizedMetricSpecificationArgs',
    'PolicyTargetTrackingConfigurationCustomizedMetricSpecificationMetricDimensionArgs',
    'PolicyTargetTrackingConfigurationPredefinedMetricSpecificationArgs',
]

@pulumi.input_type
class GroupInitialLifecycleHookArgs:
    def __init__(__self__, *,
                 lifecycle_transition: pulumi.Input[str],
                 name: pulumi.Input[str],
                 default_result: Optional[pulumi.Input[str]] = None,
                 heartbeat_timeout: Optional[pulumi.Input[float]] = None,
                 notification_metadata: Optional[pulumi.Input[str]] = None,
                 notification_target_arn: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] name: The name of the auto scaling group. By default generated by this provider.
        """
        pulumi.set(__self__, "lifecycle_transition", lifecycle_transition)
        pulumi.set(__self__, "name", name)
        if default_result is not None:
            pulumi.set(__self__, "default_result", default_result)
        if heartbeat_timeout is not None:
            pulumi.set(__self__, "heartbeat_timeout", heartbeat_timeout)
        if notification_metadata is not None:
            pulumi.set(__self__, "notification_metadata", notification_metadata)
        if notification_target_arn is not None:
            pulumi.set(__self__, "notification_target_arn", notification_target_arn)
        if role_arn is not None:
            pulumi.set(__self__, "role_arn", role_arn)

    @property
    @pulumi.getter(name="lifecycleTransition")
    def lifecycle_transition(self) -> pulumi.Input[str]:
        return pulumi.get(self, "lifecycle_transition")

    @lifecycle_transition.setter
    def lifecycle_transition(self, value: pulumi.Input[str]):
        pulumi.set(self, "lifecycle_transition", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the auto scaling group. By default generated by this provider.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="defaultResult")
    def default_result(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "default_result")

    @default_result.setter
    def default_result(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_result", value)

    @property
    @pulumi.getter(name="heartbeatTimeout")
    def heartbeat_timeout(self) -> Optional[pulumi.Input[float]]:
        return pulumi.get(self, "heartbeat_timeout")

    @heartbeat_timeout.setter
    def heartbeat_timeout(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "heartbeat_timeout", value)

    @property
    @pulumi.getter(name="notificationMetadata")
    def notification_metadata(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "notification_metadata")

    @notification_metadata.setter
    def notification_metadata(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "notification_metadata", value)

    @property
    @pulumi.getter(name="notificationTargetArn")
    def notification_target_arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "notification_target_arn")

    @notification_target_arn.setter
    def notification_target_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "notification_target_arn", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_arn", value)


@pulumi.input_type
class GroupLaunchTemplateArgs:
    def __init__(__self__, *,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] id: The ID of the launch template. Conflicts with `name`.
        :param pulumi.Input[str] name: The name of the auto scaling group. By default generated by this provider.
        :param pulumi.Input[str] version: Template version. Can be version number, `$Latest`, or `$Default`. (Default: `$Default`).
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the launch template. Conflicts with `name`.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the auto scaling group. By default generated by this provider.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        Template version. Can be version number, `$Latest`, or `$Default`. (Default: `$Default`).
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class GroupMixedInstancesPolicyArgs:
    def __init__(__self__, *,
                 launch_template: pulumi.Input['GroupMixedInstancesPolicyLaunchTemplateArgs'],
                 instances_distribution: Optional[pulumi.Input['GroupMixedInstancesPolicyInstancesDistributionArgs']] = None):
        """
        :param pulumi.Input['GroupMixedInstancesPolicyLaunchTemplateArgs'] launch_template: Nested argument containing launch template settings along with the overrides to specify multiple instance types and weights. Defined below.
        :param pulumi.Input['GroupMixedInstancesPolicyInstancesDistributionArgs'] instances_distribution: Nested argument containing settings on how to mix on-demand and Spot instances in the Auto Scaling group. Defined below.
        """
        pulumi.set(__self__, "launch_template", launch_template)
        if instances_distribution is not None:
            pulumi.set(__self__, "instances_distribution", instances_distribution)

    @property
    @pulumi.getter(name="launchTemplate")
    def launch_template(self) -> pulumi.Input['GroupMixedInstancesPolicyLaunchTemplateArgs']:
        """
        Nested argument containing launch template settings along with the overrides to specify multiple instance types and weights. Defined below.
        """
        return pulumi.get(self, "launch_template")

    @launch_template.setter
    def launch_template(self, value: pulumi.Input['GroupMixedInstancesPolicyLaunchTemplateArgs']):
        pulumi.set(self, "launch_template", value)

    @property
    @pulumi.getter(name="instancesDistribution")
    def instances_distribution(self) -> Optional[pulumi.Input['GroupMixedInstancesPolicyInstancesDistributionArgs']]:
        """
        Nested argument containing settings on how to mix on-demand and Spot instances in the Auto Scaling group. Defined below.
        """
        return pulumi.get(self, "instances_distribution")

    @instances_distribution.setter
    def instances_distribution(self, value: Optional[pulumi.Input['GroupMixedInstancesPolicyInstancesDistributionArgs']]):
        pulumi.set(self, "instances_distribution", value)


@pulumi.input_type
class GroupMixedInstancesPolicyInstancesDistributionArgs:
    def __init__(__self__, *,
                 on_demand_allocation_strategy: Optional[pulumi.Input[str]] = None,
                 on_demand_base_capacity: Optional[pulumi.Input[float]] = None,
                 on_demand_percentage_above_base_capacity: Optional[pulumi.Input[float]] = None,
                 spot_allocation_strategy: Optional[pulumi.Input[str]] = None,
                 spot_instance_pools: Optional[pulumi.Input[float]] = None,
                 spot_max_price: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] on_demand_allocation_strategy: Strategy to use when launching on-demand instances. Valid values: `prioritized`. Default: `prioritized`.
        :param pulumi.Input[float] on_demand_base_capacity: Absolute minimum amount of desired capacity that must be fulfilled by on-demand instances. Default: `0`.
        :param pulumi.Input[float] on_demand_percentage_above_base_capacity: Percentage split between on-demand and Spot instances above the base on-demand capacity. Default: `100`.
        :param pulumi.Input[str] spot_allocation_strategy: How to allocate capacity across the Spot pools. Valid values: `lowest-price`, `capacity-optimized`. Default: `lowest-price`.
        :param pulumi.Input[float] spot_instance_pools: Number of Spot pools per availability zone to allocate capacity. EC2 Auto Scaling selects the cheapest Spot pools and evenly allocates Spot capacity across the number of Spot pools that you specify. Default: `2`.
        :param pulumi.Input[str] spot_max_price: Maximum price per unit hour that the user is willing to pay for the Spot instances. Default: an empty string which means the on-demand price.
        """
        if on_demand_allocation_strategy is not None:
            pulumi.set(__self__, "on_demand_allocation_strategy", on_demand_allocation_strategy)
        if on_demand_base_capacity is not None:
            pulumi.set(__self__, "on_demand_base_capacity", on_demand_base_capacity)
        if on_demand_percentage_above_base_capacity is not None:
            pulumi.set(__self__, "on_demand_percentage_above_base_capacity", on_demand_percentage_above_base_capacity)
        if spot_allocation_strategy is not None:
            pulumi.set(__self__, "spot_allocation_strategy", spot_allocation_strategy)
        if spot_instance_pools is not None:
            pulumi.set(__self__, "spot_instance_pools", spot_instance_pools)
        if spot_max_price is not None:
            pulumi.set(__self__, "spot_max_price", spot_max_price)

    @property
    @pulumi.getter(name="onDemandAllocationStrategy")
    def on_demand_allocation_strategy(self) -> Optional[pulumi.Input[str]]:
        """
        Strategy to use when launching on-demand instances. Valid values: `prioritized`. Default: `prioritized`.
        """
        return pulumi.get(self, "on_demand_allocation_strategy")

    @on_demand_allocation_strategy.setter
    def on_demand_allocation_strategy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "on_demand_allocation_strategy", value)

    @property
    @pulumi.getter(name="onDemandBaseCapacity")
    def on_demand_base_capacity(self) -> Optional[pulumi.Input[float]]:
        """
        Absolute minimum amount of desired capacity that must be fulfilled by on-demand instances. Default: `0`.
        """
        return pulumi.get(self, "on_demand_base_capacity")

    @on_demand_base_capacity.setter
    def on_demand_base_capacity(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "on_demand_base_capacity", value)

    @property
    @pulumi.getter(name="onDemandPercentageAboveBaseCapacity")
    def on_demand_percentage_above_base_capacity(self) -> Optional[pulumi.Input[float]]:
        """
        Percentage split between on-demand and Spot instances above the base on-demand capacity. Default: `100`.
        """
        return pulumi.get(self, "on_demand_percentage_above_base_capacity")

    @on_demand_percentage_above_base_capacity.setter
    def on_demand_percentage_above_base_capacity(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "on_demand_percentage_above_base_capacity", value)

    @property
    @pulumi.getter(name="spotAllocationStrategy")
    def spot_allocation_strategy(self) -> Optional[pulumi.Input[str]]:
        """
        How to allocate capacity across the Spot pools. Valid values: `lowest-price`, `capacity-optimized`. Default: `lowest-price`.
        """
        return pulumi.get(self, "spot_allocation_strategy")

    @spot_allocation_strategy.setter
    def spot_allocation_strategy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "spot_allocation_strategy", value)

    @property
    @pulumi.getter(name="spotInstancePools")
    def spot_instance_pools(self) -> Optional[pulumi.Input[float]]:
        """
        Number of Spot pools per availability zone to allocate capacity. EC2 Auto Scaling selects the cheapest Spot pools and evenly allocates Spot capacity across the number of Spot pools that you specify. Default: `2`.
        """
        return pulumi.get(self, "spot_instance_pools")

    @spot_instance_pools.setter
    def spot_instance_pools(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "spot_instance_pools", value)

    @property
    @pulumi.getter(name="spotMaxPrice")
    def spot_max_price(self) -> Optional[pulumi.Input[str]]:
        """
        Maximum price per unit hour that the user is willing to pay for the Spot instances. Default: an empty string which means the on-demand price.
        """
        return pulumi.get(self, "spot_max_price")

    @spot_max_price.setter
    def spot_max_price(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "spot_max_price", value)


@pulumi.input_type
class GroupMixedInstancesPolicyLaunchTemplateArgs:
    def __init__(__self__, *,
                 launch_template_specification: pulumi.Input['GroupMixedInstancesPolicyLaunchTemplateLaunchTemplateSpecificationArgs'],
                 overrides: Optional[pulumi.Input[List[pulumi.Input['GroupMixedInstancesPolicyLaunchTemplateOverrideArgs']]]] = None):
        """
        :param pulumi.Input['GroupMixedInstancesPolicyLaunchTemplateLaunchTemplateSpecificationArgs'] launch_template_specification: Nested argument defines the Launch Template. Defined below.
        :param pulumi.Input[List[pulumi.Input['GroupMixedInstancesPolicyLaunchTemplateOverrideArgs']]] overrides: List of nested arguments provides the ability to specify multiple instance types. This will override the same parameter in the launch template. For on-demand instances, Auto Scaling considers the order of preference of instance types to launch based on the order specified in the overrides list. Defined below.
        """
        pulumi.set(__self__, "launch_template_specification", launch_template_specification)
        if overrides is not None:
            pulumi.set(__self__, "overrides", overrides)

    @property
    @pulumi.getter(name="launchTemplateSpecification")
    def launch_template_specification(self) -> pulumi.Input['GroupMixedInstancesPolicyLaunchTemplateLaunchTemplateSpecificationArgs']:
        """
        Nested argument defines the Launch Template. Defined below.
        """
        return pulumi.get(self, "launch_template_specification")

    @launch_template_specification.setter
    def launch_template_specification(self, value: pulumi.Input['GroupMixedInstancesPolicyLaunchTemplateLaunchTemplateSpecificationArgs']):
        pulumi.set(self, "launch_template_specification", value)

    @property
    @pulumi.getter
    def overrides(self) -> Optional[pulumi.Input[List[pulumi.Input['GroupMixedInstancesPolicyLaunchTemplateOverrideArgs']]]]:
        """
        List of nested arguments provides the ability to specify multiple instance types. This will override the same parameter in the launch template. For on-demand instances, Auto Scaling considers the order of preference of instance types to launch based on the order specified in the overrides list. Defined below.
        """
        return pulumi.get(self, "overrides")

    @overrides.setter
    def overrides(self, value: Optional[pulumi.Input[List[pulumi.Input['GroupMixedInstancesPolicyLaunchTemplateOverrideArgs']]]]):
        pulumi.set(self, "overrides", value)


@pulumi.input_type
class GroupMixedInstancesPolicyLaunchTemplateLaunchTemplateSpecificationArgs:
    def __init__(__self__, *,
                 launch_template_id: Optional[pulumi.Input[str]] = None,
                 launch_template_name: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] launch_template_id: The ID of the launch template. Conflicts with `launch_template_name`.
        :param pulumi.Input[str] launch_template_name: The name of the launch template. Conflicts with `launch_template_id`.
        :param pulumi.Input[str] version: Template version. Can be version number, `$Latest`, or `$Default`. (Default: `$Default`).
        """
        if launch_template_id is not None:
            pulumi.set(__self__, "launch_template_id", launch_template_id)
        if launch_template_name is not None:
            pulumi.set(__self__, "launch_template_name", launch_template_name)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="launchTemplateId")
    def launch_template_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the launch template. Conflicts with `launch_template_name`.
        """
        return pulumi.get(self, "launch_template_id")

    @launch_template_id.setter
    def launch_template_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "launch_template_id", value)

    @property
    @pulumi.getter(name="launchTemplateName")
    def launch_template_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the launch template. Conflicts with `launch_template_id`.
        """
        return pulumi.get(self, "launch_template_name")

    @launch_template_name.setter
    def launch_template_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "launch_template_name", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        Template version. Can be version number, `$Latest`, or `$Default`. (Default: `$Default`).
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class GroupMixedInstancesPolicyLaunchTemplateOverrideArgs:
    def __init__(__self__, *,
                 instance_type: Optional[pulumi.Input[str]] = None,
                 weighted_capacity: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] instance_type: Override the instance type in the Launch Template.
        :param pulumi.Input[str] weighted_capacity: The number of capacity units, which gives the instance type a proportional weight to other instance types.
        """
        if instance_type is not None:
            pulumi.set(__self__, "instance_type", instance_type)
        if weighted_capacity is not None:
            pulumi.set(__self__, "weighted_capacity", weighted_capacity)

    @property
    @pulumi.getter(name="instanceType")
    def instance_type(self) -> Optional[pulumi.Input[str]]:
        """
        Override the instance type in the Launch Template.
        """
        return pulumi.get(self, "instance_type")

    @instance_type.setter
    def instance_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_type", value)

    @property
    @pulumi.getter(name="weightedCapacity")
    def weighted_capacity(self) -> Optional[pulumi.Input[str]]:
        """
        The number of capacity units, which gives the instance type a proportional weight to other instance types.
        """
        return pulumi.get(self, "weighted_capacity")

    @weighted_capacity.setter
    def weighted_capacity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "weighted_capacity", value)


@pulumi.input_type
class GroupTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 propagate_at_launch: pulumi.Input[bool],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] key: Key
        :param pulumi.Input[bool] propagate_at_launch: Enables propagation of the tag to
               Amazon EC2 instances launched via this ASG
        :param pulumi.Input[str] value: Value
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "propagate_at_launch", propagate_at_launch)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        Key
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter(name="propagateAtLaunch")
    def propagate_at_launch(self) -> pulumi.Input[bool]:
        """
        Enables propagation of the tag to
        Amazon EC2 instances launched via this ASG
        """
        return pulumi.get(self, "propagate_at_launch")

    @propagate_at_launch.setter
    def propagate_at_launch(self, value: pulumi.Input[bool]):
        pulumi.set(self, "propagate_at_launch", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        Value
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class PolicyStepAdjustmentArgs:
    def __init__(__self__, *,
                 scaling_adjustment: pulumi.Input[float],
                 metric_interval_lower_bound: Optional[pulumi.Input[str]] = None,
                 metric_interval_upper_bound: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[float] scaling_adjustment: The number of members by which to
               scale, when the adjustment bounds are breached. A positive value scales
               up. A negative value scales down.
        :param pulumi.Input[str] metric_interval_lower_bound: The lower bound for the
               difference between the alarm threshold and the CloudWatch metric.
               Without a value, AWS will treat this bound as infinity.
        :param pulumi.Input[str] metric_interval_upper_bound: The upper bound for the
               difference between the alarm threshold and the CloudWatch metric.
               Without a value, AWS will treat this bound as infinity. The upper bound
               must be greater than the lower bound.
        """
        pulumi.set(__self__, "scaling_adjustment", scaling_adjustment)
        if metric_interval_lower_bound is not None:
            pulumi.set(__self__, "metric_interval_lower_bound", metric_interval_lower_bound)
        if metric_interval_upper_bound is not None:
            pulumi.set(__self__, "metric_interval_upper_bound", metric_interval_upper_bound)

    @property
    @pulumi.getter(name="scalingAdjustment")
    def scaling_adjustment(self) -> pulumi.Input[float]:
        """
        The number of members by which to
        scale, when the adjustment bounds are breached. A positive value scales
        up. A negative value scales down.
        """
        return pulumi.get(self, "scaling_adjustment")

    @scaling_adjustment.setter
    def scaling_adjustment(self, value: pulumi.Input[float]):
        pulumi.set(self, "scaling_adjustment", value)

    @property
    @pulumi.getter(name="metricIntervalLowerBound")
    def metric_interval_lower_bound(self) -> Optional[pulumi.Input[str]]:
        """
        The lower bound for the
        difference between the alarm threshold and the CloudWatch metric.
        Without a value, AWS will treat this bound as infinity.
        """
        return pulumi.get(self, "metric_interval_lower_bound")

    @metric_interval_lower_bound.setter
    def metric_interval_lower_bound(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metric_interval_lower_bound", value)

    @property
    @pulumi.getter(name="metricIntervalUpperBound")
    def metric_interval_upper_bound(self) -> Optional[pulumi.Input[str]]:
        """
        The upper bound for the
        difference between the alarm threshold and the CloudWatch metric.
        Without a value, AWS will treat this bound as infinity. The upper bound
        must be greater than the lower bound.
        """
        return pulumi.get(self, "metric_interval_upper_bound")

    @metric_interval_upper_bound.setter
    def metric_interval_upper_bound(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metric_interval_upper_bound", value)


@pulumi.input_type
class PolicyTargetTrackingConfigurationArgs:
    def __init__(__self__, *,
                 target_value: pulumi.Input[float],
                 customized_metric_specification: Optional[pulumi.Input['PolicyTargetTrackingConfigurationCustomizedMetricSpecificationArgs']] = None,
                 disable_scale_in: Optional[pulumi.Input[bool]] = None,
                 predefined_metric_specification: Optional[pulumi.Input['PolicyTargetTrackingConfigurationPredefinedMetricSpecificationArgs']] = None):
        """
        :param pulumi.Input[float] target_value: The target value for the metric.
        :param pulumi.Input['PolicyTargetTrackingConfigurationCustomizedMetricSpecificationArgs'] customized_metric_specification: A customized metric. Conflicts with `predefined_metric_specification`.
        :param pulumi.Input[bool] disable_scale_in: Indicates whether scale in by the target tracking policy is disabled.
        :param pulumi.Input['PolicyTargetTrackingConfigurationPredefinedMetricSpecificationArgs'] predefined_metric_specification: A predefined metric. Conflicts with `customized_metric_specification`.
        """
        pulumi.set(__self__, "target_value", target_value)
        if customized_metric_specification is not None:
            pulumi.set(__self__, "customized_metric_specification", customized_metric_specification)
        if disable_scale_in is not None:
            pulumi.set(__self__, "disable_scale_in", disable_scale_in)
        if predefined_metric_specification is not None:
            pulumi.set(__self__, "predefined_metric_specification", predefined_metric_specification)

    @property
    @pulumi.getter(name="targetValue")
    def target_value(self) -> pulumi.Input[float]:
        """
        The target value for the metric.
        """
        return pulumi.get(self, "target_value")

    @target_value.setter
    def target_value(self, value: pulumi.Input[float]):
        pulumi.set(self, "target_value", value)

    @property
    @pulumi.getter(name="customizedMetricSpecification")
    def customized_metric_specification(self) -> Optional[pulumi.Input['PolicyTargetTrackingConfigurationCustomizedMetricSpecificationArgs']]:
        """
        A customized metric. Conflicts with `predefined_metric_specification`.
        """
        return pulumi.get(self, "customized_metric_specification")

    @customized_metric_specification.setter
    def customized_metric_specification(self, value: Optional[pulumi.Input['PolicyTargetTrackingConfigurationCustomizedMetricSpecificationArgs']]):
        pulumi.set(self, "customized_metric_specification", value)

    @property
    @pulumi.getter(name="disableScaleIn")
    def disable_scale_in(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether scale in by the target tracking policy is disabled.
        """
        return pulumi.get(self, "disable_scale_in")

    @disable_scale_in.setter
    def disable_scale_in(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disable_scale_in", value)

    @property
    @pulumi.getter(name="predefinedMetricSpecification")
    def predefined_metric_specification(self) -> Optional[pulumi.Input['PolicyTargetTrackingConfigurationPredefinedMetricSpecificationArgs']]:
        """
        A predefined metric. Conflicts with `customized_metric_specification`.
        """
        return pulumi.get(self, "predefined_metric_specification")

    @predefined_metric_specification.setter
    def predefined_metric_specification(self, value: Optional[pulumi.Input['PolicyTargetTrackingConfigurationPredefinedMetricSpecificationArgs']]):
        pulumi.set(self, "predefined_metric_specification", value)


@pulumi.input_type
class PolicyTargetTrackingConfigurationCustomizedMetricSpecificationArgs:
    def __init__(__self__, *,
                 metric_name: pulumi.Input[str],
                 namespace: pulumi.Input[str],
                 statistic: pulumi.Input[str],
                 metric_dimensions: Optional[pulumi.Input[List[pulumi.Input['PolicyTargetTrackingConfigurationCustomizedMetricSpecificationMetricDimensionArgs']]]] = None,
                 unit: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] metric_name: The name of the metric.
        :param pulumi.Input[str] namespace: The namespace of the metric.
        :param pulumi.Input[str] statistic: The statistic of the metric.
        :param pulumi.Input[List[pulumi.Input['PolicyTargetTrackingConfigurationCustomizedMetricSpecificationMetricDimensionArgs']]] metric_dimensions: The dimensions of the metric.
        :param pulumi.Input[str] unit: The unit of the metric.
        """
        pulumi.set(__self__, "metric_name", metric_name)
        pulumi.set(__self__, "namespace", namespace)
        pulumi.set(__self__, "statistic", statistic)
        if metric_dimensions is not None:
            pulumi.set(__self__, "metric_dimensions", metric_dimensions)
        if unit is not None:
            pulumi.set(__self__, "unit", unit)

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> pulumi.Input[str]:
        """
        The name of the metric.
        """
        return pulumi.get(self, "metric_name")

    @metric_name.setter
    def metric_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "metric_name", value)

    @property
    @pulumi.getter
    def namespace(self) -> pulumi.Input[str]:
        """
        The namespace of the metric.
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: pulumi.Input[str]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter
    def statistic(self) -> pulumi.Input[str]:
        """
        The statistic of the metric.
        """
        return pulumi.get(self, "statistic")

    @statistic.setter
    def statistic(self, value: pulumi.Input[str]):
        pulumi.set(self, "statistic", value)

    @property
    @pulumi.getter(name="metricDimensions")
    def metric_dimensions(self) -> Optional[pulumi.Input[List[pulumi.Input['PolicyTargetTrackingConfigurationCustomizedMetricSpecificationMetricDimensionArgs']]]]:
        """
        The dimensions of the metric.
        """
        return pulumi.get(self, "metric_dimensions")

    @metric_dimensions.setter
    def metric_dimensions(self, value: Optional[pulumi.Input[List[pulumi.Input['PolicyTargetTrackingConfigurationCustomizedMetricSpecificationMetricDimensionArgs']]]]):
        pulumi.set(self, "metric_dimensions", value)

    @property
    @pulumi.getter
    def unit(self) -> Optional[pulumi.Input[str]]:
        """
        The unit of the metric.
        """
        return pulumi.get(self, "unit")

    @unit.setter
    def unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "unit", value)


@pulumi.input_type
class PolicyTargetTrackingConfigurationCustomizedMetricSpecificationMetricDimensionArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] name: The name of the dimension.
        :param pulumi.Input[str] value: The value of the dimension.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the dimension.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value of the dimension.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class PolicyTargetTrackingConfigurationPredefinedMetricSpecificationArgs:
    def __init__(__self__, *,
                 predefined_metric_type: pulumi.Input[str],
                 resource_label: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] predefined_metric_type: The metric type.
        :param pulumi.Input[str] resource_label: Identifies the resource associated with the metric type.
        """
        pulumi.set(__self__, "predefined_metric_type", predefined_metric_type)
        if resource_label is not None:
            pulumi.set(__self__, "resource_label", resource_label)

    @property
    @pulumi.getter(name="predefinedMetricType")
    def predefined_metric_type(self) -> pulumi.Input[str]:
        """
        The metric type.
        """
        return pulumi.get(self, "predefined_metric_type")

    @predefined_metric_type.setter
    def predefined_metric_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "predefined_metric_type", value)

    @property
    @pulumi.getter(name="resourceLabel")
    def resource_label(self) -> Optional[pulumi.Input[str]]:
        """
        Identifies the resource associated with the metric type.
        """
        return pulumi.get(self, "resource_label")

    @resource_label.setter
    def resource_label(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_label", value)


