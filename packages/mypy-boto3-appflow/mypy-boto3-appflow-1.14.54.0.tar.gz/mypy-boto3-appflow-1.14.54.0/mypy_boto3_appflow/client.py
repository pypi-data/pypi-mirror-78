# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin,too-many-locals,unused-import
"""
Main interface for appflow service client

Usage::

    ```python
    import boto3
    from mypy_boto3_appflow import AppflowClient

    client: AppflowClient = boto3.client("appflow")
    ```
"""
import sys
from typing import Any, Dict, List, Type

from botocore.client import ClientMeta
from botocore.exceptions import ClientError as Boto3ClientError

from mypy_boto3_appflow.type_defs import (
    ConnectorProfileConfigTypeDef,
    CreateConnectorProfileResponseTypeDef,
    CreateFlowResponseTypeDef,
    DescribeConnectorEntityResponseTypeDef,
    DescribeConnectorProfilesResponseTypeDef,
    DescribeConnectorsResponseTypeDef,
    DescribeFlowExecutionRecordsResponseTypeDef,
    DescribeFlowResponseTypeDef,
    DestinationFlowConfigTypeDef,
    ListConnectorEntitiesResponseTypeDef,
    ListFlowsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    SourceFlowConfigTypeDef,
    StartFlowResponseTypeDef,
    StopFlowResponseTypeDef,
    TaskTypeDef,
    TriggerConfigTypeDef,
    UpdateConnectorProfileResponseTypeDef,
    UpdateFlowResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AppflowClient",)


class Exceptions:
    ClientError: Type[Boto3ClientError]
    ConflictException: Type[Boto3ClientError]
    ConnectorAuthenticationException: Type[Boto3ClientError]
    ConnectorServerException: Type[Boto3ClientError]
    InternalServerException: Type[Boto3ClientError]
    ResourceNotFoundException: Type[Boto3ClientError]
    ServiceQuotaExceededException: Type[Boto3ClientError]
    UnsupportedOperationException: Type[Boto3ClientError]
    ValidationException: Type[Boto3ClientError]


class AppflowClient:
    """
    [Appflow.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.can_paginate)
        """

    def create_connector_profile(
        self,
        connectorProfileName: str,
        connectorType: Literal[
            "Salesforce",
            "Singular",
            "Slack",
            "Redshift",
            "S3",
            "Marketo",
            "Googleanalytics",
            "Zendesk",
            "Servicenow",
            "Datadog",
            "Trendmicro",
            "Snowflake",
            "Dynatrace",
            "Infornexus",
            "Amplitude",
            "Veeva",
            "EventBridge",
        ],
        connectionMode: Literal["Public", "Private"],
        connectorProfileConfig: ConnectorProfileConfigTypeDef,
        kmsArn: str = None,
    ) -> CreateConnectorProfileResponseTypeDef:
        """
        [Client.create_connector_profile documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.create_connector_profile)
        """

    def create_flow(
        self,
        flowName: str,
        triggerConfig: "TriggerConfigTypeDef",
        sourceFlowConfig: "SourceFlowConfigTypeDef",
        destinationFlowConfigList: List["DestinationFlowConfigTypeDef"],
        tasks: List["TaskTypeDef"],
        description: str = None,
        kmsArn: str = None,
        tags: Dict[str, str] = None,
    ) -> CreateFlowResponseTypeDef:
        """
        [Client.create_flow documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.create_flow)
        """

    def delete_connector_profile(
        self, connectorProfileName: str, forceDelete: bool = None
    ) -> Dict[str, Any]:
        """
        [Client.delete_connector_profile documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.delete_connector_profile)
        """

    def delete_flow(self, flowName: str, forceDelete: bool = None) -> Dict[str, Any]:
        """
        [Client.delete_flow documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.delete_flow)
        """

    def describe_connector_entity(
        self,
        connectorEntityName: str,
        connectorType: Literal[
            "Salesforce",
            "Singular",
            "Slack",
            "Redshift",
            "S3",
            "Marketo",
            "Googleanalytics",
            "Zendesk",
            "Servicenow",
            "Datadog",
            "Trendmicro",
            "Snowflake",
            "Dynatrace",
            "Infornexus",
            "Amplitude",
            "Veeva",
            "EventBridge",
        ] = None,
        connectorProfileName: str = None,
    ) -> DescribeConnectorEntityResponseTypeDef:
        """
        [Client.describe_connector_entity documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.describe_connector_entity)
        """

    def describe_connector_profiles(
        self,
        connectorProfileNames: List[str] = None,
        connectorType: Literal[
            "Salesforce",
            "Singular",
            "Slack",
            "Redshift",
            "S3",
            "Marketo",
            "Googleanalytics",
            "Zendesk",
            "Servicenow",
            "Datadog",
            "Trendmicro",
            "Snowflake",
            "Dynatrace",
            "Infornexus",
            "Amplitude",
            "Veeva",
            "EventBridge",
        ] = None,
        maxResults: int = None,
        nextToken: str = None,
    ) -> DescribeConnectorProfilesResponseTypeDef:
        """
        [Client.describe_connector_profiles documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.describe_connector_profiles)
        """

    def describe_connectors(
        self,
        connectorTypes: List[
            Literal[
                "Salesforce",
                "Singular",
                "Slack",
                "Redshift",
                "S3",
                "Marketo",
                "Googleanalytics",
                "Zendesk",
                "Servicenow",
                "Datadog",
                "Trendmicro",
                "Snowflake",
                "Dynatrace",
                "Infornexus",
                "Amplitude",
                "Veeva",
                "EventBridge",
            ]
        ] = None,
        nextToken: str = None,
    ) -> DescribeConnectorsResponseTypeDef:
        """
        [Client.describe_connectors documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.describe_connectors)
        """

    def describe_flow(self, flowName: str) -> DescribeFlowResponseTypeDef:
        """
        [Client.describe_flow documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.describe_flow)
        """

    def describe_flow_execution_records(
        self, flowName: str, maxResults: int = None, nextToken: str = None
    ) -> DescribeFlowExecutionRecordsResponseTypeDef:
        """
        [Client.describe_flow_execution_records documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.describe_flow_execution_records)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.generate_presigned_url)
        """

    def list_connector_entities(
        self,
        connectorProfileName: str = None,
        connectorType: Literal[
            "Salesforce",
            "Singular",
            "Slack",
            "Redshift",
            "S3",
            "Marketo",
            "Googleanalytics",
            "Zendesk",
            "Servicenow",
            "Datadog",
            "Trendmicro",
            "Snowflake",
            "Dynatrace",
            "Infornexus",
            "Amplitude",
            "Veeva",
            "EventBridge",
        ] = None,
        entitiesPath: str = None,
    ) -> ListConnectorEntitiesResponseTypeDef:
        """
        [Client.list_connector_entities documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.list_connector_entities)
        """

    def list_flows(self, maxResults: int = None, nextToken: str = None) -> ListFlowsResponseTypeDef:
        """
        [Client.list_flows documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.list_flows)
        """

    def list_tags_for_resource(self, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.list_tags_for_resource)
        """

    def start_flow(self, flowName: str) -> StartFlowResponseTypeDef:
        """
        [Client.start_flow documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.start_flow)
        """

    def stop_flow(self, flowName: str) -> StopFlowResponseTypeDef:
        """
        [Client.stop_flow documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.stop_flow)
        """

    def tag_resource(self, resourceArn: str, tags: Dict[str, str]) -> Dict[str, Any]:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.tag_resource)
        """

    def untag_resource(self, resourceArn: str, tagKeys: List[str]) -> Dict[str, Any]:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.untag_resource)
        """

    def update_connector_profile(
        self,
        connectorProfileName: str,
        connectionMode: Literal["Public", "Private"],
        connectorProfileConfig: ConnectorProfileConfigTypeDef,
    ) -> UpdateConnectorProfileResponseTypeDef:
        """
        [Client.update_connector_profile documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.update_connector_profile)
        """

    def update_flow(
        self,
        flowName: str,
        triggerConfig: "TriggerConfigTypeDef",
        destinationFlowConfigList: List["DestinationFlowConfigTypeDef"],
        tasks: List["TaskTypeDef"],
        description: str = None,
        sourceFlowConfig: "SourceFlowConfigTypeDef" = None,
    ) -> UpdateFlowResponseTypeDef:
        """
        [Client.update_flow documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.54/reference/services/appflow.html#Appflow.Client.update_flow)
        """
