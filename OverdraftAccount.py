from Account import Account, InsufficientFundsError
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

            # case 1 - withdrawal can be partially covered by balance
            elif self.balance > 0:
                remaining_after_account_withdrawal = self.balance + amount # this will be negative
                self.balance += amount
                self.overdraft_account.transact(remaining_after_account_withdrawal)

            # case 2 - withdrawal must be completely covered by o/d
            else:
                self.balance += amount
                self.overdraft_account.transact(amount)

        # deposit logic
        else:

            # case 0 - account is positive
            if self.balance >= 0:
                self.balance += amount

            # case 1 - deposit will be offset (but not completely) by o/d
            # amount to be deposited is greater than abs of balance (which is negative)
            elif self.balance < 0 and amount > abs(self.balance):
                remaining_after_od_deposit = amount - abs(self.balance)
                self.overdraft_account.transact(amount - remaining_after_od_deposit)
                self.balance += amount

            # case 2 - deposit completely used toward o/d
            else:
                self.balance += amount
                self.overdraft_account.transact(amount)

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

    def test_deposit_not_in_overdraft(self):
        self.b.transact(550)
        self.assertEqual(550, self.b.balance)
        self.b.transact(450)
        self.assertEqual(1000, self.b.balance)

    def test_deposit_in_overdraft(self):
        # withdraw 300 from o/d
        # balance should be -300 and od available 200
        self.a.transact(-300)
        self.assertEqual(-300, self.a.balance)
        self.assertEqual(200, self.a.overdraft_account.balance)

        # deposit 100
        # balance should be -200 and od available 300
        self.a.transact(100)
        self.assertEqual(-200, self.a.balance)
        self.assertEqual(300, self.a.overdraft_account.balance)

        # deposit 200
        # balance should be 0 and od available 500
        self.a.transact(200)
        self.assertEqual(0, self.a.balance)
        self.assertEqual(500, self.a.overdraft_account.balance)

    def test_deposit_in_overdraft_to_positive_balance(self):
        # withdraw 450 from o/d
        # balance should be -450 and od available 50
        self.a.transact(-450)
        self.assertEqual(-450, self.a.balance)
        self.assertEqual(50, self.a.overdraft_account.balance)

        # deposit 1000
        # balance should be 550 and od available 500
        self.a.transact(1000)
        self.assertEqual(550, self.a.balance)
        self.assertEqual(500, self.a.overdraft_account.balance)

    def test_withdrawal_beyond_overdraft(self):
        # from a balance of 0, with a 500 overdraft, withdraw 500
        self.a.transact(-500)
        self.assertEqual(-500, self.a.balance)
        self.assertEqual(0, self.a.overdraft_account.balance)

        # try to withdraw another 100
        with self.assertRaises(InsufficientFundsError) as context:
            self.a.transact(-100)
            self.assertEqual(-100, context.exception.args[0]['balance'])

