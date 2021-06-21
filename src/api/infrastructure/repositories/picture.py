from dataclasses import asdict

from sqlalchemy import insert, select, delete, func

from api.domain.entities import PictureEntity
from api.domain.interfaces.repositories.file import IPictureRepository
from api.domain.mapper import build_picture_entity
from api.exceptions import NotFoundException
from api.infrastructure.models.picture import PicturesTable
from api.infrastructure.sessions import SessionManager


class PictureRepository(IPictureRepository):

    def by_name(self, name: str) -> PictureEntity:
        query = select([PicturesTable]).where(PicturesTable.c.name == name)

        manager = SessionManager()
        with manager.main as db_session:
            result = db_session.execute(query).fetchone()

        if not result:
            raise NotFoundException("file", name)

        return build_picture_entity(result)

    def create(self, picture: PictureEntity) -> PictureEntity:
        query = (
            insert(PicturesTable).values(**asdict(picture)).returning(
                *PicturesTable.columns
            )
        )

        manager = SessionManager()
        with manager.main as db_session:
            result = db_session.execute(query).fetchone()

        return build_picture_entity(result)

    def delete(self, name: str) -> bool:
        query = delete(PicturesTable).where(PicturesTable.c.name == name)

        manager = SessionManager()
        with manager.main as db_session:
            result = db_session.execute(query).rowcount

        is_rule_exist = result == 1
        if not is_rule_exist:
            raise NotFoundException("file", name)

        return is_rule_exist

    def random_picture(self) -> PictureEntity:
        query = select([PicturesTable]).order_by(func.random())

        manager = SessionManager()
        with manager.main as db_session:
            result = db_session.execute(query).fetchone()

        return build_picture_entity(result)
