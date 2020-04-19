from Account import Account


class Bank(object):
    account_assigned = 0

    def __init__(self, institution_number):
        self.accounts = []

    def create_account(self, name: str, overdraft: float, opening_balance: float) -> Account:
        new_account = Account(name, Bank.account_assigned, overdraft, opening_balance)
        self.accounts.append(new_account)
        Bank.account_assigned = Bank.account_assigned + 1
        return new_account
