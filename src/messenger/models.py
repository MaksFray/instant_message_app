from sqlalchemy import Table, Column, Integer

message = Table(
    "message",
    metadata,
    Column("id", Integer, primary_key=True),
)