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

__all__ = ['Stage']


class Stage(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_log_settings: Optional[pulumi.Input[pulumi.InputType['StageAccessLogSettingsArgs']]] = None,
                 cache_cluster_enabled: Optional[pulumi.Input[bool]] = None,
                 cache_cluster_size: Optional[pulumi.Input[str]] = None,
                 client_certificate_id: Optional[pulumi.Input[str]] = None,
                 deployment: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 documentation_version: Optional[pulumi.Input[str]] = None,
                 rest_api: Optional[pulumi.Input[str]] = None,
                 stage_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 xray_tracing_enabled: Optional[pulumi.Input[bool]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides an API Gateway Stage.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test_rest_api = aws.apigateway.RestApi("testRestApi", description="This is my API for demonstration purposes")
        test_resource = aws.apigateway.Resource("testResource",
            rest_api=test_rest_api.id,
            parent_id=test_rest_api.root_resource_id,
            path_part="mytestresource")
        test_method = aws.apigateway.Method("testMethod",
            rest_api=test_rest_api.id,
            resource_id=test_resource.id,
            http_method="GET",
            authorization="NONE")
        test_integration = aws.apigateway.Integration("testIntegration",
            rest_api=test_rest_api.id,
            resource_id=test_resource.id,
            http_method=test_method.http_method,
            type="MOCK")
        test_deployment = aws.apigateway.Deployment("testDeployment",
            rest_api=test_rest_api.id,
            stage_name="dev",
            opts=ResourceOptions(depends_on=[test_integration]))
        test_stage = aws.apigateway.Stage("testStage",
            stage_name="prod",
            rest_api=test_rest_api.id,
            deployment=test_deployment.id)
        method_settings = aws.apigateway.MethodSettings("methodSettings",
            rest_api=test_rest_api.id,
            stage_name=test_stage.stage_name,
            method_path=pulumi.Output.all(test_resource.path_part, test_method.http_method).apply(lambda path_part, http_method: f"{path_part}/{http_method}"),
            settings=aws.apigateway.MethodSettingsSettingsArgs(
                metrics_enabled=True,
                logging_level="INFO",
            ))
        ```
        ### Managing the API Logging CloudWatch Log Group

        API Gateway provides the ability to [enable CloudWatch API logging](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-logging.html). To manage the CloudWatch Log Group when this feature is enabled, the `cloudwatch.LogGroup` resource can be used where the name matches the API Gateway naming convention. If the CloudWatch Log Group previously exists, the `cloudwatch.LogGroup` resource can be imported as a one time operation and recreation of the environment can occur without import.

        > The below configuration uses [`dependsOn`](https://www.pulumi.com/docs/intro/concepts/programming-model/#dependson) to prevent ordering issues with API Gateway automatically creating the log group first and a variable for naming consistency. Other ordering and naming methodologies may be more appropriate for your environment.

        ```python
        import pulumi
        import pulumi_aws as aws

        config = pulumi.Config()
        stage_name = config.get("stageName")
        if stage_name is None:
            stage_name = "example"
        example_rest_api = aws.apigateway.RestApi("exampleRestApi")
        # ... other configuration ...
        example_log_group = aws.cloudwatch.LogGroup("exampleLogGroup", retention_in_days=7)
        # ... potentially other configuration ...
        example_stage = aws.apigateway.Stage("exampleStage", stage_name=stage_name,
        opts=ResourceOptions(depends_on=[example_log_group]))
        # ... other configuration ...
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['StageAccessLogSettingsArgs']] access_log_settings: Enables access logs for the API stage. Detailed below.
        :param pulumi.Input[bool] cache_cluster_enabled: Specifies whether a cache cluster is enabled for the stage
        :param pulumi.Input[str] cache_cluster_size: The size of the cache cluster for the stage, if enabled.
               Allowed values include `0.5`, `1.6`, `6.1`, `13.5`, `28.4`, `58.2`, `118` and `237`.
        :param pulumi.Input[str] client_certificate_id: The identifier of a client certificate for the stage.
        :param pulumi.Input[str] deployment: The ID of the deployment that the stage points to
        :param pulumi.Input[str] description: The description of the stage
        :param pulumi.Input[str] documentation_version: The version of the associated API documentation
        :param pulumi.Input[str] rest_api: The ID of the associated REST API
        :param pulumi.Input[str] stage_name: The name of the stage
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] variables: A map that defines the stage variables
        :param pulumi.Input[bool] xray_tracing_enabled: Whether active tracing with X-ray is enabled. Defaults to `false`.
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

            __props__['access_log_settings'] = access_log_settings
            __props__['cache_cluster_enabled'] = cache_cluster_enabled
            __props__['cache_cluster_size'] = cache_cluster_size
            __props__['client_certificate_id'] = client_certificate_id
            if deployment is None:
                raise TypeError("Missing required property 'deployment'")
            __props__['deployment'] = deployment
            __props__['description'] = description
            __props__['documentation_version'] = documentation_version
            if rest_api is None:
                raise TypeError("Missing required property 'rest_api'")
            __props__['rest_api'] = rest_api
            if stage_name is None:
                raise TypeError("Missing required property 'stage_name'")
            __props__['stage_name'] = stage_name
            __props__['tags'] = tags
            __props__['variables'] = variables
            __props__['xray_tracing_enabled'] = xray_tracing_enabled
            __props__['arn'] = None
            __props__['execution_arn'] = None
            __props__['invoke_url'] = None
        super(Stage, __self__).__init__(
            'aws:apigateway/stage:Stage',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access_log_settings: Optional[pulumi.Input[pulumi.InputType['StageAccessLogSettingsArgs']]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            cache_cluster_enabled: Optional[pulumi.Input[bool]] = None,
            cache_cluster_size: Optional[pulumi.Input[str]] = None,
            client_certificate_id: Optional[pulumi.Input[str]] = None,
            deployment: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            documentation_version: Optional[pulumi.Input[str]] = None,
            execution_arn: Optional[pulumi.Input[str]] = None,
            invoke_url: Optional[pulumi.Input[str]] = None,
            rest_api: Optional[pulumi.Input[str]] = None,
            stage_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            xray_tracing_enabled: Optional[pulumi.Input[bool]] = None) -> 'Stage':
        """
        Get an existing Stage resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['StageAccessLogSettingsArgs']] access_log_settings: Enables access logs for the API stage. Detailed below.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN)
        :param pulumi.Input[bool] cache_cluster_enabled: Specifies whether a cache cluster is enabled for the stage
        :param pulumi.Input[str] cache_cluster_size: The size of the cache cluster for the stage, if enabled.
               Allowed values include `0.5`, `1.6`, `6.1`, `13.5`, `28.4`, `58.2`, `118` and `237`.
        :param pulumi.Input[str] client_certificate_id: The identifier of a client certificate for the stage.
        :param pulumi.Input[str] deployment: The ID of the deployment that the stage points to
        :param pulumi.Input[str] description: The description of the stage
        :param pulumi.Input[str] documentation_version: The version of the associated API documentation
        :param pulumi.Input[str] execution_arn: The execution ARN to be used in `lambda_permission`'s `source_arn`
               when allowing API Gateway to invoke a Lambda function,
               e.g. `arn:aws:execute-api:eu-west-2:123456789012:z4675bid1j/prod`
        :param pulumi.Input[str] invoke_url: The URL to invoke the API pointing to the stage,
               e.g. `https://z4675bid1j.execute-api.eu-west-2.amazonaws.com/prod`
        :param pulumi.Input[str] rest_api: The ID of the associated REST API
        :param pulumi.Input[str] stage_name: The name of the stage
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] variables: A map that defines the stage variables
        :param pulumi.Input[bool] xray_tracing_enabled: Whether active tracing with X-ray is enabled. Defaults to `false`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["access_log_settings"] = access_log_settings
        __props__["arn"] = arn
        __props__["cache_cluster_enabled"] = cache_cluster_enabled
        __props__["cache_cluster_size"] = cache_cluster_size
        __props__["client_certificate_id"] = client_certificate_id
        __props__["deployment"] = deployment
        __props__["description"] = description
        __props__["documentation_version"] = documentation_version
        __props__["execution_arn"] = execution_arn
        __props__["invoke_url"] = invoke_url
        __props__["rest_api"] = rest_api
        __props__["stage_name"] = stage_name
        __props__["tags"] = tags
        __props__["variables"] = variables
        __props__["xray_tracing_enabled"] = xray_tracing_enabled
        return Stage(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessLogSettings")
    def access_log_settings(self) -> pulumi.Output[Optional['outputs.StageAccessLogSettings']]:
        """
        Enables access logs for the API stage. Detailed below.
        """
        return pulumi.get(self, "access_log_settings")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN)
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="cacheClusterEnabled")
    def cache_cluster_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether a cache cluster is enabled for the stage
        """
        return pulumi.get(self, "cache_cluster_enabled")

    @property
    @pulumi.getter(name="cacheClusterSize")
    def cache_cluster_size(self) -> pulumi.Output[Optional[str]]:
        """
        The size of the cache cluster for the stage, if enabled.
        Allowed values include `0.5`, `1.6`, `6.1`, `13.5`, `28.4`, `58.2`, `118` and `237`.
        """
        return pulumi.get(self, "cache_cluster_size")

    @property
    @pulumi.getter(name="clientCertificateId")
    def client_certificate_id(self) -> pulumi.Output[Optional[str]]:
        """
        The identifier of a client certificate for the stage.
        """
        return pulumi.get(self, "client_certificate_id")

    @property
    @pulumi.getter
    def deployment(self) -> pulumi.Output[str]:
        """
        The ID of the deployment that the stage points to
        """
        return pulumi.get(self, "deployment")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the stage
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="documentationVersion")
    def documentation_version(self) -> pulumi.Output[Optional[str]]:
        """
        The version of the associated API documentation
        """
        return pulumi.get(self, "documentation_version")

    @property
    @pulumi.getter(name="executionArn")
    def execution_arn(self) -> pulumi.Output[str]:
        """
        The execution ARN to be used in `lambda_permission`'s `source_arn`
        when allowing API Gateway to invoke a Lambda function,
        e.g. `arn:aws:execute-api:eu-west-2:123456789012:z4675bid1j/prod`
        """
        return pulumi.get(self, "execution_arn")

    @property
    @pulumi.getter(name="invokeUrl")
    def invoke_url(self) -> pulumi.Output[str]:
        """
        The URL to invoke the API pointing to the stage,
        e.g. `https://z4675bid1j.execute-api.eu-west-2.amazonaws.com/prod`
        """
        return pulumi.get(self, "invoke_url")

    @property
    @pulumi.getter(name="restApi")
    def rest_api(self) -> pulumi.Output[str]:
        """
        The ID of the associated REST API
        """
        return pulumi.get(self, "rest_api")

    @property
    @pulumi.getter(name="stageName")
    def stage_name(self) -> pulumi.Output[str]:
        """
        The name of the stage
        """
        return pulumi.get(self, "stage_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def variables(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map that defines the stage variables
        """
        return pulumi.get(self, "variables")

    @property
    @pulumi.getter(name="xrayTracingEnabled")
    def xray_tracing_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether active tracing with X-ray is enabled. Defaults to `false`.
        """
        return pulumi.get(self, "xray_tracing_enabled")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

