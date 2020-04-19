from datetime import datetime
from uuid import uuid1


class AccountTransaction(object):
    def __init__(self, amount: float, memo: str):
        self.timestamp = datetime.now() # start with created time
        self.amount = amount
        self.memo = memo
        self.transaction_id = uuid1().int  # not 'safe'
        self.balance = 0
