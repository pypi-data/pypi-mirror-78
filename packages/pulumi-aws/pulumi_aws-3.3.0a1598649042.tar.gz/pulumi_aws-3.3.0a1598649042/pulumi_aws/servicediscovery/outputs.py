# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables
from . import outputs

__all__ = [
    'ServiceDnsConfig',
    'ServiceDnsConfigDnsRecord',
    'ServiceHealthCheckConfig',
    'ServiceHealthCheckCustomConfig',
]

@pulumi.output_type
class ServiceDnsConfig(dict):
    def __init__(__self__, *,
                 dns_records: List['outputs.ServiceDnsConfigDnsRecord'],
                 namespace_id: str,
                 routing_policy: Optional[str] = None):
        """
        :param List['ServiceDnsConfigDnsRecordArgs'] dns_records: An array that contains one DnsRecord object for each resource record set.
        :param str namespace_id: The ID of the namespace to use for DNS configuration.
        :param str routing_policy: The routing policy that you want to apply to all records that Route 53 creates when you register an instance and specify the service. Valid Values: MULTIVALUE, WEIGHTED
        """
        pulumi.set(__self__, "dns_records", dns_records)
        pulumi.set(__self__, "namespace_id", namespace_id)
        if routing_policy is not None:
            pulumi.set(__self__, "routing_policy", routing_policy)

    @property
    @pulumi.getter(name="dnsRecords")
    def dns_records(self) -> List['outputs.ServiceDnsConfigDnsRecord']:
        """
        An array that contains one DnsRecord object for each resource record set.
        """
        return pulumi.get(self, "dns_records")

    @property
    @pulumi.getter(name="namespaceId")
    def namespace_id(self) -> str:
        """
        The ID of the namespace to use for DNS configuration.
        """
        return pulumi.get(self, "namespace_id")

    @property
    @pulumi.getter(name="routingPolicy")
    def routing_policy(self) -> Optional[str]:
        """
        The routing policy that you want to apply to all records that Route 53 creates when you register an instance and specify the service. Valid Values: MULTIVALUE, WEIGHTED
        """
        return pulumi.get(self, "routing_policy")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ServiceDnsConfigDnsRecord(dict):
    def __init__(__self__, *,
                 ttl: float,
                 type: str):
        """
        :param float ttl: The amount of time, in seconds, that you want DNS resolvers to cache the settings for this resource record set.
        :param str type: The type of health check that you want to create, which indicates how Route 53 determines whether an endpoint is healthy. Valid Values: HTTP, HTTPS, TCP
        """
        pulumi.set(__self__, "ttl", ttl)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def ttl(self) -> float:
        """
        The amount of time, in seconds, that you want DNS resolvers to cache the settings for this resource record set.
        """
        return pulumi.get(self, "ttl")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of health check that you want to create, which indicates how Route 53 determines whether an endpoint is healthy. Valid Values: HTTP, HTTPS, TCP
        """
        return pulumi.get(self, "type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ServiceHealthCheckConfig(dict):
    def __init__(__self__, *,
                 failure_threshold: Optional[float] = None,
                 resource_path: Optional[str] = None,
                 type: Optional[str] = None):
        """
        :param float failure_threshold: The number of 30-second intervals that you want service discovery to wait before it changes the health status of a service instance.  Maximum value of 10.
        :param str resource_path: The path that you want Route 53 to request when performing health checks. Route 53 automatically adds the DNS name for the service. If you don't specify a value, the default value is /.
        :param str type: The type of health check that you want to create, which indicates how Route 53 determines whether an endpoint is healthy. Valid Values: HTTP, HTTPS, TCP
        """
        if failure_threshold is not None:
            pulumi.set(__self__, "failure_threshold", failure_threshold)
        if resource_path is not None:
            pulumi.set(__self__, "resource_path", resource_path)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="failureThreshold")
    def failure_threshold(self) -> Optional[float]:
        """
        The number of 30-second intervals that you want service discovery to wait before it changes the health status of a service instance.  Maximum value of 10.
        """
        return pulumi.get(self, "failure_threshold")

    @property
    @pulumi.getter(name="resourcePath")
    def resource_path(self) -> Optional[str]:
        """
        The path that you want Route 53 to request when performing health checks. Route 53 automatically adds the DNS name for the service. If you don't specify a value, the default value is /.
        """
        return pulumi.get(self, "resource_path")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The type of health check that you want to create, which indicates how Route 53 determines whether an endpoint is healthy. Valid Values: HTTP, HTTPS, TCP
        """
        return pulumi.get(self, "type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ServiceHealthCheckCustomConfig(dict):
    def __init__(__self__, *,
                 failure_threshold: Optional[float] = None):
        """
        :param float failure_threshold: The number of 30-second intervals that you want service discovery to wait before it changes the health status of a service instance.  Maximum value of 10.
        """
        if failure_threshold is not None:
            pulumi.set(__self__, "failure_threshold", failure_threshold)

    @property
    @pulumi.getter(name="failureThreshold")
    def failure_threshold(self) -> Optional[float]:
        """
        The number of 30-second intervals that you want service discovery to wait before it changes the health status of a service instance.  Maximum value of 10.
        """
        return pulumi.get(self, "failure_threshold")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


