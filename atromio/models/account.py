from sqlalchemy import Column, Integer, String, Index

from atromio.models.meta import Base


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))


Index('idx_account_name', Account.name, unique=True)