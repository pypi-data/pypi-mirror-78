# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'EndpointElasticsearchSettingsArgs',
    'EndpointKafkaSettingsArgs',
    'EndpointKinesisSettingsArgs',
    'EndpointMongodbSettingsArgs',
    'EndpointS3SettingsArgs',
]

@pulumi.input_type
class EndpointElasticsearchSettingsArgs:
    def __init__(__self__, *,
                 endpoint_uri: pulumi.Input[str],
                 service_access_role_arn: pulumi.Input[str],
                 error_retry_duration: Optional[pulumi.Input[float]] = None,
                 full_load_error_percentage: Optional[pulumi.Input[float]] = None):
        """
        :param pulumi.Input[str] endpoint_uri: Endpoint for the Elasticsearch cluster.
        :param pulumi.Input[str] service_access_role_arn: Amazon Resource Name (ARN) of the IAM Role with permissions to write to the Elasticsearch cluster.
        :param pulumi.Input[float] error_retry_duration: Maximum number of seconds for which DMS retries failed API requests to the Elasticsearch cluster. Defaults to `300`.
        :param pulumi.Input[float] full_load_error_percentage: Maximum percentage of records that can fail to be written before a full load operation stops. Defaults to `10`.
        """
        pulumi.set(__self__, "endpoint_uri", endpoint_uri)
        pulumi.set(__self__, "service_access_role_arn", service_access_role_arn)
        if error_retry_duration is not None:
            pulumi.set(__self__, "error_retry_duration", error_retry_duration)
        if full_load_error_percentage is not None:
            pulumi.set(__self__, "full_load_error_percentage", full_load_error_percentage)

    @property
    @pulumi.getter(name="endpointUri")
    def endpoint_uri(self) -> pulumi.Input[str]:
        """
        Endpoint for the Elasticsearch cluster.
        """
        return pulumi.get(self, "endpoint_uri")

    @endpoint_uri.setter
    def endpoint_uri(self, value: pulumi.Input[str]):
        pulumi.set(self, "endpoint_uri", value)

    @property
    @pulumi.getter(name="serviceAccessRoleArn")
    def service_access_role_arn(self) -> pulumi.Input[str]:
        """
        Amazon Resource Name (ARN) of the IAM Role with permissions to write to the Elasticsearch cluster.
        """
        return pulumi.get(self, "service_access_role_arn")

    @service_access_role_arn.setter
    def service_access_role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_access_role_arn", value)

    @property
    @pulumi.getter(name="errorRetryDuration")
    def error_retry_duration(self) -> Optional[pulumi.Input[float]]:
        """
        Maximum number of seconds for which DMS retries failed API requests to the Elasticsearch cluster. Defaults to `300`.
        """
        return pulumi.get(self, "error_retry_duration")

    @error_retry_duration.setter
    def error_retry_duration(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "error_retry_duration", value)

    @property
    @pulumi.getter(name="fullLoadErrorPercentage")
    def full_load_error_percentage(self) -> Optional[pulumi.Input[float]]:
        """
        Maximum percentage of records that can fail to be written before a full load operation stops. Defaults to `10`.
        """
        return pulumi.get(self, "full_load_error_percentage")

    @full_load_error_percentage.setter
    def full_load_error_percentage(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "full_load_error_percentage", value)


@pulumi.input_type
class EndpointKafkaSettingsArgs:
    def __init__(__self__, *,
                 broker: pulumi.Input[str],
                 topic: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] broker: Kafka broker location. Specify in the form broker-hostname-or-ip:port.
        :param pulumi.Input[str] topic: Kafka topic for migration. Defaults to `kafka-default-topic`.
        """
        pulumi.set(__self__, "broker", broker)
        if topic is not None:
            pulumi.set(__self__, "topic", topic)

    @property
    @pulumi.getter
    def broker(self) -> pulumi.Input[str]:
        """
        Kafka broker location. Specify in the form broker-hostname-or-ip:port.
        """
        return pulumi.get(self, "broker")

    @broker.setter
    def broker(self, value: pulumi.Input[str]):
        pulumi.set(self, "broker", value)

    @property
    @pulumi.getter
    def topic(self) -> Optional[pulumi.Input[str]]:
        """
        Kafka topic for migration. Defaults to `kafka-default-topic`.
        """
        return pulumi.get(self, "topic")

    @topic.setter
    def topic(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "topic", value)


@pulumi.input_type
class EndpointKinesisSettingsArgs:
    def __init__(__self__, *,
                 message_format: Optional[pulumi.Input[str]] = None,
                 service_access_role_arn: Optional[pulumi.Input[str]] = None,
                 stream_arn: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] message_format: Output format for the records created. Defaults to `json`. Valid values are `json` and `json_unformatted` (a single line with no tab).
        :param pulumi.Input[str] service_access_role_arn: Amazon Resource Name (ARN) of the IAM Role with permissions to write to the Kinesis data stream.
        :param pulumi.Input[str] stream_arn: Amazon Resource Name (ARN) of the Kinesis data stream.
        """
        if message_format is not None:
            pulumi.set(__self__, "message_format", message_format)
        if service_access_role_arn is not None:
            pulumi.set(__self__, "service_access_role_arn", service_access_role_arn)
        if stream_arn is not None:
            pulumi.set(__self__, "stream_arn", stream_arn)

    @property
    @pulumi.getter(name="messageFormat")
    def message_format(self) -> Optional[pulumi.Input[str]]:
        """
        Output format for the records created. Defaults to `json`. Valid values are `json` and `json_unformatted` (a single line with no tab).
        """
        return pulumi.get(self, "message_format")

    @message_format.setter
    def message_format(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "message_format", value)

    @property
    @pulumi.getter(name="serviceAccessRoleArn")
    def service_access_role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the IAM Role with permissions to write to the Kinesis data stream.
        """
        return pulumi.get(self, "service_access_role_arn")

    @service_access_role_arn.setter
    def service_access_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_access_role_arn", value)

    @property
    @pulumi.getter(name="streamArn")
    def stream_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the Kinesis data stream.
        """
        return pulumi.get(self, "stream_arn")

    @stream_arn.setter
    def stream_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stream_arn", value)


