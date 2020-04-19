from unittest.case import TestCase
from itertools import repeat

from Account import Account, InsufficientFundsError
from Transaction import Transaction

class TestAccountTransactions(TestCase):
    def setUp(self) -> None:
        self.a = Account('Alice', 1)
        self.a.__transact(1000) # opening balance

    def test_withdrawal(self):
        self.a.execute_transaction(Transaction(-500, 'Groceries'))
        self.assertEqual(500, self.a.balance)
        self.assertEqual(1, len(self.a.transaction_history))

    def test_deposit(self):
        self.a.execute_transaction(Transaction(200, 'Gift'))
        self.assertEqual(1200, self.a.balance)
        self.assertEqual(1, len(self.a.transaction_history))

    def test_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError) as context:
            self.a.execute_transaction(Transaction(-1200, 'Big Purchase'))
        self.assertEqual(-200, context.exception.args[0]['balance'])
        self.assertEqual(-200, self.a.balance)
        self.assertEqual(1, len(self.a.transaction_history))

        with self.assertRaises(InsufficientFundsError) as context:
            self.a.execute_transaction(Transaction(-200, 'Another Purchase'))
        self.assertEqual(-400, context.exception.args[0]['balance'])
        self.assertEqual(-400, self.a.balance)
        self.assertEqual(2, len(self.a.transaction_history))

    def test_overdraft_transactions(self):
        b = Account('Bob', 2, 500)
        b.__transact(500)
        # withdraw into -250 overdraft
        b.execute_transaction(Transaction(-750, 'First transaction'))
        self.assertEqual(-250, b.balance)

        with self.assertRaises(InsufficientFundsError) as context:
            b.execute_transaction(Transaction(-500, 'Second transaction'))
        self.assertEqual(-750, context.exception.args[0]['balance'])
        self.assertEqual(-750, b.balance)
        self.assertEqual(2, len(b.transaction_history))

    def test_transactions_and_balance_consistency(self):
        # verify that we get the same sum by iterating through all transactions.
        c = Account('Carol', 3, 500)
        c.__transact(500)
        for _ in repeat(None, 10):
            c.execute_transaction(Transaction(-50, 'No description'))
        self.assertEqual(0, c.balance)
        self.assertEqual(10, len(c.transaction_history))

        for _ in repeat(None, 10):
            c.execute_transaction(Transaction(25, 'No description'))
        self.assertEqual(250, c.balance)
        self.assertEqual(20, len(c.transaction_history))

        sum = 500 # from opening balance
        for t in c.transaction_history:
            sum += t.amount
            self.assertEqual(sum, t.balance)
        self.assertEqual(sum, c.balance)