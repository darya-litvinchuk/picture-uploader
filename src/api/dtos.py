from dataclasses import dataclass, field
from typing import Optional, Any, Dict


@dataclass
class PictureDTO:
    name: str
    mimetype: str
    content: Optional[str] = None
    link_to_image: Optional[str] = None
    replace_if_exists: bool = False
    meta: Dict[str, Any] = field(default_factory=dict)
