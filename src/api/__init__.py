import logging

from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import sessionmaker

from .config import get_settings

metadata = MetaData()

ENGINE = create_engine(make_url(get_settings().database.url()))
SESSION_FACTORY = sessionmaker(autoflush=False, bind=ENGINE)

logging.basicConfig(
    level=get_settings().logger_level,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S",
)
logger = logging.getLogger(__name__)
