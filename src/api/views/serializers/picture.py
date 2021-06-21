from typing import Any, Dict

from pydantic import BaseModel, validator, EmailStr

ACCEPTABLE_MIMETYPES = [
    "image/jpeg",
    "image/png",
    "application/pdf",
    "application/json",
    "application/vnd.ms-outlook",
    "message/rfc822",
]


class PictureSerializer(BaseModel):
    name: str
    mimetype: str
    replace_if_exists: bool = False
    meta: Dict[str, Any] = {}

    @validator("mimetype")
    def validate_mimetype(cls, mimetype):
        if mimetype not in ACCEPTABLE_MIMETYPES:
            raise ValueError(f"Mimetype {mimetype} is not acceptable")
        return mimetype


class GetPictureSerializer(PictureSerializer):
    name: str
    mimetype: str = "image/jpeg"
    meta: Dict[str, Any] = {}


class EmailSerializer(BaseModel):
    email: EmailStr
