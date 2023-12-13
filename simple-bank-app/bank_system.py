import textwrap
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime


class Costumer:

    def __init__(self, address):
        self.address = address
        self.accounts = []

    def do_transaction(self, account, transaction):
        return transaction.log_transaction(account)

    def create_account(self, account):
        self.accounts.append(account)


class IndividualAccount(Costumer):

    def __init__(self, address, id_number, name, birth_date):
        super().__init__(address)

        self.id_number = id_number
        self.name = name
        self.birth_date = birth_date


class Account:
    def __init__(self, account, costumer):
        self._balance = 0
        self._account = account
        self._agency = "0001"
        self._costumer = costumer
        self._logs = TransactionLogs()

    @classmethod
    def new_account(cls, costumer, account):
        return cls(account, costumer)

    @property
    def balance(self):
        return self._balance

    @property
    def account(self):
        return self._account

    @property
    def agency(self):
        return self._agency

    @property
    def costumer(self):
        return self._costumer

    @property
    def logs(self):
        return self._logs

    def __str__(self):
        return f"\nOwner:\t\t{self.costumer.name} \nAgency:\t\t{self.agency} \nAccount:\t{self.account}"

    def to_withdraw(self, amount):
        balance = self.balance
        insufficient_funds = amount > balance

        if insufficient_funds:
            print(f"\nOperation Failed! Insufficient funds, your balance is $: {self.balance}")

        elif amount > 0:
            self._balance -= amount
            print("Withdraw successful!")
            return True

        else:
            print("Operation failed! Invalid amount.")

        return False

    def to_deposit(self, amount) -> bool:

        if amount > 0:
            self._balance += amount
            print("Deposit successful!")

        else:
            print("Operation failed! Invalid amount.")
            return False

        return True


class CheckingAccount(Account):

    def __init__(self, account, costumer, withdraw_amount_limit=500.0, max_withdrawals=3):
        super().__init__(account, costumer)

        self.withdraw_amount_limit = withdraw_amount_limit
        self.max_withdrawals = max_withdrawals

    def to_withdraw(self, amount):

        withdrawals_count = len([transaction for transaction in self.logs.transactions if transaction["type"]
                                 == Withdraw.__name__])

        exceeded_amount_limit = amount > self.withdraw_amount_limit
        exceeded_max_withdrawals = withdrawals_count >= self.max_withdrawals

        if exceeded_amount_limit:
            print(f"\nOperation failed! \nYour withdraw limit is {self.withdraw_amount_limit}")

        elif exceeded_max_withdrawals:
            print(f"\nOperation failed! \nMaximum number of withdrawals exceeded.")

        else:
            return super().to_withdraw(amount)

        return False

    def __str__(self):
        return f"\nOwner: \t{self.costumer.name} \n Agency: \t\t{self.agency} \n Account: \t\t{self.account}"


class TransactionLogs:

    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
        self._transactions.append({"type": transaction.__class__.__name__, "amount": transaction.amount,
                                   "date": datetime.now().strftime("%m-%d-%Y %H:%M:%S"), })


class Transaction(ABC):

    @property
    @abstractmethod
    def amount(self):
        return self.amount

    @abstractmethod
    def log_transaction(self, account):
        pass


class Withdraw(Transaction):

    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def log_transaction(self, account):
        transaction_successful = account.to_withdraw(self.amount)

        if transaction_successful:
            account.logs.add_transaction(self)


class Deposit(Transaction):

    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def log_transaction(self, account):
        transaction_successful = account.to_deposit(self.amount)

        if transaction_successful:
            account.logs.add_transaction(self)


def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDeposit
    [2]\tWithdraw
    [3]\tAccount Statement
    [4]\tCreate User
    [5]\tCreate Account
    [6]\tShow Accounts
    [0]\tExit
    => """
    return input(textwrap.dedent(menu))


def op_deposit(costumers):
    id_number = input("ID number: ")
    costumer = filter_costumer(id_number, costumers)

    if not costumer:
        print("Costumer does not exist")
        return

    account = get_account(costumer)
    if not account:
        print("Costumer does not have an account!")
        return

    amount = float(input("Deposit amount: "))

    transaction = Deposit(amount)

    costumer.do_transaction(account, transaction)


def op_withdraw(costumers):
    id_number = input("ID number: ")
    costumer = filter_costumer(id_number, costumers)

    if not costumer:
        print("Register not found!")
        return

    account = get_account(costumer)
    if not account:
        print("User does not have an account!")
        return

    amount = float(input("Withdraw amount: "))
    transaction = Withdraw(amount)

    costumer.do_transaction(account, transaction)


def show_account_statement(costumers):
    id_number = input("ID number: ")
    costumer = filter_costumer(id_number, costumers)

    if not costumer:
        print("Costumer does not exist!")
        return

    account = get_account(costumer)
    if not account:
        print("Costumer does not have an account!")
        return

    print("\n================ EXTRATO ================")
    transactions = account.logs.transactions

    bank_statement = ""
    if not transactions:
        bank_statement = "Transactions not found!"
    else:
        for transaction in transactions:
            bank_statement += f"\n{transaction['type']}:\t$ {transaction['amount']:.2f} "

    print(bank_statement)
    print(f"\nBalance:\t$ {account.balance:.2f}")
    print("=========================================")


def create_costumer(costumers):
    id_number = input("ID number: ")
    costumer = filter_costumer(id_number, costumers)

    if costumer:
        print("\nThere is already a costumer with this id number!")
        return

    name = input("Full Name: ")
    birth_date = input("Birth date (mm-dd-yyyy): ")
    address = input("Address (n, street - district city/state): ")

    costumer = IndividualAccount(name=name, birth_date=birth_date, id_number=id_number, address=address)

    costumers.append(costumer)

    print("Register created with sucess!")


def create_account(account, costumers, accounts):
    id_number = input("Costumer ID number: ")
    costumer = filter_costumer(id_number, costumers)

    if not costumer:
        print("Costumer does not exist!")
        return

    account = CheckingAccount.new_account(costumer=costumer, account=account)
    accounts.append(account)
    costumer.accounts.append(account)

    print("New account created!")


def filter_costumer(id_number, costumers) -> Costumer:
    filtered_costumer = [costumer for costumer in costumers if costumer.id_number == id_number]
    return filtered_costumer[0] if filtered_costumer else None


def get_account(costumer):
    if not costumer.accounts:
        print("Costumer does not have an account!")
        return

    return costumer.accounts[0]


def show_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        print(textwrap.dedent(str(account)))


def main():
    costumers = []
    accounts = []

    while True:
        option = menu()

        if option == "1":
            op_deposit(costumers)

        elif option == "2":
            op_withdraw(costumers)

        elif option == "3":
            show_account_statement(costumers)

        elif option == "4":
            create_costumer(costumers)

        elif option == "5":
            account = len(accounts) + 1
            create_account(account, costumers, accounts)

        elif option == "6":
            show_accounts(accounts)

        elif option == "0":
            break

        else:
            print("Invalid option, please select a valid option")


main()