@pulumi.input_type
class EndpointMongodbSettingsArgs:
    def __init__(__self__, *,
                 auth_mechanism: Optional[pulumi.Input[str]] = None,
                 auth_source: Optional[pulumi.Input[str]] = None,
                 auth_type: Optional[pulumi.Input[str]] = None,
                 docs_to_investigate: Optional[pulumi.Input[str]] = None,
                 extract_doc_id: Optional[pulumi.Input[str]] = None,
                 nesting_level: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] auth_mechanism: Authentication mechanism to access the MongoDB source endpoint. Defaults to `default`.
        :param pulumi.Input[str] auth_source: Authentication database name. Not used when `auth_type` is `no`. Defaults to `admin`.
        :param pulumi.Input[str] auth_type: Authentication type to access the MongoDB source endpoint. Defaults to `password`.
        :param pulumi.Input[str] docs_to_investigate: Number of documents to preview to determine the document organization. Use this setting when `nesting_level` is set to `one`. Defaults to `1000`.
        :param pulumi.Input[str] extract_doc_id: Document ID. Use this setting when `nesting_level` is set to `none`. Defaults to `false`.
        :param pulumi.Input[str] nesting_level: Specifies either document or table mode. Defaults to `none`. Valid values are `one` (table mode) and `none` (document mode).
        """
        if auth_mechanism is not None:
            pulumi.set(__self__, "auth_mechanism", auth_mechanism)
        if auth_source is not None:
            pulumi.set(__self__, "auth_source", auth_source)
        if auth_type is not None:
            pulumi.set(__self__, "auth_type", auth_type)
        if docs_to_investigate is not None:
            pulumi.set(__self__, "docs_to_investigate", docs_to_investigate)
        if extract_doc_id is not None:
            pulumi.set(__self__, "extract_doc_id", extract_doc_id)
        if nesting_level is not None:
            pulumi.set(__self__, "nesting_level", nesting_level)

    @property
    @pulumi.getter(name="authMechanism")
    def auth_mechanism(self) -> Optional[pulumi.Input[str]]:
        """
        Authentication mechanism to access the MongoDB source endpoint. Defaults to `default`.
        """
        return pulumi.get(self, "auth_mechanism")

    @auth_mechanism.setter
    def auth_mechanism(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "auth_mechanism", value)

    @property
    @pulumi.getter(name="authSource")
    def auth_source(self) -> Optional[pulumi.Input[str]]:
        """
        Authentication database name. Not used when `auth_type` is `no`. Defaults to `admin`.
        """
        return pulumi.get(self, "auth_source")

    @auth_source.setter
    def auth_source(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "auth_source", value)

    @property
    @pulumi.getter(name="authType")
    def auth_type(self) -> Optional[pulumi.Input[str]]:
        """
        Authentication type to access the MongoDB source endpoint. Defaults to `password`.
        """
        return pulumi.get(self, "auth_type")

    @auth_type.setter
    def auth_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "auth_type", value)

    @property
    @pulumi.getter(name="docsToInvestigate")
    def docs_to_investigate(self) -> Optional[pulumi.Input[str]]:
        """
        Number of documents to preview to determine the document organization. Use this setting when `nesting_level` is set to `one`. Defaults to `1000`.
        """
        return pulumi.get(self, "docs_to_investigate")

    @docs_to_investigate.setter
    def docs_to_investigate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "docs_to_investigate", value)

    @property
    @pulumi.getter(name="extractDocId")
    def extract_doc_id(self) -> Optional[pulumi.Input[str]]:
        """
        Document ID. Use this setting when `nesting_level` is set to `none`. Defaults to `false`.
        """
        return pulumi.get(self, "extract_doc_id")

    @extract_doc_id.setter
    def extract_doc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "extract_doc_id", value)

    @property
    @pulumi.getter(name="nestingLevel")
    def nesting_level(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies either document or table mode. Defaults to `none`. Valid values are `one` (table mode) and `none` (document mode).
        """
        return pulumi.get(self, "nesting_level")

    @nesting_level.setter
    def nesting_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "nesting_level", value)


