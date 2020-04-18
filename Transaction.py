from datetime import datetime
from uuid import uuid1


class Transaction(object):
    def __init__(self, timestamp: datetime, amount: float, memo: str):
        self.timestamp = timestamp
        self.amount = amount
        self.memo = memo
        self.transaction_id = uuid1().int  # not 'safe'
