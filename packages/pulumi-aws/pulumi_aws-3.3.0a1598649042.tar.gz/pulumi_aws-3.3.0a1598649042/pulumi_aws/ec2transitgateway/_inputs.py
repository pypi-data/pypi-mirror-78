# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'GetDirectConnectGatewayAttachmentFilterArgs',
    'GetPeeringAttachmentFilterArgs',
    'GetRouteTableFilterArgs',
    'GetTransitGatewayFilterArgs',
    'GetVpcAttachmentFilterArgs',
    'GetVpnAttachmentFilterArgs',
]

@pulumi.input_type
class GetDirectConnectGatewayAttachmentFilterArgs:
    def __init__(__self__, *,
                 name: str,
                 values: List[str]):
        """
        :param str name: The name of the filter field. Valid values can be found in the [EC2 DescribeTransitGatewayAttachments API Reference](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeTransitGatewayAttachments.html).
        :param List[str] values: Set of values that are accepted for the given filter field. Results will be selected if any given value matches.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the filter field. Valid values can be found in the [EC2 DescribeTransitGatewayAttachments API Reference](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeTransitGatewayAttachments.html).
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: str):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def values(self) -> List[str]:
        """
        Set of values that are accepted for the given filter field. Results will be selected if any given value matches.
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: List[str]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class GetPeeringAttachmentFilterArgs:
    def __init__(__self__, *,
                 name: str,
                 values: List[str]):
        """
        :param str name: The name of the field to filter by, as defined by
               [the underlying AWS API](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeTransitGatewayPeeringAttachments.html).
        :param List[str] values: Set of values that are accepted for the given field.
               An EC2 Transit Gateway Peering Attachment be selected if any one of the given values matches.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the field to filter by, as defined by
        [the underlying AWS API](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeTransitGatewayPeeringAttachments.html).
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: str):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def values(self) -> List[str]:
        """
        Set of values that are accepted for the given field.
        An EC2 Transit Gateway Peering Attachment be selected if any one of the given values matches.
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: List[str]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class GetRouteTableFilterArgs:
    def __init__(__self__, *,
                 name: str,
                 values: List[str]):
        """
        :param str name: Name of the filter.
        :param List[str] values: List of one or more values for the filter.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the filter.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: str):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def values(self) -> List[str]:
        """
        List of one or more values for the filter.
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: List[str]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class GetTransitGatewayFilterArgs:
    def __init__(__self__, *,
                 name: str,
                 values: List[str]):
        """
        :param str name: Name of the filter.
        :param List[str] values: List of one or more values for the filter.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the filter.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: str):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def values(self) -> List[str]:
        """
        List of one or more values for the filter.
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: List[str]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class GetVpcAttachmentFilterArgs:
    def __init__(__self__, *,
                 name: str,
                 values: List[str]):
        """
        :param str name: Name of the filter.
        :param List[str] values: List of one or more values for the filter.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the filter.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: str):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def values(self) -> List[str]:
        """
        List of one or more values for the filter.
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: List[str]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class GetVpnAttachmentFilterArgs:
    def __init__(__self__, *,
                 name: str,
                 values: List[str]):
        """
        :param str name: The name of the filter field. Valid values can be found in the [EC2 DescribeTransitGatewayAttachments API Reference](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeTransitGatewayAttachments.html).
        :param List[str] values: Set of values that are accepted for the given filter field. Results will be selected if any given value matches.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the filter field. Valid values can be found in the [EC2 DescribeTransitGatewayAttachments API Reference](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeTransitGatewayAttachments.html).
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: str):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def values(self) -> List[str]:
        """
        Set of values that are accepted for the given filter field. Results will be selected if any given value matches.
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: List[str]):
        pulumi.set(self, "values", value)


