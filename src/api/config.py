import logging
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, DirectoryPath, Field
from ssm_parameter_store import EC2ParameterStore

APP_URL_PREFIX = "/api/v1/picture-uploader/"

DEFAULT_STORAGE_TYPE = "s3"
DEFAULT_REGION_NAME = "us-east-1"
DEFAULT_SSM_PREFIX_NAME = "/picture-uploader/env/"


class DatabaseSettings(BaseSettings):
    class Config:
        env_prefix = "POSTGRES_"

    work_user: str
    work_user_password: str
    work_db: str
    host: str
    port: int
    alchemy_driver: str

    def url(self) -> str:
        return "{}://{}:{}@{}:{}/{}".format(
            self.alchemy_driver,
            self.work_user,
            self.work_user_password,
            self.host,
            self.port,
            self.work_db,
        )


class BlobFileStorageSettings(BaseSettings):
    root_dir: DirectoryPath = Path(__file__).resolve().parent
    media_root: Path = Field("media/files")


class S3StorageSettings(BaseSettings):
    class Config:
        env_prefix = "AWS_"
    s3_bucket_name: str = Field("")


class AWSSubscriptionSettings(BaseSettings):
    class Config:
        env_prefix = "AWS_"
    sns_topic_name: str = Field("")
    sqs_queue_name: str = Field("")


class CredentialsStoreSettings(BaseSettings):
    region_name: str = Field(DEFAULT_REGION_NAME)
    aws_access_key_id: str = Field("")
    aws_secret_access_key: str = Field("")

    ssm_prefix_name: str = Field(DEFAULT_SSM_PREFIX_NAME)


class ApplicationSettings(BaseSettings):
    class Config:
        env_prefix = "PICTURE_UPLOADER_"

    is_debug: bool = Field(False)

    is_ssm_enabled: bool = Field(False)

    logger_level: int = Field(logging.WARNING)

    max_content_length: int = Field(20 * 1024 * 1024)

    database: DatabaseSettings = Field(DatabaseSettings())

    aws_credentials: CredentialsStoreSettings = Field(CredentialsStoreSettings())

    storage_type: str = Field(DEFAULT_STORAGE_TYPE)

    s3_storage: S3StorageSettings = Field(S3StorageSettings())
    blob_storage: BlobFileStorageSettings = Field(BlobFileStorageSettings())

    subscription: AWSSubscriptionSettings = Field(AWSSubscriptionSettings())


def _envs_from_ssm():
    credentials = CredentialsStoreSettings()
    parameter_store = EC2ParameterStore(
        region_name=credentials.region_name,
        aws_access_key_id=credentials.aws_access_key_id,
        aws_secret_access_key=credentials.aws_secret_access_key,
    )
    parameters = parameter_store.get_parameters_by_path(credentials.ssm_prefix_name)
    EC2ParameterStore.set_env(parameters)


@lru_cache()
def get_settings() -> ApplicationSettings:
    settings = ApplicationSettings()
    if settings.is_ssm_enabled:
        _envs_from_ssm()

    return ApplicationSettings()
