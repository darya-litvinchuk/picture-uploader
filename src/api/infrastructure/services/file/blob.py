import os
from pathlib import Path
from typing import Any, Dict

from api.config import get_settings
from api.domain.interfaces.services.file import IUploadService
from api.dtos import PictureDTO
from api.exceptions import AlreadyExistException, LogicalException, NotFoundException
from api.infrastructure.services.utils import stat_to_dict


class UploadFileStorageService(IUploadService):
    FILE_UPLOAD_PERMISSIONS = 0o777

    def __init__(self) -> None:
        self.media_root = get_settings().blob_storage.media_root

    def _get_absolute_path(self, path: str) -> Path:
        return Path(self.media_root) / path

    def upload(self, picture_dto: PictureDTO) -> PictureDTO:
        absolute_path = self._get_absolute_path(picture_dto.name)

        try:
            absolute_path.parent.mkdir(
                self.FILE_UPLOAD_PERMISSIONS, parents=True, exist_ok=True
            )
            if absolute_path.exists() and not picture_dto.replace_if_exists:
                raise AlreadyExistException(picture_dto.name)
            absolute_path.write_bytes(picture_dto.content)
        except FileExistsError:
            raise AlreadyExistException(picture_dto.name)
        except IsADirectoryError:
            raise AlreadyExistException(picture_dto.name)

        picture_dto.link_to_image = str(absolute_path)

        return picture_dto

    def download(self, picture_dto: PictureDTO) -> PictureDTO:
        path = picture_dto.link_to_image
        try:
            content = Path(path).read_bytes()
        except FileNotFoundError:
            raise NotFoundException("file", path)
        except IsADirectoryError:
            raise LogicalException(
                f"Could not delete file {path} because it's directory"
            )

        picture_dto.content = content

        return picture_dto

    def picture_metadata(self, picture_dto: PictureDTO) -> Dict[str, Any]:
        link_to_image = picture_dto.link_to_image
        if not Path(link_to_image).exists():
            raise NotFoundException("file", link_to_image)
        return stat_to_dict(link_to_image)

    def _delete_dir_if_empty(self, link_to_image: str) -> None:
        dir_name = Path(link_to_image).parent
        while not self.media_root.samefile(dir_name) and not os.listdir(dir_name):
            Path(dir_name).rmdir()
            dir_name = dir_name.parent

    def delete(self, picture_dto: PictureDTO) -> None:
        link_to_image = picture_dto.link_to_image
        try:
            Path(link_to_image).unlink()
            self._delete_dir_if_empty(link_to_image)
        except FileNotFoundError:
            raise NotFoundException("file", link_to_image)
        except IsADirectoryError:
            raise LogicalException(
                f"Could not delete file {link_to_image} because it's directory"
            )
