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

__all__ = ['Policy']


class Policy(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 adjustment_type: Optional[pulumi.Input[str]] = None,
                 autoscaling_group_name: Optional[pulumi.Input[str]] = None,
                 cooldown: Optional[pulumi.Input[float]] = None,
                 estimated_instance_warmup: Optional[pulumi.Input[float]] = None,
                 metric_aggregation_type: Optional[pulumi.Input[str]] = None,
                 min_adjustment_magnitude: Optional[pulumi.Input[float]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_type: Optional[pulumi.Input[str]] = None,
                 scaling_adjustment: Optional[pulumi.Input[float]] = None,
                 step_adjustments: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['PolicyStepAdjustmentArgs']]]]] = None,
                 target_tracking_configuration: Optional[pulumi.Input[pulumi.InputType['PolicyTargetTrackingConfigurationArgs']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides an AutoScaling Scaling Policy resource.

        > **NOTE:** You may want to omit `desired_capacity` attribute from attached `autoscaling.Group`
        when using autoscaling policies. It's good practice to pick either
        [manual](https://docs.aws.amazon.com/AutoScaling/latest/DeveloperGuide/as-manual-scaling.html)
        or [dynamic](https://docs.aws.amazon.com/AutoScaling/latest/DeveloperGuide/as-scale-based-on-demand.html)
        (policy-based) scaling.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        bar = aws.autoscaling.Group("bar",
            availability_zones=["us-east-1a"],
            max_size=5,
            min_size=2,
            health_check_grace_period=300,
            health_check_type="ELB",
            force_delete=True,
            launch_configuration=aws_launch_configuration["foo"]["name"])
        bat = aws.autoscaling.Policy("bat",
            scaling_adjustment=4,
            adjustment_type="ChangeInCapacity",
            cooldown=300,
            autoscaling_group_name=bar.name)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] adjustment_type: Specifies whether the adjustment is an absolute number or a percentage of the current capacity. Valid values are `ChangeInCapacity`, `ExactCapacity`, and `PercentChangeInCapacity`.
        :param pulumi.Input[str] autoscaling_group_name: The name of the autoscaling group.
        :param pulumi.Input[float] cooldown: The amount of time, in seconds, after a scaling activity completes and before the next scaling activity can start.
        :param pulumi.Input[float] estimated_instance_warmup: The estimated time, in seconds, until a newly launched instance will contribute CloudWatch metrics. Without a value, AWS will default to the group's specified cooldown period.
        :param pulumi.Input[str] metric_aggregation_type: The aggregation type for the policy's metrics. Valid values are "Minimum", "Maximum", and "Average". Without a value, AWS will treat the aggregation type as "Average".
        :param pulumi.Input[str] name: The name of the dimension.
        :param pulumi.Input[str] policy_type: The policy type, either "SimpleScaling", "StepScaling" or "TargetTrackingScaling". If this value isn't provided, AWS will default to "SimpleScaling."
        :param pulumi.Input[float] scaling_adjustment: The number of members by which to
               scale, when the adjustment bounds are breached. A positive value scales
               up. A negative value scales down.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['PolicyStepAdjustmentArgs']]]] step_adjustments: A set of adjustments that manage
               group scaling. These have the following structure:
        :param pulumi.Input[pulumi.InputType['PolicyTargetTrackingConfigurationArgs']] target_tracking_configuration: A target tracking policy. These have the following structure:
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

            __props__['adjustment_type'] = adjustment_type
            if autoscaling_group_name is None:
                raise TypeError("Missing required property 'autoscaling_group_name'")
            __props__['autoscaling_group_name'] = autoscaling_group_name
            __props__['cooldown'] = cooldown
            __props__['estimated_instance_warmup'] = estimated_instance_warmup
            __props__['metric_aggregation_type'] = metric_aggregation_type
            __props__['min_adjustment_magnitude'] = min_adjustment_magnitude
            __props__['name'] = name
            __props__['policy_type'] = policy_type
            __props__['scaling_adjustment'] = scaling_adjustment
            __props__['step_adjustments'] = step_adjustments
            __props__['target_tracking_configuration'] = target_tracking_configuration
            __props__['arn'] = None
        super(Policy, __self__).__init__(
            'aws:autoscaling/policy:Policy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            adjustment_type: Optional[pulumi.Input[str]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            autoscaling_group_name: Optional[pulumi.Input[str]] = None,
            cooldown: Optional[pulumi.Input[float]] = None,
            estimated_instance_warmup: Optional[pulumi.Input[float]] = None,
            metric_aggregation_type: Optional[pulumi.Input[str]] = None,
            min_adjustment_magnitude: Optional[pulumi.Input[float]] = None,
            name: Optional[pulumi.Input[str]] = None,
            policy_type: Optional[pulumi.Input[str]] = None,
            scaling_adjustment: Optional[pulumi.Input[float]] = None,
            step_adjustments: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['PolicyStepAdjustmentArgs']]]]] = None,
            target_tracking_configuration: Optional[pulumi.Input[pulumi.InputType['PolicyTargetTrackingConfigurationArgs']]] = None) -> 'Policy':
        """
        Get an existing Policy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] adjustment_type: Specifies whether the adjustment is an absolute number or a percentage of the current capacity. Valid values are `ChangeInCapacity`, `ExactCapacity`, and `PercentChangeInCapacity`.
        :param pulumi.Input[str] arn: The ARN assigned by AWS to the scaling policy.
        :param pulumi.Input[str] autoscaling_group_name: The name of the autoscaling group.
        :param pulumi.Input[float] cooldown: The amount of time, in seconds, after a scaling activity completes and before the next scaling activity can start.
        :param pulumi.Input[float] estimated_instance_warmup: The estimated time, in seconds, until a newly launched instance will contribute CloudWatch metrics. Without a value, AWS will default to the group's specified cooldown period.
        :param pulumi.Input[str] metric_aggregation_type: The aggregation type for the policy's metrics. Valid values are "Minimum", "Maximum", and "Average". Without a value, AWS will treat the aggregation type as "Average".
        :param pulumi.Input[str] name: The name of the dimension.
        :param pulumi.Input[str] policy_type: The policy type, either "SimpleScaling", "StepScaling" or "TargetTrackingScaling". If this value isn't provided, AWS will default to "SimpleScaling."
        :param pulumi.Input[float] scaling_adjustment: The number of members by which to
               scale, when the adjustment bounds are breached. A positive value scales
               up. A negative value scales down.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['PolicyStepAdjustmentArgs']]]] step_adjustments: A set of adjustments that manage
               group scaling. These have the following structure:
        :param pulumi.Input[pulumi.InputType['PolicyTargetTrackingConfigurationArgs']] target_tracking_configuration: A target tracking policy. These have the following structure:
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["adjustment_type"] = adjustment_type
        __props__["arn"] = arn
        __props__["autoscaling_group_name"] = autoscaling_group_name
        __props__["cooldown"] = cooldown
        __props__["estimated_instance_warmup"] = estimated_instance_warmup
        __props__["metric_aggregation_type"] = metric_aggregation_type
        __props__["min_adjustment_magnitude"] = min_adjustment_magnitude
        __props__["name"] = name
        __props__["policy_type"] = policy_type
        __props__["scaling_adjustment"] = scaling_adjustment
        __props__["step_adjustments"] = step_adjustments
        __props__["target_tracking_configuration"] = target_tracking_configuration
        return Policy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="adjustmentType")
    def adjustment_type(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies whether the adjustment is an absolute number or a percentage of the current capacity. Valid values are `ChangeInCapacity`, `ExactCapacity`, and `PercentChangeInCapacity`.
        """
        return pulumi.get(self, "adjustment_type")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN assigned by AWS to the scaling policy.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="autoscalingGroupName")
    def autoscaling_group_name(self) -> pulumi.Output[str]:
        """
        The name of the autoscaling group.
        """
        return pulumi.get(self, "autoscaling_group_name")

    @property
    @pulumi.getter
    def cooldown(self) -> pulumi.Output[Optional[float]]:
        """
        The amount of time, in seconds, after a scaling activity completes and before the next scaling activity can start.
        """
        return pulumi.get(self, "cooldown")

    @property
    @pulumi.getter(name="estimatedInstanceWarmup")
    def estimated_instance_warmup(self) -> pulumi.Output[Optional[float]]:
        """
        The estimated time, in seconds, until a newly launched instance will contribute CloudWatch metrics. Without a value, AWS will default to the group's specified cooldown period.
        """
        return pulumi.get(self, "estimated_instance_warmup")

    @property
    @pulumi.getter(name="metricAggregationType")
    def metric_aggregation_type(self) -> pulumi.Output[str]:
        """
        The aggregation type for the policy's metrics. Valid values are "Minimum", "Maximum", and "Average". Without a value, AWS will treat the aggregation type as "Average".
        """
        return pulumi.get(self, "metric_aggregation_type")

    @property
    @pulumi.getter(name="minAdjustmentMagnitude")
    def min_adjustment_magnitude(self) -> pulumi.Output[Optional[float]]:
        return pulumi.get(self, "min_adjustment_magnitude")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the dimension.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="policyType")
    def policy_type(self) -> pulumi.Output[Optional[str]]:
        """
        The policy type, either "SimpleScaling", "StepScaling" or "TargetTrackingScaling". If this value isn't provided, AWS will default to "SimpleScaling."
        """
        return pulumi.get(self, "policy_type")

    @property
    @pulumi.getter(name="scalingAdjustment")
    def scaling_adjustment(self) -> pulumi.Output[Optional[float]]:
        """
        The number of members by which to
        scale, when the adjustment bounds are breached. A positive value scales
        up. A negative value scales down.
        """
        return pulumi.get(self, "scaling_adjustment")

    @property
    @pulumi.getter(name="stepAdjustments")
    def step_adjustments(self) -> pulumi.Output[Optional[List['outputs.PolicyStepAdjustment']]]:
        """
        A set of adjustments that manage
        group scaling. These have the following structure:
        """
        return pulumi.get(self, "step_adjustments")

    @property
    @pulumi.getter(name="targetTrackingConfiguration")
    def target_tracking_configuration(self) -> pulumi.Output[Optional['outputs.PolicyTargetTrackingConfiguration']]:
        """
        A target tracking policy. These have the following structure:
        """
        return pulumi.get(self, "target_tracking_configuration")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

