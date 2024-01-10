from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Column, String, Integer, DateTime
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    body = Column(String)
    username = Column(String)
    created_at = Column(DateTime, server_default=db.func.now())
    updated_at = Column(DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f"Body: {self.body}, Username: {self.username}, created at {self.created_at}"
