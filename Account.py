from Transaction import Transaction

from datetime import datetime


class AccountError(Exception):
    pass


class InsufficientFundsError(AccountError):
    pass


class Account(object):
    def __init__(self, name, number, overdraft=0, opening_balance=0):
        self.account_holder = name
        self.account_number = number
        self._balance = opening_balance
        self.overdraft_maximum = overdraft
        self.transaction_history = []

    def execute_transaction(self, transaction: Transaction) -> float:
        # warning : we modify the transaction passed in:
        transaction.timestamp = datetime.now();
        transaction.balance = self._balance + transaction.amount
        self.transaction_history.append(transaction)
        self.__transact(transaction.amount)
        return self._balance

    def __transact(self, amount: float) -> float:
        self._balance += amount
        if self._balance + self.overdraft_maximum < 0:
            raise InsufficientFundsError({'message': 'Negative balance', 'balance': self.balance})
        return self.balance

    def get_overdraft_amount_available(self) -> float:
        return self.overdraft_maximum if self._balance >= 0 else self.overdraft_maximum + self._balance

    def get_balance(self):
        return self._balance

    balance = property(get_balance)
