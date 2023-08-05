# pylint: disable=unused-argument,multiple-statements,unused-import
from typing import Any, List

import boto3
import boto3.utils
import botocore.session
from boto3.exceptions import ResourceNotExistsError, UnknownAPIVersionError
from boto3.resources.factory import ResourceFactory
from botocore.client import Config
from botocore.credentials import Credentials
from botocore.exceptions import DataNotFoundError, UnknownServiceError
from botocore.loaders import Loader
from botocore.model import ServiceModel


class _SessionServicesFallback:
    def client(
        self,
        service_name: str,
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> Any: ...
    def resource(
        self,
        service_name: str,
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> Any: ...

try:
    from mypy_boto3.boto3_session import Session as SessionServices
except (ImportError, ModuleNotFoundError):
    SessionServices = _SessionServicesFallback

class Session(SessionServices):
    def __init__(
        self,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        region_name: str = None,
        botocore_session: Session = None,
        profile_name: str = None,
    ):
        self._session: ServiceModel
        self.resource_factory: ResourceFactory
        self._loader: Loader
    def __repr__(self) -> str: ...
    @property
    def profile_name(self) -> str: ...
    @property
    def region_name(self) -> str: ...
    @property
    def events(self) -> List[Any]: ...
    @property
    def available_profiles(self) -> List[Any]: ...
    def _setup_loader(self) -> None: ...
    def get_available_services(self) -> List[str]: ...
    def get_available_resources(self) -> List[str]: ...
    def get_available_partitions(self) -> List[str]: ...
    def get_available_regions(
        self, service_name: str, partition_name: str = "aws", allow_non_regional: bool = False,
    ) -> List[str]: ...
    def get_credentials(self) -> Credentials: ...
    def _register_default_handlers(self) -> None: ...
