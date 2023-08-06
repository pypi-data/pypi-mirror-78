# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin,too-many-locals,unused-import
"""
Main interface for identitystore service client

Usage::

    ```python
    import boto3
    from mypy_boto3_identitystore import IdentityStoreClient

    client: IdentityStoreClient = boto3.client("identitystore")
    ```
"""
from typing import Any, Dict, List, Type

from botocore.client import ClientMeta
from botocore.exceptions import ClientError as Boto3ClientError

from mypy_boto3_identitystore.type_defs import (
    DescribeGroupResponseTypeDef,
    DescribeUserResponseTypeDef,
    FilterTypeDef,
    ListGroupsResponseTypeDef,
    ListUsersResponseTypeDef,
)

__all__ = ("IdentityStoreClient",)


class Exceptions:
    AccessDeniedException: Type[Boto3ClientError]
    ClientError: Type[Boto3ClientError]
    InternalServerException: Type[Boto3ClientError]
    ResourceNotFoundException: Type[Boto3ClientError]
    ThrottlingException: Type[Boto3ClientError]
    ValidationException: Type[Boto3ClientError]


class IdentityStoreClient:
    """
    [IdentityStore.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.53/reference/services/identitystore.html#IdentityStore.Client)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.53/reference/services/identitystore.html#IdentityStore.Client.can_paginate)
        """

    def describe_group(self, IdentityStoreId: str, GroupId: str) -> DescribeGroupResponseTypeDef:
        """
        [Client.describe_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.53/reference/services/identitystore.html#IdentityStore.Client.describe_group)
        """

    def describe_user(self, IdentityStoreId: str, UserId: str) -> DescribeUserResponseTypeDef:
        """
        [Client.describe_user documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.53/reference/services/identitystore.html#IdentityStore.Client.describe_user)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.53/reference/services/identitystore.html#IdentityStore.Client.generate_presigned_url)
        """

    def list_groups(
        self,
        IdentityStoreId: str,
        MaxResults: int = None,
        NextToken: str = None,
        Filters: List[FilterTypeDef] = None,
    ) -> ListGroupsResponseTypeDef:
        """
        [Client.list_groups documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.53/reference/services/identitystore.html#IdentityStore.Client.list_groups)
        """

    def list_users(
        self,
        IdentityStoreId: str,
        MaxResults: int = None,
        NextToken: str = None,
        Filters: List[FilterTypeDef] = None,
    ) -> ListUsersResponseTypeDef:
        """
        [Client.list_users documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.53/reference/services/identitystore.html#IdentityStore.Client.list_users)
        """
