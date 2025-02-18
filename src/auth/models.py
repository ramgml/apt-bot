from sqlalchemy import Column, Integer, String, DateTime

from auth.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, index=True, nullable=False)
    email_to = Column(String, unique=True)
    email_from = Column(String)
    account_number = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
    expires_at = Column(DateTime)
