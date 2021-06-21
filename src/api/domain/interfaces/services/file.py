from abc import ABC, abstractmethod
from typing import Any, Dict

from api.dtos import PictureDTO


class IUploadService(ABC):
    @abstractmethod
    def upload(self, picture: PictureDTO) -> PictureDTO:
        pass

    @abstractmethod
    def download(self, picture_dto: PictureDTO) -> PictureDTO:
        pass

    @abstractmethod
    def picture_metadata(self, picture_dto: PictureDTO) -> Dict[str, Any]:
        pass

    @abstractmethod
    def delete(self, picture_dto: PictureDTO) -> None:
        pass
