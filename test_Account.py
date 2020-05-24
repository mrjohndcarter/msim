from unittest.case import TestCase

from Account import Account, InsufficientFundsError
from AccountTransaction import AccountTransaction

class TestAccount(TestCase):
    def setUp(self) -> None:
        self.a = Account('Alice', 1)
        self.b = Account('Bob', 2, opening_balance=1000.0)

    def test_new_account(self):
        self.assertEqual(0, self.a.balance)

    def test_deposit(self):
        self.a.execute_transaction(AccountTransaction(505.50, ''))
        self.assertEqual(505.50, self.a.balance)
        self.assertEqual(515.50, self.a.execute_transaction(AccountTransaction(10, '')))

    def test_withdrawal_no_overdraft(self):
        self.b.execute_transaction(AccountTransaction(-500, ''))
        self.assertEqual(500, self.b.balance)
        self.assertEqual(400, self.b.execute_transaction(AccountTransaction(-100, '')))

    def test_withdrawal_no_overdraft_attempted_overdraw(self):
        with self.assertRaises(InsufficientFundsError) as context:
            self.a.execute_transaction(AccountTransaction(-500, ''))
        self.assertEqual(-500, context.exception.args[0]['balance'])

        self.b.execute_transaction(AccountTransaction(4000, ''))
        with self.assertRaises(InsufficientFundsError) as context:
            self.b.execute_transaction(AccountTransaction(-10000, ''))
        self.assertEqual(-5000, context.exception.args[0]['balance'])

    def test_update_transaction(self):
        t = AccountTransaction(-500, '')
        self.b.execute_transaction(t)
        self.assertEqual(500, t.balance)

    def test_print_transactions(self):
        self.b.get_transaction_history(None, None)
