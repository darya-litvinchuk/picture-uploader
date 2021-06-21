from dataclasses import asdict
from typing import Any, Dict

from api import logger
from api.domain.entities import PictureEntity
from api.domain.interfaces.domain_services.file import IStorageService
from api.domain.interfaces.repositories.file import IPictureRepository
from api.domain.interfaces.services.file import IUploadService
from api.domain.interfaces.services.subscription import ICloudSubscriptionService
from api.domain.mapper import build_picture_entity
from api.dtos import PictureDTO


class FileStorageService(IStorageService):

    def __init__(
            self,
            upload_service: IUploadService,
            storage_repository: IPictureRepository,
    ) -> None:
        self._upload_service: IUploadService = upload_service
        logger.debug(f"Storage service: {self._upload_service}")

        self._picture_repo: IPictureRepository = storage_repository

    def upload(self, picture_dto: PictureDTO) -> PictureEntity:
        picture_dto = self._upload_service.upload(picture_dto)
        picture = self._picture_repo.create(build_picture_entity(asdict(picture_dto)))
        return picture

    def download(self, name: str) -> PictureDTO:
        picture_entity = self._picture_repo.by_name(name)
        return self._upload_service.download(picture_entity)

    def picture_metadata(self, name: str) -> Dict[str, Any]:
        picture_entity = self._picture_repo.by_name(name)
        picture_dto = PictureDTO(**asdict(picture_entity))
        return self._upload_service.picture_metadata(picture_dto)

    def random_metadata(self) -> Dict[str, Any]:
        picture_entity = self._picture_repo.random_picture()
        picture_dto = PictureDTO(**asdict(picture_entity))
        return self._upload_service.picture_metadata(picture_dto)

    def delete(self, name: str) -> None:
        picture_entity = self._picture_repo.by_name(name)
        picture_dto = PictureDTO(**asdict(picture_entity))
        self._upload_service.delete(picture_dto)
        return self._picture_repo.delete(name)
