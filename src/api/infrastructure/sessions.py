import logging
import traceback
from typing import Optional

from sqlalchemy.orm import Session, scoped_session

from api import SESSION_FACTORY

logger = logging.getLogger(__name__)


class ValidationServiceSession:
    def __init__(self) -> None:
        self._session = scoped_session(SESSION_FACTORY)
        self._session_refs_count = 0

    def __enter__(self):
        self._session_refs_count += 1
        return self._session()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            if self._session_refs_count == 1:
                self._session().commit()
            else:
                self._session().flush()
        else:
            try:
                if self._session_refs_count == 1:
                    self._session().rollback()
            except Exception as exception:
                logger.error(str(exception))
                logger.error(traceback.format_exc())
            logger.error(traceback.format_tb(exc_tb))
        self._session_refs_count -= 1


class SessionManager:
    def __init__(self) -> None:
        self._main_session: Optional[Session] = None

    @property
    def main(self) -> Session:
        if not self._main_session:
            self._main_session = ValidationServiceSession()

        return self._main_session
