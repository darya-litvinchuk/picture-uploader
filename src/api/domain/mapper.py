from typing import Any, Dict

from api.domain.entities import PictureEntity


def build_picture_entity(picture_dict: Dict[str, Any]) -> PictureEntity:
    return PictureEntity(
        name=picture_dict["name"],
        mimetype=picture_dict["mimetype"],
        link_to_image=picture_dict["link_to_image"],
        meta=picture_dict["meta"],
    )
