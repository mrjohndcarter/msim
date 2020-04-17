from unittest.case import TestCase

from Account import Account, InsufficientFundsError


class TestAccountOverdraft(TestCase):
    def setUp(self) -> None:
        self.a = Account('Alice', 1, 500)
        self.b = Account('Bob, ', 2, 750)
        self.c = Account('Carol', 3, 0)

    def test_overdraft_amounts(self):
        self.assertEqual(500, self.a.overdraft_maximum)
        self.assertEqual(750, self.b.overdraft_maximum)
        self.assertEqual(0, self.c.overdraft_maximum)

    def test_overdraft_maximums(self):
        self.assertEqual(500, self.a.overdraft_maximum)
        self.assertEqual(750, self.b.overdraft_maximum)
        self.assertEqual(0, self.c.overdraft_maximum)

    def test_withdraw_with_overdraft(self):
        self.a.transact(-300)
        self.assertEqual(-300, self.a.balance)
        self.assertEqual(200, self.a.get_overdraft_amount_available())

    def test_withdrawal_while_overdrawn(self):
        # withdraw 100 from an account with 0 and 500 o/d
        # balance should be -100 and od available 400
        self.a.transact(-100)
        self.assertEqual(-100, self.a.balance)
        self.assertEqual(400, self.a.get_overdraft_amount_available())

        # withdraw 200 from an account already overdrawn (-100)
        # balance should be -300, and od available 200
        self.a.transact(-200)
        self.assertEqual(-300, self.a.balance)
        self.assertEqual(200, self.a.get_overdraft_amount_available())

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
        self.assertEqual(200, self.a.get_overdraft_amount_available())

        # deposit 100
        # balance should be -200 and od available 300
        self.a.transact(100)
        self.assertEqual(-200, self.a.balance)
        self.assertEqual(300, self.a.get_overdraft_amount_available())

        # deposit 200
        # balance should be 0 and od available 500
        self.a.transact(200)
        self.assertEqual(0, self.a.balance)
        self.assertEqual(500, self.a.get_overdraft_amount_available())

    def test_deposit_in_overdraft_to_positive_balance(self):
        # withdraw 450 from o/d
        # balance should be -450 and od available 50
        self.a.transact(-450)
        self.assertEqual(-450, self.a.balance)
        self.assertEqual(50, self.a.get_overdraft_amount_available())

        # deposit 1000
        # balance should be 550 and od available 500
        self.a.transact(1000)
        self.assertEqual(550, self.a.balance)
        self.assertEqual(500, self.a.get_overdraft_amount_available())

    def test_withdrawal_beyond_overdraft(self):
        # from a balance of 0, with a 500 overdraft, withdraw 500
        self.a.transact(-500)
        self.assertEqual(-500, self.a.balance)
        self.assertEqual(0, self.a.get_overdraft_amount_available())

        # try to withdraw another 100
        with self.assertRaises(InsufficientFundsError) as context:
            self.a.transact(-100)
            self.assertEqual(-100, context.exception.args[0]['balance'])