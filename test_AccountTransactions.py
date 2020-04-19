from unittest.case import TestCase
from itertools import repeat

from Account import Account, InsufficientFundsError
from AccountTransaction import AccountTransaction


class TestAccountTransactions(TestCase):
    def setUp(self) -> None:
        self.a = Account('Alice', 1, opening_balance=1000.0)

    def test_withdrawal(self):
        self.a.execute_transaction(AccountTransaction(-500, 'Groceries'))
        self.assertEqual(500, self.a.balance)
        self.assertEqual(1, len(self.a.transaction_history))

    def test_deposit(self):
        self.a.execute_transaction(AccountTransaction(200, 'Gift'))
        self.assertEqual(1200, self.a.balance)
        self.assertEqual(1, len(self.a.transaction_history))

    def test_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError) as context:
            self.a.execute_transaction(AccountTransaction(-1200, 'Big Purchase'))
        self.assertEqual(-200, context.exception.args[0]['balance'])
        self.assertEqual(-200, self.a.balance)
        self.assertEqual(1, len(self.a.transaction_history))

        with self.assertRaises(InsufficientFundsError) as context:
            self.a.execute_transaction(AccountTransaction(-200, 'Another Purchase'))
        self.assertEqual(-400, context.exception.args[0]['balance'])
        self.assertEqual(-400, self.a.balance)
        self.assertEqual(2, len(self.a.transaction_history))

    def test_overdraft_transactions(self):
        b = Account('Bob', 2, 500, opening_balance=500)

        # withdraw into -250 overdraft
        b.execute_transaction(AccountTransaction(-750, 'First transaction'))
        self.assertEqual(-250, b.balance)

        with self.assertRaises(InsufficientFundsError) as context:
            b.execute_transaction(AccountTransaction(-500, 'Second transaction'))
        self.assertEqual(-750, context.exception.args[0]['balance'])
        self.assertEqual(-750, b.balance)
        self.assertEqual(2, len(b.transaction_history))

    def test_transactions_and_balance_consistency(self):
        # verify that we get the same sum by iterating through all transactions.
        c = Account('Carol', 3, overdraft=500, opening_balance=500)

        for _ in repeat(None, 10):
            c.execute_transaction(AccountTransaction(-50, 'No description'))
        self.assertEqual(0, c.balance)
        self.assertEqual(10, len(c.transaction_history))

        for _ in repeat(None, 10):
            c.execute_transaction(AccountTransaction(25, 'No description'))
        self.assertEqual(250, c.balance)
        self.assertEqual(20, len(c.transaction_history))

        sum = 500  # from opening balance
        for t in c.transaction_history:
            sum += t.amount
            self.assertEqual(sum, t.balance)
        self.assertEqual(sum, c.balance)

    def test_transaction_update(self):
        d = Account('David', 4)

        t = AccountTransaction(100, 'small deposit')
        t.timestamp = None
        t.balance = 0
        d.execute_transaction(t)

        self.assertIsNotNone(t.timestamp)
        self.assertEqual(100, t.balance)

    def test_transaction_rollback(self):
        e = Account('Eunice', 5)
        t = AccountTransaction(-500, 'Transaction that should fail.')

        with self.assertRaises(InsufficientFundsError) as context:
            e.execute_transaction(t)

        self.assertEqual(-500, e.balance)
        self.assertEqual(-500, t.balance)

        new_transaction = e.rollback_transaction(t)

        self.assertEqual(0, e.balance)
        self.assertEqual(0, new_transaction.balance)

        self.assertEqual(2, len(e.transaction_history))

    def test_failing_transaction_rollback(self):
        t = AccountTransaction(400, "not associated with account")
        with self.assertRaises(KeyError) as context:
            self.a.rollback_transaction(t)

        self.assertEqual(1000, self.a.balance)
        self.assertEqual(0, len(self.a.transaction_history))