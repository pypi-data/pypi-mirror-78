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

__all__ = ['TargetGroup']


class TargetGroup(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 deregistration_delay: Optional[pulumi.Input[float]] = None,
                 health_check: Optional[pulumi.Input[pulumi.InputType['TargetGroupHealthCheckArgs']]] = None,
                 lambda_multi_value_headers_enabled: Optional[pulumi.Input[bool]] = None,
                 load_balancing_algorithm_type: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_prefix: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[float]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 proxy_protocol_v2: Optional[pulumi.Input[bool]] = None,
                 slow_start: Optional[pulumi.Input[float]] = None,
                 stickiness: Optional[pulumi.Input[pulumi.InputType['TargetGroupStickinessArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_type: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a Target Group resource for use with Load Balancer resources.

        > **Note:** `alb.TargetGroup` is known as `lb.TargetGroup`. The functionality is identical.

        ## Example Usage
        ### Instance Target Group

        ```python
        import pulumi
        import pulumi_aws as aws

        main = aws.ec2.Vpc("main", cidr_block="10.0.0.0/16")
        test = aws.lb.TargetGroup("test",
            port=80,
            protocol="HTTP",
            vpc_id=main.id)
        ```
        ### IP Target Group

        ```python
        import pulumi
        import pulumi_aws as aws

        main = aws.ec2.Vpc("main", cidr_block="10.0.0.0/16")
        ip_example = aws.lb.TargetGroup("ip-example",
            port=80,
            protocol="HTTP",
            target_type="ip",
            vpc_id=main.id)
        ```
        ### Lambda Target Group

        ```python
        import pulumi
        import pulumi_aws as aws

        lambda_example = aws.lb.TargetGroup("lambda-example", target_type="lambda")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] deregistration_delay: The amount time for Elastic Load Balancing to wait before changing the state of a deregistering target from draining to unused. The range is 0-3600 seconds. The default value is 300 seconds.
        :param pulumi.Input[pulumi.InputType['TargetGroupHealthCheckArgs']] health_check: A Health Check block. Health Check blocks are documented below.
        :param pulumi.Input[bool] lambda_multi_value_headers_enabled: Boolean whether the request and response headers exchanged between the load balancer and the Lambda function include arrays of values or strings. Only applies when `target_type` is `lambda`.
        :param pulumi.Input[str] load_balancing_algorithm_type: Determines how the load balancer selects targets when routing requests. Only applicable for Application Load Balancer Target Groups. The value is `round_robin` or `least_outstanding_requests`. The default is `round_robin`.
        :param pulumi.Input[str] name: The name of the target group. If omitted, this provider will assign a random, unique name.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`. Cannot be longer than 6 characters.
        :param pulumi.Input[float] port: The port on which targets receive traffic, unless overridden when registering a specific target. Required when `target_type` is `instance` or `ip`. Does not apply when `target_type` is `lambda`.
        :param pulumi.Input[str] protocol: The protocol to use for routing traffic to the targets. Should be one of "TCP", "TLS", "UDP", "TCP_UDP", "HTTP" or "HTTPS". Required when `target_type` is `instance` or `ip`. Does not apply when `target_type` is `lambda`.
        :param pulumi.Input[bool] proxy_protocol_v2: Boolean to enable / disable support for proxy protocol v2 on Network Load Balancers. See [doc](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#proxy-protocol) for more information.
        :param pulumi.Input[float] slow_start: The amount time for targets to warm up before the load balancer sends them a full share of requests. The range is 30-900 seconds or 0 to disable. The default value is 0 seconds.
        :param pulumi.Input[pulumi.InputType['TargetGroupStickinessArgs']] stickiness: A Stickiness block. Stickiness blocks are documented below. `stickiness` is only valid if used with Load Balancers of type `Application`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource.
        :param pulumi.Input[str] target_type: The type of target that you must specify when registering targets with this target group.
               The possible values are `instance` (targets are specified by instance ID) or `ip` (targets are specified by IP address) or `lambda` (targets are specified by lambda arn).
               The default is `instance`. Note that you can't specify targets for a target group using both instance IDs and IP addresses.
               If the target type is `ip`, specify IP addresses from the subnets of the virtual private cloud (VPC) for the target group,
               the RFC 1918 range (10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16), and the RFC 6598 range (100.64.0.0/10).
               You can't specify publicly routable IP addresses.
        :param pulumi.Input[str] vpc_id: The identifier of the VPC in which to create the target group. Required when `target_type` is `instance` or `ip`. Does not apply when `target_type` is `lambda`.
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

            __props__['deregistration_delay'] = deregistration_delay
            __props__['health_check'] = health_check
            __props__['lambda_multi_value_headers_enabled'] = lambda_multi_value_headers_enabled
            __props__['load_balancing_algorithm_type'] = load_balancing_algorithm_type
            __props__['name'] = name
            __props__['name_prefix'] = name_prefix
            __props__['port'] = port
            __props__['protocol'] = protocol
            __props__['proxy_protocol_v2'] = proxy_protocol_v2
            __props__['slow_start'] = slow_start
            __props__['stickiness'] = stickiness
            __props__['tags'] = tags
            __props__['target_type'] = target_type
            __props__['vpc_id'] = vpc_id
            __props__['arn'] = None
            __props__['arn_suffix'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="aws:applicationloadbalancing/targetGroup:TargetGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(TargetGroup, __self__).__init__(
            'aws:alb/targetGroup:TargetGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            arn_suffix: Optional[pulumi.Input[str]] = None,
            deregistration_delay: Optional[pulumi.Input[float]] = None,
            health_check: Optional[pulumi.Input[pulumi.InputType['TargetGroupHealthCheckArgs']]] = None,
            lambda_multi_value_headers_enabled: Optional[pulumi.Input[bool]] = None,
            load_balancing_algorithm_type: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            name_prefix: Optional[pulumi.Input[str]] = None,
            port: Optional[pulumi.Input[float]] = None,
            protocol: Optional[pulumi.Input[str]] = None,
            proxy_protocol_v2: Optional[pulumi.Input[bool]] = None,
            slow_start: Optional[pulumi.Input[float]] = None,
            stickiness: Optional[pulumi.Input[pulumi.InputType['TargetGroupStickinessArgs']]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            target_type: Optional[pulumi.Input[str]] = None,
            vpc_id: Optional[pulumi.Input[str]] = None) -> 'TargetGroup':
        """
        Get an existing TargetGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the Target Group (matches `id`)
        :param pulumi.Input[str] arn_suffix: The ARN suffix for use with CloudWatch Metrics.
        :param pulumi.Input[float] deregistration_delay: The amount time for Elastic Load Balancing to wait before changing the state of a deregistering target from draining to unused. The range is 0-3600 seconds. The default value is 300 seconds.
        :param pulumi.Input[pulumi.InputType['TargetGroupHealthCheckArgs']] health_check: A Health Check block. Health Check blocks are documented below.
        :param pulumi.Input[bool] lambda_multi_value_headers_enabled: Boolean whether the request and response headers exchanged between the load balancer and the Lambda function include arrays of values or strings. Only applies when `target_type` is `lambda`.
        :param pulumi.Input[str] load_balancing_algorithm_type: Determines how the load balancer selects targets when routing requests. Only applicable for Application Load Balancer Target Groups. The value is `round_robin` or `least_outstanding_requests`. The default is `round_robin`.
        :param pulumi.Input[str] name: The name of the target group. If omitted, this provider will assign a random, unique name.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`. Cannot be longer than 6 characters.
        :param pulumi.Input[float] port: The port on which targets receive traffic, unless overridden when registering a specific target. Required when `target_type` is `instance` or `ip`. Does not apply when `target_type` is `lambda`.
        :param pulumi.Input[str] protocol: The protocol to use for routing traffic to the targets. Should be one of "TCP", "TLS", "UDP", "TCP_UDP", "HTTP" or "HTTPS". Required when `target_type` is `instance` or `ip`. Does not apply when `target_type` is `lambda`.
        :param pulumi.Input[bool] proxy_protocol_v2: Boolean to enable / disable support for proxy protocol v2 on Network Load Balancers. See [doc](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#proxy-protocol) for more information.
        :param pulumi.Input[float] slow_start: The amount time for targets to warm up before the load balancer sends them a full share of requests. The range is 30-900 seconds or 0 to disable. The default value is 0 seconds.
        :param pulumi.Input[pulumi.InputType['TargetGroupStickinessArgs']] stickiness: A Stickiness block. Stickiness blocks are documented below. `stickiness` is only valid if used with Load Balancers of type `Application`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource.
        :param pulumi.Input[str] target_type: The type of target that you must specify when registering targets with this target group.
               The possible values are `instance` (targets are specified by instance ID) or `ip` (targets are specified by IP address) or `lambda` (targets are specified by lambda arn).
               The default is `instance`. Note that you can't specify targets for a target group using both instance IDs and IP addresses.
               If the target type is `ip`, specify IP addresses from the subnets of the virtual private cloud (VPC) for the target group,
               the RFC 1918 range (10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16), and the RFC 6598 range (100.64.0.0/10).
               You can't specify publicly routable IP addresses.
        :param pulumi.Input[str] vpc_id: The identifier of the VPC in which to create the target group. Required when `target_type` is `instance` or `ip`. Does not apply when `target_type` is `lambda`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["arn_suffix"] = arn_suffix
        __props__["deregistration_delay"] = deregistration_delay
        __props__["health_check"] = health_check
        __props__["lambda_multi_value_headers_enabled"] = lambda_multi_value_headers_enabled
        __props__["load_balancing_algorithm_type"] = load_balancing_algorithm_type
        __props__["name"] = name
        __props__["name_prefix"] = name_prefix
        __props__["port"] = port
        __props__["protocol"] = protocol
        __props__["proxy_protocol_v2"] = proxy_protocol_v2
        __props__["slow_start"] = slow_start
        __props__["stickiness"] = stickiness
        __props__["tags"] = tags
        __props__["target_type"] = target_type
        __props__["vpc_id"] = vpc_id
        return TargetGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the Target Group (matches `id`)
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="arnSuffix")
    def arn_suffix(self) -> pulumi.Output[str]:
        """
        The ARN suffix for use with CloudWatch Metrics.
        """
        return pulumi.get(self, "arn_suffix")

    @property
    @pulumi.getter(name="deregistrationDelay")
    def deregistration_delay(self) -> pulumi.Output[Optional[float]]:
        """
        The amount time for Elastic Load Balancing to wait before changing the state of a deregistering target from draining to unused. The range is 0-3600 seconds. The default value is 300 seconds.
        """
        return pulumi.get(self, "deregistration_delay")

    @property
    @pulumi.getter(name="healthCheck")
    def health_check(self) -> pulumi.Output['outputs.TargetGroupHealthCheck']:
        """
        A Health Check block. Health Check blocks are documented below.
        """
        return pulumi.get(self, "health_check")

    @property
    @pulumi.getter(name="lambdaMultiValueHeadersEnabled")
    def lambda_multi_value_headers_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Boolean whether the request and response headers exchanged between the load balancer and the Lambda function include arrays of values or strings. Only applies when `target_type` is `lambda`.
        """
        return pulumi.get(self, "lambda_multi_value_headers_enabled")

    @property
    @pulumi.getter(name="loadBalancingAlgorithmType")
    def load_balancing_algorithm_type(self) -> pulumi.Output[str]:
        """
        Determines how the load balancer selects targets when routing requests. Only applicable for Application Load Balancer Target Groups. The value is `round_robin` or `least_outstanding_requests`. The default is `round_robin`.
        """
        return pulumi.get(self, "load_balancing_algorithm_type")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the target group. If omitted, this provider will assign a random, unique name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="namePrefix")
    def name_prefix(self) -> pulumi.Output[Optional[str]]:
        """
        Creates a unique name beginning with the specified prefix. Conflicts with `name`. Cannot be longer than 6 characters.
        """
        return pulumi.get(self, "name_prefix")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[Optional[float]]:
        """
        The port on which targets receive traffic, unless overridden when registering a specific target. Required when `target_type` is `instance` or `ip`. Does not apply when `target_type` is `lambda`.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Output[Optional[str]]:
        """
        The protocol to use for routing traffic to the targets. Should be one of "TCP", "TLS", "UDP", "TCP_UDP", "HTTP" or "HTTPS". Required when `target_type` is `instance` or `ip`. Does not apply when `target_type` is `lambda`.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="proxyProtocolV2")
    def proxy_protocol_v2(self) -> pulumi.Output[Optional[bool]]:
        """
        Boolean to enable / disable support for proxy protocol v2 on Network Load Balancers. See [doc](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#proxy-protocol) for more information.
        """
        return pulumi.get(self, "proxy_protocol_v2")

    @property
    @pulumi.getter(name="slowStart")
    def slow_start(self) -> pulumi.Output[Optional[float]]:
        """
        The amount time for targets to warm up before the load balancer sends them a full share of requests. The range is 30-900 seconds or 0 to disable. The default value is 0 seconds.
        """
        return pulumi.get(self, "slow_start")

    @property
    @pulumi.getter
    def stickiness(self) -> pulumi.Output['outputs.TargetGroupStickiness']:
        """
        A Stickiness block. Stickiness blocks are documented below. `stickiness` is only valid if used with Load Balancers of type `Application`
        """
        return pulumi.get(self, "stickiness")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetType")
    def target_type(self) -> pulumi.Output[Optional[str]]:
        """
        The type of target that you must specify when registering targets with this target group.
        The possible values are `instance` (targets are specified by instance ID) or `ip` (targets are specified by IP address) or `lambda` (targets are specified by lambda arn).
        The default is `instance`. Note that you can't specify targets for a target group using both instance IDs and IP addresses.
        If the target type is `ip`, specify IP addresses from the subnets of the virtual private cloud (VPC) for the target group,
        the RFC 1918 range (10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16), and the RFC 6598 range (100.64.0.0/10).
        You can't specify publicly routable IP addresses.
        """
        return pulumi.get(self, "target_type")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Output[Optional[str]]:
        """
        The identifier of the VPC in which to create the target group. Required when `target_type` is `instance` or `ip`. Does not apply when `target_type` is `lambda`.
        """
        return pulumi.get(self, "vpc_id")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

