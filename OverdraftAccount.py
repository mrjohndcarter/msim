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

            # case 0 - withdrawal covered by balance
            if self.balance + amount >= 0:
                self.balance += amount

            # case 1 - withdrawal cannot be covered by balance
            elif self.balance + amount < 0:
                remaining_after_account_withdrawal = abs(amount) - self.balance
                self.balance += amount
                self.overdraft_account.transact(-remaining_after_account_withdrawal)

        return self.balance


class TestOverdraftAccount(TestCase):
    def setUp(self) -> None:
        self.a = OverdraftAccount('Alice', 1, 500)
        self.b = OverdraftAccount('Bob, ', 2, 750)
        self.c = OverdraftAccount('Carol', 3, 0)

    def test_overdraft_amounts(self):
        self.assertEqual(500, self.a.get_overdraft_amount())
        self.assertEqual(750, self.b.get_overdraft_amount())
        self.assertEqual(0, self.c.get_overdraft_amount())

    def test_overdraft_maximums(self):
        self.assertEqual(500, self.a.overdraft_maximum)
        self.assertEqual(750, self.b.overdraft_maximum)
        self.assertEqual(0, self.c.overdraft_maximum)

    def test_withdraw_with_overdraft(self):
        self.a.transact(-300)
        self.assertEqual(-300, self.a.balance)
        self.assertEqual(200, self.a.overdraft_account.balance)

    def test_withdrawal_while_overdrawn(self):
        # withdraw 100 from an account with 0 and 500 o/d
        # balance should be -100 and od available 400
        self.a.transact(-100)
        self.assertEqual(-100, self.a.balance)
        self.assertEqual(400, self.a.overdraft_account.balance)

        # withdraw 200 from an account already overdrawn (-100)
        # balance should be -300, and od available 200
        self.a.transact(-200)
        self.assertEqual(-300, self.a.balance)
        self.assertEqual(200, self.a.overdraft_account.balance)
