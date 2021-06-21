from dependency_injector import containers, providers

from api.domain.sevices.file import FileStorageService
from api.domain.sevices.subscription import SubscriptionService
from api.infrastructure.repositories.picture import PictureRepository
from api.infrastructure.services.file.blob import UploadFileStorageService
from api.infrastructure.services.file.s3 import S3StorageService

from api.infrastructure.services.subscription.aws import AWSSubscriptionService


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()


class UploadStorageService(containers.DeclarativeContainer):
    blob = providers.Singleton(UploadFileStorageService)
    s3 = providers.Singleton(S3StorageService)


class CloudSubscriptionService(containers.DeclarativeContainer):
    aws = providers.Singleton(AWSSubscriptionService)


class InfrastructureServices(containers.DeclarativeContainer):
    upload_service = providers.Selector(
        Core.config.storage_type,
        blob=providers.Singleton(UploadStorageService.blob),
        s3=providers.Singleton(UploadStorageService.s3)
    )
    subscription_service = providers.Singleton(CloudSubscriptionService.aws)


class Repositories(containers.DeclarativeContainer):
    picture = providers.Singleton(PictureRepository)


class DomainServices(containers.DeclarativeContainer):
    storage_service = providers.Singleton(
        FileStorageService,
        InfrastructureServices.upload_service,
        Repositories.picture
    )
    subscription_service = providers.Singleton(
        SubscriptionService,
        InfrastructureServices.subscription_service
    )
