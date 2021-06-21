from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class PictureEntity:
    name: str
    mimetype: str
    link_to_image: str
    meta: Dict[str, Any] = field(default_factory=dict)
