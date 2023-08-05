# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'AccountThrottleSettings',
    'DocumentationPartLocation',
    'DomainNameEndpointConfiguration',
    'MethodSettingsSettings',
    'RestApiEndpointConfiguration',
    'StageAccessLogSettings',
    'UsagePlanApiStage',
    'UsagePlanQuotaSettings',
    'UsagePlanThrottleSettings',
    'GetRestApiEndpointConfigurationResult',
]

@pulumi.output_type
class AccountThrottleSettings(dict):
    def __init__(__self__, *,
                 burst_limit: Optional[float] = None,
                 rate_limit: Optional[float] = None):
        """
        :param float burst_limit: The absolute maximum number of times API Gateway allows the API to be called per second (RPS).
        :param float rate_limit: The number of times API Gateway allows the API to be called per second on average (RPS).
        """
        if burst_limit is not None:
            pulumi.set(__self__, "burst_limit", burst_limit)
        if rate_limit is not None:
            pulumi.set(__self__, "rate_limit", rate_limit)

    @property
    @pulumi.getter(name="burstLimit")
    def burst_limit(self) -> Optional[float]:
        """
        The absolute maximum number of times API Gateway allows the API to be called per second (RPS).
        """
        return pulumi.get(self, "burst_limit")

    @property
    @pulumi.getter(name="rateLimit")
    def rate_limit(self) -> Optional[float]:
        """
        The number of times API Gateway allows the API to be called per second on average (RPS).
        """
        return pulumi.get(self, "rate_limit")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class DocumentationPartLocation(dict):
    def __init__(__self__, *,
                 type: str,
                 method: Optional[str] = None,
                 name: Optional[str] = None,
                 path: Optional[str] = None,
                 status_code: Optional[str] = None):
        """
        :param str type: The type of API entity to which the documentation content applies. e.g. `API`, `METHOD` or `REQUEST_BODY`
        :param str method: The HTTP verb of a method. The default value is `*` for any method.
        :param str name: The name of the targeted API entity.
        :param str path: The URL path of the target. The default value is `/` for the root resource.
        :param str status_code: The HTTP status code of a response. The default value is `*` for any status code.
        """
        pulumi.set(__self__, "type", type)
        if method is not None:
            pulumi.set(__self__, "method", method)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if path is not None:
            pulumi.set(__self__, "path", path)
        if status_code is not None:
            pulumi.set(__self__, "status_code", status_code)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of API entity to which the documentation content applies. e.g. `API`, `METHOD` or `REQUEST_BODY`
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def method(self) -> Optional[str]:
        """
        The HTTP verb of a method. The default value is `*` for any method.
        """
        return pulumi.get(self, "method")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the targeted API entity.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def path(self) -> Optional[str]:
        """
        The URL path of the target. The default value is `/` for the root resource.
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter(name="statusCode")
    def status_code(self) -> Optional[str]:
        """
        The HTTP status code of a response. The default value is `*` for any status code.
        """
        return pulumi.get(self, "status_code")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class DomainNameEndpointConfiguration(dict):
    def __init__(__self__, *,
                 types: str):
        """
        :param str types: A list of endpoint types. This resource currently only supports managing a single value. Valid values: `EDGE` or `REGIONAL`. If unspecified, defaults to `EDGE`. Must be declared as `REGIONAL` in non-Commercial partitions. Refer to the [documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/create-regional-api.html) for more information on the difference between edge-optimized and regional APIs.
        """
        pulumi.set(__self__, "types", types)

    @property
    @pulumi.getter
    def types(self) -> str:
        """
        A list of endpoint types. This resource currently only supports managing a single value. Valid values: `EDGE` or `REGIONAL`. If unspecified, defaults to `EDGE`. Must be declared as `REGIONAL` in non-Commercial partitions. Refer to the [documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/create-regional-api.html) for more information on the difference between edge-optimized and regional APIs.
        """
        return pulumi.get(self, "types")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class MethodSettingsSettings(dict):
    def __init__(__self__, *,
                 cache_data_encrypted: Optional[bool] = None,
                 cache_ttl_in_seconds: Optional[float] = None,
                 caching_enabled: Optional[bool] = None,
                 data_trace_enabled: Optional[bool] = None,
                 logging_level: Optional[str] = None,
                 metrics_enabled: Optional[bool] = None,
                 require_authorization_for_cache_control: Optional[bool] = None,
                 throttling_burst_limit: Optional[float] = None,
                 throttling_rate_limit: Optional[float] = None,
                 unauthorized_cache_control_header_strategy: Optional[str] = None):
        """
        :param bool cache_data_encrypted: Specifies whether the cached responses are encrypted.
        :param float cache_ttl_in_seconds: Specifies the time to live (TTL), in seconds, for cached responses. The higher the TTL, the longer the response will be cached.
        :param bool caching_enabled: Specifies whether responses should be cached and returned for requests. A cache cluster must be enabled on the stage for responses to be cached.
        :param bool data_trace_enabled: Specifies whether data trace logging is enabled for this method, which effects the log entries pushed to Amazon CloudWatch Logs.
        :param str logging_level: Specifies the logging level for this method, which effects the log entries pushed to Amazon CloudWatch Logs. The available levels are `OFF`, `ERROR`, and `INFO`.
        :param bool metrics_enabled: Specifies whether Amazon CloudWatch metrics are enabled for this method.
        :param bool require_authorization_for_cache_control: Specifies whether authorization is required for a cache invalidation request.
        :param float throttling_burst_limit: Specifies the throttling burst limit. Default: `-1` (throttling disabled).
        :param float throttling_rate_limit: Specifies the throttling rate limit. Default: `-1` (throttling disabled).
        :param str unauthorized_cache_control_header_strategy: Specifies how to handle unauthorized requests for cache invalidation. The available values are `FAIL_WITH_403`, `SUCCEED_WITH_RESPONSE_HEADER`, `SUCCEED_WITHOUT_RESPONSE_HEADER`.
        """
        if cache_data_encrypted is not None:
            pulumi.set(__self__, "cache_data_encrypted", cache_data_encrypted)
        if cache_ttl_in_seconds is not None:
            pulumi.set(__self__, "cache_ttl_in_seconds", cache_ttl_in_seconds)
        if caching_enabled is not None:
            pulumi.set(__self__, "caching_enabled", caching_enabled)
        if data_trace_enabled is not None:
            pulumi.set(__self__, "data_trace_enabled", data_trace_enabled)
        if logging_level is not None:
            pulumi.set(__self__, "logging_level", logging_level)
        if metrics_enabled is not None:
            pulumi.set(__self__, "metrics_enabled", metrics_enabled)
        if require_authorization_for_cache_control is not None:
            pulumi.set(__self__, "require_authorization_for_cache_control", require_authorization_for_cache_control)
        if throttling_burst_limit is not None:
            pulumi.set(__self__, "throttling_burst_limit", throttling_burst_limit)
        if throttling_rate_limit is not None:
            pulumi.set(__self__, "throttling_rate_limit", throttling_rate_limit)
        if unauthorized_cache_control_header_strategy is not None:
            pulumi.set(__self__, "unauthorized_cache_control_header_strategy", unauthorized_cache_control_header_strategy)

    @property
    @pulumi.getter(name="cacheDataEncrypted")
    def cache_data_encrypted(self) -> Optional[bool]:
        """
        Specifies whether the cached responses are encrypted.
        """
        return pulumi.get(self, "cache_data_encrypted")

    @property
    @pulumi.getter(name="cacheTtlInSeconds")
    def cache_ttl_in_seconds(self) -> Optional[float]:
        """
        Specifies the time to live (TTL), in seconds, for cached responses. The higher the TTL, the longer the response will be cached.
        """
        return pulumi.get(self, "cache_ttl_in_seconds")

    @property
    @pulumi.getter(name="cachingEnabled")
    def caching_enabled(self) -> Optional[bool]:
        """
        Specifies whether responses should be cached and returned for requests. A cache cluster must be enabled on the stage for responses to be cached.
        """
        return pulumi.get(self, "caching_enabled")

    @property
    @pulumi.getter(name="dataTraceEnabled")
    def data_trace_enabled(self) -> Optional[bool]:
        """
        Specifies whether data trace logging is enabled for this method, which effects the log entries pushed to Amazon CloudWatch Logs.
        """
        return pulumi.get(self, "data_trace_enabled")

    @property
    @pulumi.getter(name="loggingLevel")
    def logging_level(self) -> Optional[str]:
        """
        Specifies the logging level for this method, which effects the log entries pushed to Amazon CloudWatch Logs. The available levels are `OFF`, `ERROR`, and `INFO`.
        """
        return pulumi.get(self, "logging_level")

    @property
    @pulumi.getter(name="metricsEnabled")
    def metrics_enabled(self) -> Optional[bool]:
        """
        Specifies whether Amazon CloudWatch metrics are enabled for this method.
        """
        return pulumi.get(self, "metrics_enabled")

    @property
    @pulumi.getter(name="requireAuthorizationForCacheControl")
    def require_authorization_for_cache_control(self) -> Optional[bool]:
        """
        Specifies whether authorization is required for a cache invalidation request.
        """
        return pulumi.get(self, "require_authorization_for_cache_control")

    @property
    @pulumi.getter(name="throttlingBurstLimit")
    def throttling_burst_limit(self) -> Optional[float]:
        """
        Specifies the throttling burst limit. Default: `-1` (throttling disabled).
        """
        return pulumi.get(self, "throttling_burst_limit")

    @property
    @pulumi.getter(name="throttlingRateLimit")
    def throttling_rate_limit(self) -> Optional[float]:
        """
        Specifies the throttling rate limit. Default: `-1` (throttling disabled).
        """
        return pulumi.get(self, "throttling_rate_limit")

    @property
    @pulumi.getter(name="unauthorizedCacheControlHeaderStrategy")
    def unauthorized_cache_control_header_strategy(self) -> Optional[str]:
        """
        Specifies how to handle unauthorized requests for cache invalidation. The available values are `FAIL_WITH_403`, `SUCCEED_WITH_RESPONSE_HEADER`, `SUCCEED_WITHOUT_RESPONSE_HEADER`.
        """
        return pulumi.get(self, "unauthorized_cache_control_header_strategy")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class RestApiEndpointConfiguration(dict):
    def __init__(__self__, *,
                 types: str,
                 vpc_endpoint_ids: Optional[List[str]] = None):
        """
        :param str types: A list of endpoint types. This resource currently only supports managing a single value. Valid values: `EDGE`, `REGIONAL` or `PRIVATE`. If unspecified, defaults to `EDGE`. Must be declared as `REGIONAL` in non-Commercial partitions. Refer to the [documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/create-regional-api.html) for more information on the difference between edge-optimized and regional APIs.
        :param List[str] vpc_endpoint_ids: A list of VPC Endpoint Ids. It is only supported for PRIVATE endpoint type.
        """
        pulumi.set(__self__, "types", types)
        if vpc_endpoint_ids is not None:
            pulumi.set(__self__, "vpc_endpoint_ids", vpc_endpoint_ids)

    @property
    @pulumi.getter
    def types(self) -> str:
        """
        A list of endpoint types. This resource currently only supports managing a single value. Valid values: `EDGE`, `REGIONAL` or `PRIVATE`. If unspecified, defaults to `EDGE`. Must be declared as `REGIONAL` in non-Commercial partitions. Refer to the [documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/create-regional-api.html) for more information on the difference between edge-optimized and regional APIs.
        """
        return pulumi.get(self, "types")

    @property
    @pulumi.getter(name="vpcEndpointIds")
    def vpc_endpoint_ids(self) -> Optional[List[str]]:
        """
        A list of VPC Endpoint Ids. It is only supported for PRIVATE endpoint type.
        """
        return pulumi.get(self, "vpc_endpoint_ids")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class StageAccessLogSettings(dict):
    def __init__(__self__, *,
                 destination_arn: str,
                 format: str):
        """
        :param str destination_arn: The Amazon Resource Name (ARN) of the CloudWatch Logs log group or Kinesis Data Firehose delivery stream to receive access logs. If you specify a Kinesis Data Firehose delivery stream, the stream name must begin with `amazon-apigateway-`. Automatically removes trailing `:*` if present.
        :param str format: The formatting and values recorded in the logs. 
               For more information on configuring the log format rules visit the AWS [documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-logging.html)
        """
        pulumi.set(__self__, "destination_arn", destination_arn)
        pulumi.set(__self__, "format", format)

    @property
    @pulumi.getter(name="destinationArn")
    def destination_arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of the CloudWatch Logs log group or Kinesis Data Firehose delivery stream to receive access logs. If you specify a Kinesis Data Firehose delivery stream, the stream name must begin with `amazon-apigateway-`. Automatically removes trailing `:*` if present.
        """
        return pulumi.get(self, "destination_arn")

    @property
    @pulumi.getter
    def format(self) -> str:
        """
        The formatting and values recorded in the logs. 
        For more information on configuring the log format rules visit the AWS [documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-logging.html)
        """
        return pulumi.get(self, "format")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class UsagePlanApiStage(dict):
    def __init__(__self__, *,
                 api_id: str,
                 stage: str):
        """
        :param str api_id: API Id of the associated API stage in a usage plan.
        :param str stage: API stage name of the associated API stage in a usage plan.
        """
        pulumi.set(__self__, "api_id", api_id)
        pulumi.set(__self__, "stage", stage)

    @property
    @pulumi.getter(name="apiId")
    def api_id(self) -> str:
        """
        API Id of the associated API stage in a usage plan.
        """
        return pulumi.get(self, "api_id")

    @property
    @pulumi.getter
    def stage(self) -> str:
        """
        API stage name of the associated API stage in a usage plan.
        """
        return pulumi.get(self, "stage")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class UsagePlanQuotaSettings(dict):
    def __init__(__self__, *,
                 limit: float,
                 period: str,
                 offset: Optional[float] = None):
        """
        :param float limit: The maximum number of requests that can be made in a given time period.
        :param str period: The time period in which the limit applies. Valid values are "DAY", "WEEK" or "MONTH".
        :param float offset: The number of requests subtracted from the given limit in the initial time period.
        """
        pulumi.set(__self__, "limit", limit)
        pulumi.set(__self__, "period", period)
        if offset is not None:
            pulumi.set(__self__, "offset", offset)

    @property
    @pulumi.getter
    def limit(self) -> float:
        """
        The maximum number of requests that can be made in a given time period.
        """
        return pulumi.get(self, "limit")

    @property
    @pulumi.getter
    def period(self) -> str:
        """
        The time period in which the limit applies. Valid values are "DAY", "WEEK" or "MONTH".
        """
        return pulumi.get(self, "period")

    @property
    @pulumi.getter
    def offset(self) -> Optional[float]:
        """
        The number of requests subtracted from the given limit in the initial time period.
        """
        return pulumi.get(self, "offset")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class UsagePlanThrottleSettings(dict):
    def __init__(__self__, *,
                 burst_limit: Optional[float] = None,
                 rate_limit: Optional[float] = None):
        """
        :param float burst_limit: The API request burst limit, the maximum rate limit over a time ranging from one to a few seconds, depending upon whether the underlying token bucket is at its full capacity.
        :param float rate_limit: The API request steady-state rate limit.
        """
        if burst_limit is not None:
            pulumi.set(__self__, "burst_limit", burst_limit)
        if rate_limit is not None:
            pulumi.set(__self__, "rate_limit", rate_limit)

    @property
    @pulumi.getter(name="burstLimit")
    def burst_limit(self) -> Optional[float]:
        """
        The API request burst limit, the maximum rate limit over a time ranging from one to a few seconds, depending upon whether the underlying token bucket is at its full capacity.
        """
        return pulumi.get(self, "burst_limit")

    @property
    @pulumi.getter(name="rateLimit")
    def rate_limit(self) -> Optional[float]:
        """
        The API request steady-state rate limit.
        """
        return pulumi.get(self, "rate_limit")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class GetRestApiEndpointConfigurationResult(dict):
    def __init__(__self__, *,
                 types: List[str],
                 vpc_endpoint_ids: List[str]):
        pulumi.set(__self__, "types", types)
        pulumi.set(__self__, "vpc_endpoint_ids", vpc_endpoint_ids)

    @property
    @pulumi.getter
    def types(self) -> List[str]:
        return pulumi.get(self, "types")

    @property
    @pulumi.getter(name="vpcEndpointIds")
    def vpc_endpoint_ids(self) -> List[str]:
        return pulumi.get(self, "vpc_endpoint_ids")


