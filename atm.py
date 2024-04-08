# Task 1: ATM Interface
# (c) Kaushik Goswami 2024 onwards

class Account:
    def __init__(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance

class Transaction:
    def __init__(self, type, amount):
        self.type = type
        self.amount = amount

class Bank:
    def __init__(self):
        self.accounts = {}  # Stores accounts with user_id as key
        self.transactions = {}  # Stores transactions lists with user_id as key

    def add_account(self, account):
        self.accounts[account.user_id] = account
        self.transactions[account.user_id] = []

    def record_transaction(self, user_id, transaction):
        self.transactions[user_id].append(transaction)

    def validate_login(self, user_id, pin):
        account = self.accounts.get(user_id)
        if account and account.pin == pin:
            return True
        return False

    def get_account(self, user_id):
        return self.accounts.get(user_id)

class ATM:
    def __init__(self, bank):
        self.bank = bank
        self.current_user_id = None

    def start(self):
        user_id = input("Enter your user ID: ")
        pin = input("Enter your PIN: ")
        if self.bank.validate_login(user_id, pin):
            self.current_user_id = user_id
            print("Login successful!")
            self.show_menu()
        else:
            print("Invalid credentials!")

    def show_menu(self):
        while True:
            print("\n1. Transactions History\n2. Withdraw\n3. Deposit\n4. Transfer\n5. Quit")
            choice = input("Choose an option: ")
            if choice == "1":
                self.show_transactions()
            elif choice == "2":
                self.withdraw()
            elif choice == "3":
                self.deposit()
            elif choice == "4":
                self.transfer()
            elif choice == "5":
                print("Thank you for using the ATM. Goodbye!")
                self.current_user_id = None
                break
            else:
                print("Invalid option!")

    def show_transactions(self):
        transactions = self.bank.transactions[self.current_user_id]
        if transactions:
            for transaction in transactions:
                print(f"Type: {transaction.type}, Amount: {transaction.amount}")
        else:
            print("No transactions found.")

    def withdraw(self):
        amount = float(input("Enter amount to withdraw: "))
        account = self.bank.get_account(self.current_user_id)
        if account.balance >= amount:
            account.balance -= amount
            self.bank.record_transaction(self.current_user_id, Transaction("Withdraw", amount))
            print(f"Withdrawn: {amount}. New Balance: {account.balance}")
        else:
            print("Insufficient funds.")

    def deposit(self):
        amount = float(input("Enter amount to deposit: "))
        account = self.bank.get_account(self.current_user_id)
        account.balance += amount
        self.bank.record_transaction(self.current_user_id, Transaction("Deposit", amount))
        print(f"Deposited: {amount}. New Balance: {account.balance}")

    def transfer(self):
        recipient_id = input("Enter reciever's user ID: ")
        amount = float(input("Enter amount to transfer: "))
        sender_account = self.bank.get_account(self.current_user_id)
        recipient_account = self.bank.get_account(recipient_id)

        if sender_account.balance >= amount and recipient_account:
            sender_account.balance -= amount
            recipient_account.balance += amount
            self.bank.record_transaction(self.current_user_id, Transaction("Transfer Out", amount))
            self.bank.record_transaction(recipient_id, Transaction("Transfer In", amount))
            print(f"Transferred: {amount} to {recipient_id}. New Balance: {sender_account.balance}")
        else:
            print("Transfer failed. Check the recipient ID and your balance.")

def main():
    # Creating a bank and adding accounts (2 by default)
    bank = Bank()
    bank.add_account(Account("user1", "1234", 10000))
    bank.add_account(Account("user2", "5678", 15000))

    # Starting ATM
    atm = ATM(bank)
    atm.start()

if __name__ == "__main__":
    main()
