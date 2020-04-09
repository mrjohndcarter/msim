from Account import Account
from unittest import TestCase


class OverdraftAccount(Account):
    def __init__(self, name, number, overdraft):
        super().__init__(name, number)
        self.overdraft_account = Account(name, number)
        self.overdraft_account.balance = overdraft

    def get_overdraft_amount(self):
        return self.overdraft_account.balance


class TestOverdraftAccount(TestCase):
    def setUp(self) -> None:
        self.a = OverdraftAccount('Alice', 1, 500)
        self.b = OverdraftAccount('Bob, ', 2, 750)
        self.c = OverdraftAccount('Carol', 3, 0)

    def test_overdraft_amounts(self):
        self.assertEqual(self.a.get_overdraft_amount(), 500)
        self.assertEqual(self.b.get_overdraft_amount(), 750)
        self.assertEqual(self.c.get_overdraft_amount(), 0)
