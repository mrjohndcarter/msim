class AccountError(Exception):
    pass


class InsufficientFundsError(AccountError):
    pass


class Account(object):
    def __init__(self, name, number, overdraft=0):
        self.account_holder = name
        self.account_number = number
        self.balance = 0
        self.overdraft_maximum = overdraft

    def transact(self, amount: float) -> float:
        self.balance += amount
        if self.balance + self.overdraft_maximum < 0:
            raise InsufficientFundsError({'message': 'Negative balance', 'balance': self.balance})
        return self.balance

    def get_overdraft_amount_available(self) -> float:
        return self.overdraft_maximum if self.balance >= 0 else self.overdraft_maximum + self.balance
