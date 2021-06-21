from sqlalchemy import Column, JSON, String, Table

from api import metadata

PicturesTable = Table(
    "pictures_table",
    metadata,
    Column("name", String, primary_key=True, nullable=False),
    Column("link_to_image", String, nullable=False),
    Column("mimetype", String, nullable=False),
    Column("meta", JSON, default="{}"),
)
