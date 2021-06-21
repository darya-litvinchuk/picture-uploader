import os
from typing import Dict, Any


def stat_to_dict(path: str) -> Dict[str, Any]:
    metadata = os.stat(path)
    return {k: getattr(metadata, k) for k in dir(metadata) if k.startswith('st_')}


def parse_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    image_metadata = {}
    for k, v in metadata.items():
        if k not in ("ResponseMetadata", "Body"):
            image_metadata[k] = v
    return image_metadata
