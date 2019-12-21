from sqlalchemy import Column, Integer, DateTime, ForeignKey, Index

from atromio.models.meta import Base


class RealBalance(Base):
    __tablename__ = 'real_balance'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    confirmed_at = Column(DateTime, nullable=False)
    amount = Column(Integer, nullable=False)


Index('idx_real_balance_acc_n_date', RealBalance.account_id, RealBalance.confirmed_at, unique=True)