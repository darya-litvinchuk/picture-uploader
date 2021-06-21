from typing import Optional

from pydantic import BaseSettings

DEFAULT_PORT = 8000
RELOAD = True
DEFAULT_NUM_WORKERS = 2
DEFAULT_NUM_THREADS = 2


class GunicornSettings(BaseSettings):
    class Config:
        env_prefix = "PICTURE_UPLOADER_"

    port: Optional[int] = DEFAULT_PORT
    reload: Optional[bool] = RELOAD
    num_workers: Optional[int] = DEFAULT_NUM_WORKERS
    num_threads: Optional[int] = DEFAULT_NUM_THREADS


setting = GunicornSettings()
port = setting.port
bind = f"0.0.0.0:{port}"
reload = setting.reload
workers = setting.num_workers
threads = setting.num_threads
