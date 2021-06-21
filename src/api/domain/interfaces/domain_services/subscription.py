from abc import ABC, abstractmethod

from api.dtos import PictureDTO


class ISubscriptionService(ABC):
    @abstractmethod
    def subscribe(self, email: str) -> str:
        pass

    @abstractmethod
    def unsubscribe(self, subscription_arn: str) -> None:
        pass

    @abstractmethod
    def message_to_queue(self, picture_dto: PictureDTO) -> None:
        pass

    @abstractmethod
    def message_to_topic(self):
        pass
