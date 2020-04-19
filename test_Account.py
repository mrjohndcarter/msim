from unittest.case import TestCase

from Account import Account, InsufficientFundsError
from Transaction import Transaction

class TestAccount(TestCase):
    def setUp(self) -> None:
        self.a = Account('Alice', 1)
        self.b = Account('Bob', 2)
        self.b.balance = 1000.0

    def test_new_account(self):
        self.assertEqual(0, self.a.balance)

    def test_deposit(self):
        self.a.execute_transaction(Transaction(505.50, ''))
        self.assertEqual(505.50, self.a.balance)
        self.assertEqual(515.50, self.a.execute_transaction(Transaction(10, '')))

    def test_withdrawal_no_overdraft(self):
        self.b.execute_transaction(Transaction(-500, ''))
        self.assertEqual(500, self.b.balance)
        self.assertEqual(400, self.b.execute_transaction(Transaction(-100, '')))

    def test_withdrawal_no_overdraft_attempted_overdraw(self):
        with self.assertRaises(InsufficientFundsError) as context:
            self.a.execute_transaction(Transaction(-500, ''))
        self.assertEqual(-500, context.exception.args[0]['balance'])

        self.b.execute_transaction(Transaction(4000, ''))
        with self.assertRaises(InsufficientFundsError) as context:
            self.b.execute_transaction(Transaction(-10000, ''))
        self.assertEqual(-5000, context.exception.args[0]['balance'])


