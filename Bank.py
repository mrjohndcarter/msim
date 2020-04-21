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

    def find_account(self, account_number) -> Account:
        return next(filter(lambda a: a.account_number == account_number, self.accounts))

    def internal_transfer(self, source_account_number, destination_account_number, amount : float) -> tuple:
        source_account = self.find_account(source_account_number)
        destination_account_number = self.find_account(destination_account_number)