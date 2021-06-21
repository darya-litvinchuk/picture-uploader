from abc import ABC, abstractmethod


class ICloudSubscriptionService(ABC):
    @abstractmethod
    def subscribe(self, email: str) -> str:
        pass

    @abstractmethod
    def unsubscribe(self, subscription_arn: str) -> None:
        pass

    @abstractmethod
    def message_to_queue(self, message: str) -> None:
        pass

    @abstractmethod
    def message_to_topic(self):
        pass
