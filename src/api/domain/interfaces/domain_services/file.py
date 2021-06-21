from abc import ABC, abstractmethod
from typing import Any, Dict

from api.domain.entities import PictureEntity
from api.dtos import PictureDTO


class IStorageService(ABC):
    @abstractmethod
    def upload(self, picture: PictureDTO) -> PictureEntity:
        pass

    @abstractmethod
    def download(self, name: str) -> PictureDTO:
        pass

    @abstractmethod
    def picture_metadata(self, name: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def delete(self, name: str) -> None:
        pass
