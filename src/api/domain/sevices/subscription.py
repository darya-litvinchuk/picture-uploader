from api.domain.interfaces.domain_services.subscription import ISubscriptionService
from api.domain.interfaces.services.subscription import ICloudSubscriptionService
from api.dtos import PictureDTO

from api.domain.sevices.utils import image_size, image_link, image_extension


class SubscriptionService(ISubscriptionService):

    def __init__(self, subscription_service: ICloudSubscriptionService):
        self._subscription_service: ICloudSubscriptionService = subscription_service

    def subscribe(self, email: str):
        return self._subscription_service.subscribe(email)

    def unsubscribe(self, subscription_arn: str):
        return self._subscription_service.unsubscribe(subscription_arn)

    def message_to_queue(self, picture_dto: PictureDTO) -> None:
        message = (
            f"Image {picture_dto.name} has been uploaded. "
            f"Image metadata: mimetype - {picture_dto.mimetype}, "
            f"extension - {image_extension(picture_dto)}, "
            f"size - {image_size(picture_dto)} bytes. "
            f"Link to the application to download the image - {image_link(picture_dto)}"
        )
        return self._subscription_service.message_to_queue(message)

    def message_to_topic(self):
        return self._subscription_service.message_to_topic()
