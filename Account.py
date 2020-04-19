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
        # side effect : we modify the transaction passed in:
        transaction.timestamp = datetime.now();
        transaction.balance = self._balance + transaction.amount
        self.transaction_history.append(transaction)
        self.__transact(transaction.amount)
        return self._balance

    def rollback_transaction(self, transaction: Transaction) -> Transaction:
        # can only rollback transactions that are in the history for this account
        # step 1 -- find the transaction
        transaction_in_history = self.find_transactions_with_id(transaction.transaction_id)

        # invariant : should only be 0 or 1 transaction in history with that id
        if len(transaction_in_history) <= 0 or len(transaction_in_history) > 1:
            raise KeyError;

        # flip from credit/debit or debit/credit
        opposite_transaction = Transaction(-transaction_in_history[0].amount,
                                           f'rollback: {transaction_in_history[0].memo}')

        self.execute_transaction(opposite_transaction)
        return opposite_transaction

    def find_transactions_with_id(self, transaction_id):
        return list(filter(lambda x: x.transaction_id == transaction_id, self.transaction_history))

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
