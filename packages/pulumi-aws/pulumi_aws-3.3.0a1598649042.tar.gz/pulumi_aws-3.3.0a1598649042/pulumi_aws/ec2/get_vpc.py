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

__all__ = [
    'GetVpcResult',
    'AwaitableGetVpcResult',
    'get_vpc',
]

@pulumi.output_type
class GetVpcResult:
    """
    A collection of values returned by getVpc.
    """
    def __init__(__self__, arn=None, cidr_block=None, cidr_block_associations=None, default=None, dhcp_options_id=None, enable_dns_hostnames=None, enable_dns_support=None, filters=None, id=None, instance_tenancy=None, ipv6_association_id=None, ipv6_cidr_block=None, main_route_table_id=None, owner_id=None, state=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if cidr_block and not isinstance(cidr_block, str):
            raise TypeError("Expected argument 'cidr_block' to be a str")
        pulumi.set(__self__, "cidr_block", cidr_block)
        if cidr_block_associations and not isinstance(cidr_block_associations, list):
            raise TypeError("Expected argument 'cidr_block_associations' to be a list")
        pulumi.set(__self__, "cidr_block_associations", cidr_block_associations)
        if default and not isinstance(default, bool):
            raise TypeError("Expected argument 'default' to be a bool")
        pulumi.set(__self__, "default", default)
        if dhcp_options_id and not isinstance(dhcp_options_id, str):
            raise TypeError("Expected argument 'dhcp_options_id' to be a str")
        pulumi.set(__self__, "dhcp_options_id", dhcp_options_id)
        if enable_dns_hostnames and not isinstance(enable_dns_hostnames, bool):
            raise TypeError("Expected argument 'enable_dns_hostnames' to be a bool")
        pulumi.set(__self__, "enable_dns_hostnames", enable_dns_hostnames)
        if enable_dns_support and not isinstance(enable_dns_support, bool):
            raise TypeError("Expected argument 'enable_dns_support' to be a bool")
        pulumi.set(__self__, "enable_dns_support", enable_dns_support)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_tenancy and not isinstance(instance_tenancy, str):
            raise TypeError("Expected argument 'instance_tenancy' to be a str")
        pulumi.set(__self__, "instance_tenancy", instance_tenancy)
        if ipv6_association_id and not isinstance(ipv6_association_id, str):
            raise TypeError("Expected argument 'ipv6_association_id' to be a str")
        pulumi.set(__self__, "ipv6_association_id", ipv6_association_id)
        if ipv6_cidr_block and not isinstance(ipv6_cidr_block, str):
            raise TypeError("Expected argument 'ipv6_cidr_block' to be a str")
        pulumi.set(__self__, "ipv6_cidr_block", ipv6_cidr_block)
        if main_route_table_id and not isinstance(main_route_table_id, str):
            raise TypeError("Expected argument 'main_route_table_id' to be a str")
        pulumi.set(__self__, "main_route_table_id", main_route_table_id)
        if owner_id and not isinstance(owner_id, str):
            raise TypeError("Expected argument 'owner_id' to be a str")
        pulumi.set(__self__, "owner_id", owner_id)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        Amazon Resource Name (ARN) of VPC
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> str:
        """
        The CIDR block for the association.
        """
        return pulumi.get(self, "cidr_block")

    @property
    @pulumi.getter(name="cidrBlockAssociations")
    def cidr_block_associations(self) -> List['outputs.GetVpcCidrBlockAssociationResult']:
        return pulumi.get(self, "cidr_block_associations")

    @property
    @pulumi.getter
    def default(self) -> bool:
        return pulumi.get(self, "default")

    @property
    @pulumi.getter(name="dhcpOptionsId")
    def dhcp_options_id(self) -> str:
        return pulumi.get(self, "dhcp_options_id")

    @property
    @pulumi.getter(name="enableDnsHostnames")
    def enable_dns_hostnames(self) -> bool:
        """
        Whether or not the VPC has DNS hostname support
        """
        return pulumi.get(self, "enable_dns_hostnames")

    @property
    @pulumi.getter(name="enableDnsSupport")
    def enable_dns_support(self) -> bool:
        """
        Whether or not the VPC has DNS support
        """
        return pulumi.get(self, "enable_dns_support")

    @property
    @pulumi.getter
    def filters(self) -> Optional[List['outputs.GetVpcFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="instanceTenancy")
    def instance_tenancy(self) -> str:
        """
        The allowed tenancy of instances launched into the
        selected VPC. May be any of `"default"`, `"dedicated"`, or `"host"`.
        """
        return pulumi.get(self, "instance_tenancy")

    @property
    @pulumi.getter(name="ipv6AssociationId")
    def ipv6_association_id(self) -> str:
        """
        The association ID for the IPv6 CIDR block.
        """
        return pulumi.get(self, "ipv6_association_id")

    @property
    @pulumi.getter(name="ipv6CidrBlock")
    def ipv6_cidr_block(self) -> str:
        """
        The IPv6 CIDR block.
        """
        return pulumi.get(self, "ipv6_cidr_block")

    @property
    @pulumi.getter(name="mainRouteTableId")
    def main_route_table_id(self) -> str:
        """
        The ID of the main route table associated with this VPC.
        """
        return pulumi.get(self, "main_route_table_id")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> str:
        """
        The ID of the AWS account that owns the VPC.
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The State of the association.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")


class AwaitableGetVpcResult(GetVpcResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVpcResult(
            arn=self.arn,
            cidr_block=self.cidr_block,
            cidr_block_associations=self.cidr_block_associations,
            default=self.default,
            dhcp_options_id=self.dhcp_options_id,
            enable_dns_hostnames=self.enable_dns_hostnames,
            enable_dns_support=self.enable_dns_support,
            filters=self.filters,
            id=self.id,
            instance_tenancy=self.instance_tenancy,
            ipv6_association_id=self.ipv6_association_id,
            ipv6_cidr_block=self.ipv6_cidr_block,
            main_route_table_id=self.main_route_table_id,
            owner_id=self.owner_id,
            state=self.state,
            tags=self.tags)


def get_vpc(cidr_block: Optional[str] = None,
            default: Optional[bool] = None,
            dhcp_options_id: Optional[str] = None,
            filters: Optional[List[pulumi.InputType['GetVpcFilterArgs']]] = None,
            id: Optional[str] = None,
            state: Optional[str] = None,
            tags: Optional[Mapping[str, str]] = None,
            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVpcResult:
    """
    `ec2.Vpc` provides details about a specific VPC.

    This resource can prove useful when a module accepts a vpc id as
    an input variable and needs to, for example, determine the CIDR block of that
    VPC.


    :param str cidr_block: The cidr block of the desired VPC.
    :param bool default: Boolean constraint on whether the desired VPC is
           the default VPC for the region.
    :param str dhcp_options_id: The DHCP options id of the desired VPC.
    :param List[pulumi.InputType['GetVpcFilterArgs']] filters: Custom filter block as described below.
    :param str id: The id of the specific VPC to retrieve.
    :param str state: The current state of the desired VPC.
           Can be either `"pending"` or `"available"`.
    :param Mapping[str, str] tags: A map of tags, each pair of which must exactly match
           a pair on the desired VPC.
    """
    __args__ = dict()
    __args__['cidrBlock'] = cidr_block
    __args__['default'] = default
    __args__['dhcpOptionsId'] = dhcp_options_id
    __args__['filters'] = filters
    __args__['id'] = id
    __args__['state'] = state
    __args__['tags'] = tags
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:ec2/getVpc:getVpc', __args__, opts=opts, typ=GetVpcResult).value

    return AwaitableGetVpcResult(
        arn=__ret__.arn,
        cidr_block=__ret__.cidr_block,
        cidr_block_associations=__ret__.cidr_block_associations,
        default=__ret__.default,
        dhcp_options_id=__ret__.dhcp_options_id,
        enable_dns_hostnames=__ret__.enable_dns_hostnames,
        enable_dns_support=__ret__.enable_dns_support,
        filters=__ret__.filters,
        id=__ret__.id,
        instance_tenancy=__ret__.instance_tenancy,
        ipv6_association_id=__ret__.ipv6_association_id,
        ipv6_cidr_block=__ret__.ipv6_cidr_block,
        main_route_table_id=__ret__.main_route_table_id,
        owner_id=__ret__.owner_id,
        state=__ret__.state,
        tags=__ret__.tags)
