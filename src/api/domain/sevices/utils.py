import sys
from functools import reduce
from pathlib import Path
from urllib.parse import urljoin

from requests import ConnectTimeout

from api.config import APP_URL_PREFIX
from api.dtos import PictureDTO
from ec2_metadata import ec2_metadata


LOCAL_HOST = f"http://localhost:8080"


def image_size(picture_dto: PictureDTO) -> float:
    return sys.getsizeof(picture_dto.content)


def image_extension(picture_dto: PictureDTO) -> str:
    return Path(picture_dto.name).suffix


def image_link(picture_dto: PictureDTO) -> str:
    try:
        public_api = ec2_metadata.public_ipv4
    except ConnectTimeout:
        public_api = LOCAL_HOST
    return reduce(urljoin, [public_api, APP_URL_PREFIX, "pictures/", picture_dto.name])