@pulumi.input_type
class EndpointS3SettingsArgs:
    def __init__(__self__, *,
                 bucket_folder: Optional[pulumi.Input[str]] = None,
                 bucket_name: Optional[pulumi.Input[str]] = None,
                 compression_type: Optional[pulumi.Input[str]] = None,
                 csv_delimiter: Optional[pulumi.Input[str]] = None,
                 csv_row_delimiter: Optional[pulumi.Input[str]] = None,
                 external_table_definition: Optional[pulumi.Input[str]] = None,
                 service_access_role_arn: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] bucket_folder: S3 Bucket Object prefix.
        :param pulumi.Input[str] bucket_name: S3 Bucket name.
        :param pulumi.Input[str] compression_type: Set to compress target files. Defaults to `NONE`. Valid values are `GZIP` and `NONE`.
        :param pulumi.Input[str] csv_delimiter: Delimiter used to separate columns in the source files. Defaults to `,`.
        :param pulumi.Input[str] csv_row_delimiter: Delimiter used to separate rows in the source files. Defaults to `\n`.
        :param pulumi.Input[str] external_table_definition: JSON document that describes how AWS DMS should interpret the data.
        :param pulumi.Input[str] service_access_role_arn: Amazon Resource Name (ARN) of the IAM Role with permissions to read from or write to the S3 Bucket.
        """
        if bucket_folder is not None:
            pulumi.set(__self__, "bucket_folder", bucket_folder)
        if bucket_name is not None:
            pulumi.set(__self__, "bucket_name", bucket_name)
        if compression_type is not None:
            pulumi.set(__self__, "compression_type", compression_type)
        if csv_delimiter is not None:
            pulumi.set(__self__, "csv_delimiter", csv_delimiter)
        if csv_row_delimiter is not None:
            pulumi.set(__self__, "csv_row_delimiter", csv_row_delimiter)
        if external_table_definition is not None:
            pulumi.set(__self__, "external_table_definition", external_table_definition)
        if service_access_role_arn is not None:
            pulumi.set(__self__, "service_access_role_arn", service_access_role_arn)

    @property
    @pulumi.getter(name="bucketFolder")
    def bucket_folder(self) -> Optional[pulumi.Input[str]]:
        """
        S3 Bucket Object prefix.
        """
        return pulumi.get(self, "bucket_folder")

    @bucket_folder.setter
    def bucket_folder(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket_folder", value)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> Optional[pulumi.Input[str]]:
        """
        S3 Bucket name.
        """
        return pulumi.get(self, "bucket_name")

    @bucket_name.setter
    def bucket_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket_name", value)

    @property
    @pulumi.getter(name="compressionType")
    def compression_type(self) -> Optional[pulumi.Input[str]]:
        """
        Set to compress target files. Defaults to `NONE`. Valid values are `GZIP` and `NONE`.
        """
        return pulumi.get(self, "compression_type")

    @compression_type.setter
    def compression_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "compression_type", value)

    @property
    @pulumi.getter(name="csvDelimiter")
    def csv_delimiter(self) -> Optional[pulumi.Input[str]]:
        """
        Delimiter used to separate columns in the source files. Defaults to `,`.
        """
        return pulumi.get(self, "csv_delimiter")

    @csv_delimiter.setter
    def csv_delimiter(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "csv_delimiter", value)

    @property
    @pulumi.getter(name="csvRowDelimiter")
    def csv_row_delimiter(self) -> Optional[pulumi.Input[str]]:
        """
        Delimiter used to separate rows in the source files. Defaults to `\n`.
        """
        return pulumi.get(self, "csv_row_delimiter")

    @csv_row_delimiter.setter
    def csv_row_delimiter(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "csv_row_delimiter", value)

    @property
    @pulumi.getter(name="externalTableDefinition")
    def external_table_definition(self) -> Optional[pulumi.Input[str]]:
        """
        JSON document that describes how AWS DMS should interpret the data.
        """
        return pulumi.get(self, "external_table_definition")

    @external_table_definition.setter
    def external_table_definition(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "external_table_definition", value)

    @property
    @pulumi.getter(name="serviceAccessRoleArn")
    def service_access_role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the IAM Role with permissions to read from or write to the S3 Bucket.
        """
        return pulumi.get(self, "service_access_role_arn")

    @service_access_role_arn.setter
    def service_access_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_access_role_arn", value)


