from abc import ABCMeta, abstractmethod

from api.domain.entities import PictureEntity


class IPictureRepository(metaclass=ABCMeta):

    @abstractmethod
    def by_name(self, name: str) -> PictureEntity:
        pass

    @abstractmethod
    def create(self, picture: PictureEntity) -> PictureEntity:
        pass

    @abstractmethod
    def delete(self, name: str) -> bool:
        pass

    def random_picture(self) -> PictureEntity:
        pass
