from sqlalchemy import Table, Column, Integer, TIMESTAMP, MetaData, ForeignKey, String

from database import metadata

message = Table(
    "message",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("date", TIMESTAMP),
    Column("content", String, nullable=False)
)