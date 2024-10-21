from sqlalchemy import Table, Column, Integer, TIMESTAMP, MetaData, ForeignKey, String

from database import metadata, Base


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    date = Column(TIMESTAMP)
    content = Column(String, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}