from typing import Dict, Any

import boto3
from botocore.exceptions import ClientError

from api import get_settings
from api.domain.interfaces.domain_services.file import IStorageService
from api.dtos import PictureDTO
from api.exceptions import AlreadyExistException, NotFoundException, LogicalException
from api.infrastructure.services.utils import parse_metadata


class S3StorageService(IStorageService):

    def _bucket_exists(self):
        try:
            self._s3_client.head_bucket(Bucket=self._bucket)
        except ClientError:
            raise NotFoundException("bucket", self._bucket)

    def __init__(self):
        self._s3_resource = boto3.resource(
            "s3",
            aws_access_key_id=get_settings().aws_credentials.aws_access_key_id,
            aws_secret_access_key=get_settings().aws_credentials.aws_secret_access_key,
        )
        self._s3_client = boto3.client("s3")
        self._bucket = get_settings().s3_storage.s3_bucket_name

        self._bucket_exists()

    def exists(self, picture_name) -> bool:
        try:
            self._s3_resource.Object(self._bucket, picture_name).load()
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
        return True

    def upload(self, picture_dto: PictureDTO) -> PictureDTO:
        if not picture_dto.replace_if_exists and self.exists(picture_dto.name):
            raise AlreadyExistException(picture_dto.name)

        s3_object = self._s3_resource.Object(self._bucket, picture_dto.name)
        s3_object.put(Body=picture_dto.content, ContentType=picture_dto.mimetype)

        picture_dto.link_to_image = f"s3://{self._bucket}/{picture_dto.name}"

        return picture_dto

    def download(self, picture_dto: PictureDTO) -> PictureDTO:
        try:
            s3_object = self._s3_resource.Object(self._bucket, picture_dto.name)
            content = s3_object.get()["Body"].read()
        except ClientError as exception:
            if exception.response["Error"]["Code"] == "404":
                raise NotFoundException("file", picture_dto.name)
            raise LogicalException(f"Could not download {picture_dto.name}")

        picture_dto.content = content
        return picture_dto

    def delete(self, picture_dto: PictureDTO) -> None:
        try:
            s3_object = self._s3_resource.Object(self._bucket, picture_dto.name)
            s3_object.delete()
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                raise NotFoundException("file", picture_dto.name)
            raise LogicalException(f"Could not delete {picture_dto.name}")

    def picture_metadata(self, picture_dto: PictureDTO) -> Dict[str, Any]:
        try:
            s3_object = self._s3_resource.Object(self._bucket, picture_dto.name)
            metadata = s3_object.get()
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                raise NotFoundException("file", picture_dto.name)
            raise LogicalException(f"Could not get metadata for the {picture_dto.name}")
        return parse_metadata(metadata)
