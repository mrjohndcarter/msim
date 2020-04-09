from unittest import TestCase

class Account(object):
    def __init__(self, name, number):
        self.account_holder = name
        self.account_number = number
        self.balance = 0

    def transact(self, amount : float ) -> float:
        self.balance += amount
        return self.balance

class TestGetJiraDate(TestCase):
    def setUp(self) -> None:
        self.a = Account('Alice', 1)

    def test_new_acount(self):
        self.assertEqual(self.a.balance, 0)

    def test_deposit(self):
        self.a.transact(505.50)
        self.assertEqual(self.a.balance, 505.50)
        self.assertEqual(self.a.transact(10), 515.50)

