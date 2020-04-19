from unittest.case import TestCase

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
