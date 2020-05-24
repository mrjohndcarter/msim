from AccountTransaction import AccountTransaction

from datetime import datetime


class AccountError(Exception):
    pass


class InsufficientFundsError(AccountError):
    pass


class AmountError(AccountError):
    pass


class Account(object):
    def __init__(self, name, number, overdraft=0, opening_balance=0):
        self.account_holder = name
        self.account_number = number
        self._balance = 0
        self.overdraft_maximum = overdraft
        self.transaction_history = []
        self.execute_transaction(AccountTransaction(opening_balance, 'opening balance'))

    def execute_transaction(self, transaction: AccountTransaction) -> float:
        # side effect : we modify the transaction passed in:
        transaction.timestamp = datetime.now();
        transaction.balance = self._balance + transaction.amount
        self.transaction_history.append(transaction)
        self.__transact(transaction.amount)
        transaction.balance = self._balance
        return self._balance

    def rollback_transaction(self, transaction: AccountTransaction) -> AccountTransaction:
        # can only rollback transactions that are in the history for this account
        # step 1 -- find the transaction
        transaction_in_history = self.find_transactions_with_id(transaction.transaction_id)

        # invariant : should only be 0 or 1 transaction in history with that id
        if len(transaction_in_history) <= 0 or len(transaction_in_history) > 1:
            raise KeyError;

        # flip from credit/debit or debit/credit
        opposite_transaction = AccountTransaction(-transaction_in_history[0].amount,
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

    def get_transaction_history(self, start_date, end_date) -> list:
        sorted_transactions = sorted(self.transaction_history, key=lambda t: t.timestamp)

        for transaction in self.transaction_history:
            print(f'{transaction.transaction_id} {transaction.timestamp} A:{transaction.amount} B:{transaction.balance} {transaction.memo}')

    balance = property(get_balance)
