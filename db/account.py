from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .meta.base import Base
from .meta.types import Money


class Transfer(Base):
    __tablename__ = 'transfer'

    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    committed_at = Column(DateTime, nullable=False)
    amount = Column(Money, nullable=False)
    source_id = Column(Integer, ForeignKey('account.id'))
    source = relationship('Account', foreign_keys=[source_id])
    destination_id = Column(Integer, ForeignKey('account.id'))
    destination = relationship('Account', foreign_keys=[destination_id], back_populates='incomes')


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    description = Column(String(255))





class AccountBalance(Base):
    __tablename__ = 'account_balance'

    id = Column(Integer, primary_key=True)
    confirmed_at = Column(DateTime, nullable=False)
    amount = Column(Money, nullable=False)
    account_id = Column(Integer, ForeignKey(Account.id))
    account = relationship(Account)