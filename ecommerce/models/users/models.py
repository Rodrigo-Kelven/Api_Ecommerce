from sqlalchemy import Column, Integer, String
from databases.ecommerce_config.database import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    fullname = Column(String, nullable=False)
    username = Column(String, nullable=False ,unique=True, index=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    