from unittest import TestCase


class AccountError(Exception):
    pass


class InsufficientFundsError(AccountError):
    pass


class Account(object):
    def __init__(self, name, number):
        self.account_holder = name
        self.account_number = number
        self.balance = 0

    def transact(self, amount: float) -> float:
        self.balance += amount
        if self.balance < 0:
            raise InsufficientFundsError({'message': 'Negative balance', 'balance': self.balance})
        return self.balance


class TestAccount(TestCase):
    def setUp(self) -> None:
        self.a = Account('Alice', 1)
        self.b = Account('Bob', 2)
        self.b.balance = 1000.0

    def test_new_account(self):
        self.assertEqual(self.a.balance, 0)

    def test_deposit(self):
        self.a.transact(505.50)
        self.assertEqual(self.a.balance, 505.50)
        self.assertEqual(self.a.transact(10), 515.50)

    def test_withdrawal_no_overdraft(self):
        self.b.transact(-500)
        self.assertEqual(self.b.balance, 500)
        self.assertEqual(self.b.transact(-100), 400)

    def test_withdrawal_no_overdraft_attempted_overdraw(self):
        with self.assertRaises(InsufficientFundsError) as context:
            self.a.transact(-500)
        self.assertEqual(context.exception.args[0]['balance'], -500)

        self.b.transact(4000)
        with self.assertRaises(InsufficientFundsError) as context:
            self.b.transact(-10000)
        self.assertEqual(context.exception.args[0]['balance'], -5000)