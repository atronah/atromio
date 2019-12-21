from atromio.models import Transfer


def make_transfer(session, amount, committed_at, source_account_id, target_account_id):
    transfer = Transfer(committed_at=committed_at,
                        source_account_id=source_account_id,
                        target_account_id=target_account_id,
                        amount=amount)
    session.add(transfer)
    session.flush()
    return transfer.id


def get_transfers(session, source_account_id):
    account_transfers = session.query(Transfer).filter(Transfer.source_account_id == source_account_id).all()
    return [(t.id, t.committed_at, t.source_account_id, t.amount, t.target_account_id) for t in account_transfers]
