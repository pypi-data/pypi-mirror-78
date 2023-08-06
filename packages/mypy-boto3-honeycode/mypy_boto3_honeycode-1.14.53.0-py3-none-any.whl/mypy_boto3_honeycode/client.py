# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin,too-many-locals,unused-import
"""
Main interface for honeycode service client

Usage::

    ```python
    import boto3
    from mypy_boto3_honeycode import HoneycodeClient

    client: HoneycodeClient = boto3.client("honeycode")
    ```
"""
from typing import Any, Dict, Type

from botocore.client import ClientMeta
from botocore.exceptions import ClientError as Boto3ClientError

from mypy_boto3_honeycode.type_defs import (
    GetScreenDataResultTypeDef,
    InvokeScreenAutomationResultTypeDef,
    VariableValueTypeDef,
)

__all__ = ("HoneycodeClient",)


class Exceptions:
    AccessDeniedException: Type[Boto3ClientError]
    AutomationExecutionException: Type[Boto3ClientError]
    AutomationExecutionTimeoutException: Type[Boto3ClientError]
    ClientError: Type[Boto3ClientError]
    InternalServerException: Type[Boto3ClientError]
    RequestTimeoutException: Type[Boto3ClientError]
    ResourceNotFoundException: Type[Boto3ClientError]
    ServiceUnavailableException: Type[Boto3ClientError]
    ThrottlingException: Type[Boto3ClientError]
    ValidationException: Type[Boto3ClientError]


class HoneycodeClient:
    """
    [Honeycode.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.53/reference/services/honeycode.html#Honeycode.Client)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.53/reference/services/honeycode.html#Honeycode.Client.can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.53/reference/services/honeycode.html#Honeycode.Client.generate_presigned_url)
        """

    def get_screen_data(
        self,
        workbookId: str,
        appId: str,
        screenId: str,
        variables: Dict[str, VariableValueTypeDef] = None,
        maxResults: int = None,
        nextToken: str = None,
    ) -> GetScreenDataResultTypeDef:
        """
        [Client.get_screen_data documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.53/reference/services/honeycode.html#Honeycode.Client.get_screen_data)
        """

    def invoke_screen_automation(
        self,
        workbookId: str,
        appId: str,
        screenId: str,
        screenAutomationId: str,
        variables: Dict[str, VariableValueTypeDef] = None,
        rowId: str = None,
        clientRequestToken: str = None,
    ) -> InvokeScreenAutomationResultTypeDef:
        """
        [Client.invoke_screen_automation documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.53/reference/services/honeycode.html#Honeycode.Client.invoke_screen_automation)
        """
