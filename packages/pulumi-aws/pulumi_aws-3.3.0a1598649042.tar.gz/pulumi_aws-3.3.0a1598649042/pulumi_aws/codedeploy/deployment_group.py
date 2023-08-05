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

__all__ = ['DeploymentGroup']


class DeploymentGroup(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 alarm_configuration: Optional[pulumi.Input[pulumi.InputType['DeploymentGroupAlarmConfigurationArgs']]] = None,
                 app_name: Optional[pulumi.Input[str]] = None,
                 auto_rollback_configuration: Optional[pulumi.Input[pulumi.InputType['DeploymentGroupAutoRollbackConfigurationArgs']]] = None,
                 autoscaling_groups: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 blue_green_deployment_config: Optional[pulumi.Input[pulumi.InputType['DeploymentGroupBlueGreenDeploymentConfigArgs']]] = None,
                 deployment_config_name: Optional[pulumi.Input[str]] = None,
                 deployment_group_name: Optional[pulumi.Input[str]] = None,
                 deployment_style: Optional[pulumi.Input[pulumi.InputType['DeploymentGroupDeploymentStyleArgs']]] = None,
                 ec2_tag_filters: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['DeploymentGroupEc2TagFilterArgs']]]]] = None,
                 ec2_tag_sets: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['DeploymentGroupEc2TagSetArgs']]]]] = None,
                 ecs_service: Optional[pulumi.Input[pulumi.InputType['DeploymentGroupEcsServiceArgs']]] = None,
                 load_balancer_info: Optional[pulumi.Input[pulumi.InputType['DeploymentGroupLoadBalancerInfoArgs']]] = None,
                 on_premises_instance_tag_filters: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['DeploymentGroupOnPremisesInstanceTagFilterArgs']]]]] = None,
                 service_role_arn: Optional[pulumi.Input[str]] = None,
                 trigger_configurations: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['DeploymentGroupTriggerConfigurationArgs']]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a CodeDeploy Deployment Group for a CodeDeploy Application

        > **NOTE on blue/green deployments:** When using `green_fleet_provisioning_option` with the `COPY_AUTO_SCALING_GROUP` action, CodeDeploy will create a new ASG with a different name. This ASG is _not_ managed by this provider and will conflict with existing configuration and state. You may want to use a different approach to managing deployments that involve multiple ASG, such as `DISCOVER_EXISTING` with separate blue and green ASG.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example_role = aws.iam.Role("exampleRole", assume_role_policy=\"\"\"{
          "Version": "2012-10-17",
          "Statement": [
            {
              "Sid": "",
              "Effect": "Allow",
              "Principal": {
                "Service": "codedeploy.amazonaws.com"
              },
              "Action": "sts:AssumeRole"
            }
          ]
        }
        \"\"\")
        a_ws_code_deploy_role = aws.iam.RolePolicyAttachment("aWSCodeDeployRole",
            policy_arn="arn:aws:iam::aws:policy/service-role/AWSCodeDeployRole",
            role=example_role.name)
        example_application = aws.codedeploy.Application("exampleApplication")
        example_topic = aws.sns.Topic("exampleTopic")
        example_deployment_group = aws.codedeploy.DeploymentGroup("exampleDeploymentGroup",
            app_name=example_application.name,
            deployment_group_name="example-group",
            service_role_arn=example_role.arn,
            ec2_tag_sets=[aws.codedeploy.DeploymentGroupEc2TagSetArgs(
                ec2_tag_filters=[
                    {
                        "key": "filterkey1",
                        "type": "KEY_AND_VALUE",
                        "value": "filtervalue",
                    },
                    {
                        "key": "filterkey2",
                        "type": "KEY_AND_VALUE",
                        "value": "filtervalue",
                    },
                ],
            )],
            trigger_configurations=[aws.codedeploy.DeploymentGroupTriggerConfigurationArgs(
                trigger_events=["DeploymentFailure"],
                trigger_name="example-trigger",
                trigger_target_arn=example_topic.arn,
            )],
            auto_rollback_configuration=aws.codedeploy.DeploymentGroupAutoRollbackConfigurationArgs(
                enabled=True,
                events=["DEPLOYMENT_FAILURE"],
            ),
            alarm_configuration=aws.codedeploy.DeploymentGroupAlarmConfigurationArgs(
                alarms=["my-alarm-name"],
                enabled=True,
            ))
        ```
        ### Blue Green Deployments with ECS

        ```python
        import pulumi
        import pulumi_aws as aws

        example_application = aws.codedeploy.Application("exampleApplication", compute_platform="ECS")
        example_deployment_group = aws.codedeploy.DeploymentGroup("exampleDeploymentGroup",
            app_name=example_application.name,
            deployment_config_name="CodeDeployDefault.ECSAllAtOnce",
            deployment_group_name="example",
            service_role_arn=aws_iam_role["example"]["arn"],
            auto_rollback_configuration=aws.codedeploy.DeploymentGroupAutoRollbackConfigurationArgs(
                enabled=True,
                events=["DEPLOYMENT_FAILURE"],
            ),
            blue_green_deployment_config=aws.codedeploy.DeploymentGroupBlueGreenDeploymentConfigArgs(
                deployment_ready_option=aws.codedeploy.DeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOptionArgs(
                    action_on_timeout="CONTINUE_DEPLOYMENT",
                ),
                terminate_blue_instances_on_deployment_success=aws.codedeploy.DeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccessArgs(
                    action="TERMINATE",
                    termination_wait_time_in_minutes=5,
                ),
            ),
            deployment_style=aws.codedeploy.DeploymentGroupDeploymentStyleArgs(
                deployment_option="WITH_TRAFFIC_CONTROL",
                deployment_type="BLUE_GREEN",
            ),
            ecs_service=aws.codedeploy.DeploymentGroupEcsServiceArgs(
                cluster_name=aws_ecs_cluster["example"]["name"],
                service_name=aws_ecs_service["example"]["name"],
            ),
            load_balancer_info=aws.codedeploy.DeploymentGroupLoadBalancerInfoArgs(
                target_group_pair_info=aws.codedeploy.DeploymentGroupLoadBalancerInfoTargetGroupPairInfoArgs(
                    prod_traffic_route=aws.codedeploy.DeploymentGroupLoadBalancerInfoTargetGroupPairInfoProdTrafficRouteArgs(
                        listener_arns=[aws_lb_listener["example"]["arn"]],
                    ),
                    target_groups=[
                        aws.codedeploy.DeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupArgs(
                            name=aws_lb_target_group["blue"]["name"],
                        ),
                        aws.codedeploy.DeploymentGroupLoadBalancerInfoTargetGroupPairInfoTargetGroupArgs(
                            name=aws_lb_target_group["green"]["name"],
                        ),
                    ],
                ),
            ))
        ```
        ### Blue Green Deployments with Servers and Classic ELB

        ```python
        import pulumi
        import pulumi_aws as aws

        example_application = aws.codedeploy.Application("exampleApplication")
        example_deployment_group = aws.codedeploy.DeploymentGroup("exampleDeploymentGroup",
            app_name=example_application.name,
            deployment_group_name="example-group",
            service_role_arn=aws_iam_role["example"]["arn"],
            deployment_style=aws.codedeploy.DeploymentGroupDeploymentStyleArgs(
                deployment_option="WITH_TRAFFIC_CONTROL",
                deployment_type="BLUE_GREEN",
            ),
            load_balancer_info=aws.codedeploy.DeploymentGroupLoadBalancerInfoArgs(
                elb_infos=[aws.codedeploy.DeploymentGroupLoadBalancerInfoElbInfoArgs(
                    name=aws_elb["example"]["name"],
                )],
            ),
            blue_green_deployment_config=aws.codedeploy.DeploymentGroupBlueGreenDeploymentConfigArgs(
                deployment_ready_option=aws.codedeploy.DeploymentGroupBlueGreenDeploymentConfigDeploymentReadyOptionArgs(
                    action_on_timeout="STOP_DEPLOYMENT",
                    wait_time_in_minutes=60,
                ),
                green_fleet_provisioning_option=aws.codedeploy.DeploymentGroupBlueGreenDeploymentConfigGreenFleetProvisioningOptionArgs(
                    action="DISCOVER_EXISTING",
                ),
                terminate_blue_instances_on_deployment_success=aws.codedeploy.DeploymentGroupBlueGreenDeploymentConfigTerminateBlueInstancesOnDeploymentSuccessArgs(
                    action="KEEP_ALIVE",
                ),
            ))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['DeploymentGroupAlarmConfigurationArgs']] alarm_configuration: Configuration block of alarms associated with the deployment group (documented below).
        :param pulumi.Input[str] app_name: The name of the application.
        :param pulumi.Input[pulumi.InputType['DeploymentGroupAutoRollbackConfigurationArgs']] auto_rollback_configuration: Configuration block of the automatic rollback configuration associated with the deployment group (documented below).
        :param pulumi.Input[List[pulumi.Input[str]]] autoscaling_groups: Autoscaling groups associated with the deployment group.
        :param pulumi.Input[pulumi.InputType['DeploymentGroupBlueGreenDeploymentConfigArgs']] blue_green_deployment_config: Configuration block of the blue/green deployment options for a deployment group (documented below).
        :param pulumi.Input[str] deployment_config_name: The name of the group's deployment config. The default is "CodeDeployDefault.OneAtATime".
        :param pulumi.Input[str] deployment_group_name: The name of the deployment group.
        :param pulumi.Input[pulumi.InputType['DeploymentGroupDeploymentStyleArgs']] deployment_style: Configuration block of the type of deployment, either in-place or blue/green, you want to run and whether to route deployment traffic behind a load balancer (documented below).
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['DeploymentGroupEc2TagFilterArgs']]]] ec2_tag_filters: Tag filters associated with the deployment group. See the AWS docs for details.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['DeploymentGroupEc2TagSetArgs']]]] ec2_tag_sets: Configuration block(s) of Tag filters associated with the deployment group, which are also referred to as tag groups (documented below). See the AWS docs for details.
        :param pulumi.Input[pulumi.InputType['DeploymentGroupEcsServiceArgs']] ecs_service: Configuration block(s) of the ECS services for a deployment group (documented below).
        :param pulumi.Input[pulumi.InputType['DeploymentGroupLoadBalancerInfoArgs']] load_balancer_info: Single configuration block of the load balancer to use in a blue/green deployment (documented below).
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['DeploymentGroupOnPremisesInstanceTagFilterArgs']]]] on_premises_instance_tag_filters: On premise tag filters associated with the group. See the AWS docs for details.
        :param pulumi.Input[str] service_role_arn: The service role ARN that allows deployments.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['DeploymentGroupTriggerConfigurationArgs']]]] trigger_configurations: Configuration block(s) of the triggers for the deployment group (documented below).
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

            __props__['alarm_configuration'] = alarm_configuration
            if app_name is None:
                raise TypeError("Missing required property 'app_name'")
            __props__['app_name'] = app_name
            __props__['auto_rollback_configuration'] = auto_rollback_configuration
            __props__['autoscaling_groups'] = autoscaling_groups
            __props__['blue_green_deployment_config'] = blue_green_deployment_config
            __props__['deployment_config_name'] = deployment_config_name
            if deployment_group_name is None:
                raise TypeError("Missing required property 'deployment_group_name'")
            __props__['deployment_group_name'] = deployment_group_name
            __props__['deployment_style'] = deployment_style
            __props__['ec2_tag_filters'] = ec2_tag_filters
            __props__['ec2_tag_sets'] = ec2_tag_sets
            __props__['ecs_service'] = ecs_service
            __props__['load_balancer_info'] = load_balancer_info
            __props__['on_premises_instance_tag_filters'] = on_premises_instance_tag_filters
            if service_role_arn is None:
                raise TypeError("Missing required property 'service_role_arn'")
            __props__['service_role_arn'] = service_role_arn
            __props__['trigger_configurations'] = trigger_configurations
        super(DeploymentGroup, __self__).__init__(
            'aws:codedeploy/deploymentGroup:DeploymentGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            alarm_configuration: Optional[pulumi.Input[pulumi.InputType['DeploymentGroupAlarmConfigurationArgs']]] = None,
            app_name: Optional[pulumi.Input[str]] = None,
            auto_rollback_configuration: Optional[pulumi.Input[pulumi.InputType['DeploymentGroupAutoRollbackConfigurationArgs']]] = None,
            autoscaling_groups: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            blue_green_deployment_config: Optional[pulumi.Input[pulumi.InputType['DeploymentGroupBlueGreenDeploymentConfigArgs']]] = None,
            deployment_config_name: Optional[pulumi.Input[str]] = None,
            deployment_group_name: Optional[pulumi.Input[str]] = None,
            deployment_style: Optional[pulumi.Input[pulumi.InputType['DeploymentGroupDeploymentStyleArgs']]] = None,
            ec2_tag_filters: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['DeploymentGroupEc2TagFilterArgs']]]]] = None,
            ec2_tag_sets: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['DeploymentGroupEc2TagSetArgs']]]]] = None,
            ecs_service: Optional[pulumi.Input[pulumi.InputType['DeploymentGroupEcsServiceArgs']]] = None,
            load_balancer_info: Optional[pulumi.Input[pulumi.InputType['DeploymentGroupLoadBalancerInfoArgs']]] = None,
            on_premises_instance_tag_filters: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['DeploymentGroupOnPremisesInstanceTagFilterArgs']]]]] = None,
            service_role_arn: Optional[pulumi.Input[str]] = None,
            trigger_configurations: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['DeploymentGroupTriggerConfigurationArgs']]]]] = None) -> 'DeploymentGroup':
        """
        Get an existing DeploymentGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['DeploymentGroupAlarmConfigurationArgs']] alarm_configuration: Configuration block of alarms associated with the deployment group (documented below).
        :param pulumi.Input[str] app_name: The name of the application.
        :param pulumi.Input[pulumi.InputType['DeploymentGroupAutoRollbackConfigurationArgs']] auto_rollback_configuration: Configuration block of the automatic rollback configuration associated with the deployment group (documented below).
        :param pulumi.Input[List[pulumi.Input[str]]] autoscaling_groups: Autoscaling groups associated with the deployment group.
        :param pulumi.Input[pulumi.InputType['DeploymentGroupBlueGreenDeploymentConfigArgs']] blue_green_deployment_config: Configuration block of the blue/green deployment options for a deployment group (documented below).
        :param pulumi.Input[str] deployment_config_name: The name of the group's deployment config. The default is "CodeDeployDefault.OneAtATime".
        :param pulumi.Input[str] deployment_group_name: The name of the deployment group.
        :param pulumi.Input[pulumi.InputType['DeploymentGroupDeploymentStyleArgs']] deployment_style: Configuration block of the type of deployment, either in-place or blue/green, you want to run and whether to route deployment traffic behind a load balancer (documented below).
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['DeploymentGroupEc2TagFilterArgs']]]] ec2_tag_filters: Tag filters associated with the deployment group. See the AWS docs for details.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['DeploymentGroupEc2TagSetArgs']]]] ec2_tag_sets: Configuration block(s) of Tag filters associated with the deployment group, which are also referred to as tag groups (documented below). See the AWS docs for details.
        :param pulumi.Input[pulumi.InputType['DeploymentGroupEcsServiceArgs']] ecs_service: Configuration block(s) of the ECS services for a deployment group (documented below).
        :param pulumi.Input[pulumi.InputType['DeploymentGroupLoadBalancerInfoArgs']] load_balancer_info: Single configuration block of the load balancer to use in a blue/green deployment (documented below).
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['DeploymentGroupOnPremisesInstanceTagFilterArgs']]]] on_premises_instance_tag_filters: On premise tag filters associated with the group. See the AWS docs for details.
        :param pulumi.Input[str] service_role_arn: The service role ARN that allows deployments.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['DeploymentGroupTriggerConfigurationArgs']]]] trigger_configurations: Configuration block(s) of the triggers for the deployment group (documented below).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["alarm_configuration"] = alarm_configuration
        __props__["app_name"] = app_name
        __props__["auto_rollback_configuration"] = auto_rollback_configuration
        __props__["autoscaling_groups"] = autoscaling_groups
        __props__["blue_green_deployment_config"] = blue_green_deployment_config
        __props__["deployment_config_name"] = deployment_config_name
        __props__["deployment_group_name"] = deployment_group_name
        __props__["deployment_style"] = deployment_style
        __props__["ec2_tag_filters"] = ec2_tag_filters
        __props__["ec2_tag_sets"] = ec2_tag_sets
        __props__["ecs_service"] = ecs_service
        __props__["load_balancer_info"] = load_balancer_info
        __props__["on_premises_instance_tag_filters"] = on_premises_instance_tag_filters
        __props__["service_role_arn"] = service_role_arn
        __props__["trigger_configurations"] = trigger_configurations
        return DeploymentGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="alarmConfiguration")
    def alarm_configuration(self) -> pulumi.Output[Optional['outputs.DeploymentGroupAlarmConfiguration']]:
        """
        Configuration block of alarms associated with the deployment group (documented below).
        """
        return pulumi.get(self, "alarm_configuration")

    @property
    @pulumi.getter(name="appName")
    def app_name(self) -> pulumi.Output[str]:
        """
        The name of the application.
        """
        return pulumi.get(self, "app_name")

    @property
    @pulumi.getter(name="autoRollbackConfiguration")
    def auto_rollback_configuration(self) -> pulumi.Output[Optional['outputs.DeploymentGroupAutoRollbackConfiguration']]:
        """
        Configuration block of the automatic rollback configuration associated with the deployment group (documented below).
        """
        return pulumi.get(self, "auto_rollback_configuration")

    @property
    @pulumi.getter(name="autoscalingGroups")
    def autoscaling_groups(self) -> pulumi.Output[Optional[List[str]]]:
        """
        Autoscaling groups associated with the deployment group.
        """
        return pulumi.get(self, "autoscaling_groups")

    @property
    @pulumi.getter(name="blueGreenDeploymentConfig")
    def blue_green_deployment_config(self) -> pulumi.Output['outputs.DeploymentGroupBlueGreenDeploymentConfig']:
        """
        Configuration block of the blue/green deployment options for a deployment group (documented below).
        """
        return pulumi.get(self, "blue_green_deployment_config")

    @property
    @pulumi.getter(name="deploymentConfigName")
    def deployment_config_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the group's deployment config. The default is "CodeDeployDefault.OneAtATime".
        """
        return pulumi.get(self, "deployment_config_name")

    @property
    @pulumi.getter(name="deploymentGroupName")
    def deployment_group_name(self) -> pulumi.Output[str]:
        """
        The name of the deployment group.
        """
        return pulumi.get(self, "deployment_group_name")

    @property
    @pulumi.getter(name="deploymentStyle")
    def deployment_style(self) -> pulumi.Output[Optional['outputs.DeploymentGroupDeploymentStyle']]:
        """
        Configuration block of the type of deployment, either in-place or blue/green, you want to run and whether to route deployment traffic behind a load balancer (documented below).
        """
        return pulumi.get(self, "deployment_style")

    @property
    @pulumi.getter(name="ec2TagFilters")
    def ec2_tag_filters(self) -> pulumi.Output[Optional[List['outputs.DeploymentGroupEc2TagFilter']]]:
        """
        Tag filters associated with the deployment group. See the AWS docs for details.
        """
        return pulumi.get(self, "ec2_tag_filters")

    @property
    @pulumi.getter(name="ec2TagSets")
    def ec2_tag_sets(self) -> pulumi.Output[Optional[List['outputs.DeploymentGroupEc2TagSet']]]:
        """
        Configuration block(s) of Tag filters associated with the deployment group, which are also referred to as tag groups (documented below). See the AWS docs for details.
        """
        return pulumi.get(self, "ec2_tag_sets")

    @property
    @pulumi.getter(name="ecsService")
    def ecs_service(self) -> pulumi.Output[Optional['outputs.DeploymentGroupEcsService']]:
        """
        Configuration block(s) of the ECS services for a deployment group (documented below).
        """
        return pulumi.get(self, "ecs_service")

    @property
    @pulumi.getter(name="loadBalancerInfo")
    def load_balancer_info(self) -> pulumi.Output[Optional['outputs.DeploymentGroupLoadBalancerInfo']]:
        """
        Single configuration block of the load balancer to use in a blue/green deployment (documented below).
        """
        return pulumi.get(self, "load_balancer_info")

    @property
    @pulumi.getter(name="onPremisesInstanceTagFilters")
    def on_premises_instance_tag_filters(self) -> pulumi.Output[Optional[List['outputs.DeploymentGroupOnPremisesInstanceTagFilter']]]:
        """
        On premise tag filters associated with the group. See the AWS docs for details.
        """
        return pulumi.get(self, "on_premises_instance_tag_filters")

    @property
    @pulumi.getter(name="serviceRoleArn")
    def service_role_arn(self) -> pulumi.Output[str]:
        """
        The service role ARN that allows deployments.
        """
        return pulumi.get(self, "service_role_arn")

    @property
    @pulumi.getter(name="triggerConfigurations")
    def trigger_configurations(self) -> pulumi.Output[Optional[List['outputs.DeploymentGroupTriggerConfiguration']]]:
        """
        Configuration block(s) of the triggers for the deployment group (documented below).
        """
        return pulumi.get(self, "trigger_configurations")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

