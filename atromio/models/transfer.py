from sqlalchemy import Column, Integer, DateTime, ForeignKey

from atromio.models.meta import Base


class Transfer(Base):
    __tablename__ = 'transfer'

    id = Column(Integer, primary_key=True)
    committed_at = Column(DateTime, nullable=False)
    source_account_id = Column(Integer, ForeignKey('account.id'))
    target_account_id = Column(Integer, ForeignKey('account.id'))
    amount = Column(Integer, nullable=False)
