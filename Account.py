from Transaction import Transaction

from datetime import datetime

class AccountError(Exception):
    pass


class InsufficientFundsError(AccountError):
    pass

# TODO: how to represent opening balance?
class Account(object):
    def __init__(self, name, number, overdraft=0):
        self.account_holder = name
        self.account_number = number
        self.balance = 0
        self.overdraft_maximum = overdraft
        self.transaction_history = []

    def execute_transaction(self, transaction: Transaction) -> float:
        # warning : we modify the transaction passed in:
        transaction.timestamp = datetime.now();
        transaction.balance = self.balance + transaction.amount
        self.transaction_history.append(transaction)
        self.__transact(transaction.amount)
        return self.balance

    def __transact(self, amount: float) -> float:
        self.balance += amount
        if self.balance + self.overdraft_maximum < 0:
            raise InsufficientFundsError({'message': 'Negative balance', 'balance': self.balance})
        return self.balance

    def get_overdraft_amount_available(self) -> float:
        return self.overdraft_maximum if self.balance >= 0 else self.overdraft_maximum + self.balance
