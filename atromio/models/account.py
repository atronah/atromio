from sqlalchemy import Column, Integer, String, Index, select, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, column_property

from .meta import Base
from .transfer import Transfer


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    outcomes = relationship('Transfer', foreign_keys='Transfer.source_account_id', backref='source', lazy='dynamic')
    incomes = relationship('Transfer', foreign_keys='Transfer.target_account_id', backref='target', lazy='dynamic')
    transfers = relationship('Transfer',
                             primaryjoin='or_(Transfer.source_account_id == Account.id, '
                                         'Transfer.target_account_id == Account.id)',
                             lazy='dynamic',
                             order_by='desc(Transfer.committed_at)')

    @hybrid_property
    def balance(self):
        incomes = sum((t.amount for t in self.incomes.all()))
        outcomes = sum((t.amount for t in self.outcomes.all()))
        return incomes - outcomes


Index('idx_account_name', Account.name, unique=True)