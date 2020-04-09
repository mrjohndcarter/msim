from Account import Account
from unittest import TestCase


class OverdraftAccount(Account):
    def __init__(self, name, number, overdraft):
        super().__init__(name, number)
        self.overdraft_account = Account(name, number)
        self.overdraft_account.balance = overdraft
        self.overdraft_maximum = overdraft

    def get_overdraft_amount(self):
        return self.overdraft_account.balance

    def transact(self, amount: float) -> float:
# withdraw -> take from balance first, then O/D
# deposit -> put toward O/D first then balance
        # withdrawal logic:
        if amount < 0:
            self.balance += amount

            # if account has gone into negative
            if self.balance < 0:
                self.overdraft_account.transact(self.balance)

        return self.balance

class TestOverdraftAccount(TestCase):
    def setUp(self) -> None:
        self.a = OverdraftAccount('Alice', 1, 500)
        self.b = OverdraftAccount('Bob, ', 2, 750)
        self.c = OverdraftAccount('Carol', 3, 0)

    def test_overdraft_amounts(self):
        self.assertEqual(self.a.get_overdraft_amount(), 500)
        self.assertEqual(self.b.get_overdraft_amount(), 750)
        self.assertEqual(self.c.get_overdraft_amount(), 0)

    def test_overdraft_maximums(self):
        self.assertEqual(self.a.overdraft_maximum, 500)
        self.assertEqual(self.b.overdraft_maximum, 750)
        self.assertEqual(self.c.overdraft_maximum, 0)

    def test_withdraw_with_overdraft(self):
        self.a.transact(-300)
        self.assertEqual(self.a.balance, -300)