from unittest.case import TestCase

from Account import AmountError, InsufficientFundsError
from Bank import Bank


class TestBank(TestCase):
    def setUp(self) -> None:
        self.bankA = Bank(1003)

    def test_new_account(self):
        new_account = self.bankA.create_account('Leroy Jenkins', 1000, 1000)
        self.assertEqual(1000, new_account.balance)
        self.assertEqual(1000, new_account.overdraft_maximum)

        newer_account = self.bankA.create_account('Bob Newhart', 500, 500)
        self.assertNotEqual(new_account.account_number, newer_account.account_number)
        self.assertEqual(2, len(self.bankA.accounts))

    def test_find_account(self):
        my_account = None

        # put the account somewhere in the list
        for i in range(0, 100):
            if i == 77:
                my_account = self.bankA.create_account('Meme Melrose', 100, 600)
            else:
                self.bankA.create_account('A Nonymous', 100, 100)

        self.assertEqual(my_account, self.bankA.find_account(my_account.account_number))

    def test_intrabank_transfer(self):
        source_account = self.bankA.create_account('Scrooge McDuck', overdraft=1000, opening_balance=1000000)
        destination_account = self.bankA.create_account('Donald Duck', overdraft=100, opening_balance=50)

        self.bankA.internal_transfer(source_account.account_number, destination_account.account_number, 0.99)
        self.assertEqual(50.99, destination_account.balance)
        self.assertEqual(1, len(source_account.transaction_history))
        self.assertEqual(1, len(destination_account.transaction_history))

    def test_intrabank_transfer_fail(self):
        source_account = self.bankA.create_account('Huey', overdraft=0, opening_balance=50)
        destination_account = self.bankA.create_account('Donald Duck', overdraft=100, opening_balance=50)

        with self.assertRaises(InsufficientFundsError) as context:
            self.bankA.internal_transfer(source_account.account_number, destination_account.account_number, 1000)

        self.assertEqual(50, source_account.balance)
        self.assertEqual(50, destination_account.balance)

        # should have an in and out transaction (from rollback)
        self.assertEqual(2, len(source_account.transaction_history))

        # destination account should be none the wiser
        self.assertEqual(0, len(destination_account.transaction_history))

        with self.assertRaises(AmountError) as context:
            self.bankA.internal_transfer(source_account.account_number, destination_account.account_number, -100.0)

        with self.assertRaises(AmountError) as context:
            self.bankA.internal_transfer(source_account.account_number, destination_account.account_number, -0.0)
