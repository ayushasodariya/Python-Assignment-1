class BankError(Exception):
    """Base exception for banking errors."""
    pass


class AccountNotFoundError(BankError):
    pass


class InvalidAmountError(BankError):
    pass


class InsufficientBalanceError(BankError):
    pass


class Account:
    def __init__(self, account_id, balance):
        if not account_id:
            raise ValueError("Account ID cannot be empty")

        if balance < 0:
            raise ValueError("Initial balance cannot be negative")

        self.account_id = account_id
        self._balance = balance
        self.transaction_history = []

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")

        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")

        if amount > self._balance:
            raise InsufficientBalanceError("Insufficient balance")

        self._balance -= amount


class Transaction:
    def __init__(self, transaction_type, account_id, amount,
                 target_account=None):
        self.transaction_type = transaction_type
        self.account_id = account_id
        self.amount = amount
        self.target_account = target_account


class Bank:
    def __init__(self):
        self.accounts = {}
        self.batch_snapshot = None
        self.batch_number = 0
        self.batch_failed = False

    def add_account(self, account_id, balance):
        if account_id in self.accounts:
            raise BankError("Duplicate account")

        self.accounts[account_id] = Account(account_id, balance)

    def get_account(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFoundError(
                f"Account {account_id} not found"
            )

        return self.accounts[account_id]

    def deposit(self, account_id, amount):
        account = self.get_account(account_id)
        account.deposit(amount)

        account.transaction_history.append(
            Transaction("DEPOSIT", account_id, amount)
        )

    def withdraw(self, account_id, amount):
        account = self.get_account(account_id)
        account.withdraw(amount)

        account.transaction_history.append(
            Transaction("WITHDRAW", account_id, amount)
        )

    def transfer(self, from_account, to_account, amount):
        sender = self.get_account(from_account)
        receiver = self.get_account(to_account)

        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")

        # Both accounts are changed only after validation succeeds.
        sender.withdraw(amount)
        receiver.deposit(amount)

        sender.transaction_history.append(
            Transaction("TRANSFER", from_account, amount, to_account)
        )

    def begin_batch(self):
        if self.batch_snapshot is not None:
            raise BankError("Batch already active")

        # Save balances so they can be restored if the batch fails.
        self.batch_snapshot = {
            account_id: account.balance
            for account_id, account in self.accounts.items()
        }

        self.batch_number += 1
        self.batch_failed = False

    def end_batch(self):
        if self.batch_snapshot is None:
            raise BankError("No active batch")

        if self.batch_failed:
            # Restore every account to its pre-batch balance.
            for account_id, balance in self.batch_snapshot.items():
                self.accounts[account_id]._balance = balance

            failed = True
        else:
            failed = False

        self.batch_snapshot = None
        self.batch_failed = False

        return failed


def read_positive_amount(value):
    """Convert input to a positive integer."""
    try:
        amount = int(value)

        if amount <= 0:
            raise ValueError

        return amount

    except ValueError:
        raise InvalidAmountError("Amount must be a positive integer")


def process_operation(bank, operation):
    parts = operation.split()

    if not parts:
        raise BankError("Empty operation")

    command = parts[0]

    if command == "DEPOSIT":
        if len(parts) != 3:
            raise BankError("Invalid DEPOSIT format")

        account = parts[1]
        amount = read_positive_amount(parts[2])
        bank.deposit(account, amount)

    elif command == "WITHDRAW":
        if len(parts) != 3:
            raise BankError("Invalid WITHDRAW format")

        account = parts[1]
        amount = read_positive_amount(parts[2])
        bank.withdraw(account, amount)

    elif command == "TRANSFER":
        if len(parts) != 4:
            raise BankError("Invalid TRANSFER format")

        from_account = parts[1]
        to_account = parts[2]
        amount = read_positive_amount(parts[3])

        bank.transfer(from_account, to_account, amount)

    else:
        raise BankError("Unknown operation")


def main():
    try:
        # Read number of accounts.
        n = int(input().strip())

        if n <= 0:
            raise ValueError("Number of accounts must be positive")

        bank = Bank()

        # Read initial account data.
        for _ in range(n):
            parts = input().split()

            if len(parts) != 2:
                raise ValueError("Invalid account format")

            account_id = parts[0]
            balance = int(parts[1])

            bank.add_account(account_id, balance)

        q = int(input().strip())

        if q < 0:
            raise ValueError("Number of operations cannot be negative")

        failed_batches = []

        # Process all operations.
        for _ in range(q):
            operation = input().strip()

            if operation == "BATCH_BEGIN":
                bank.begin_batch()

            elif operation == "BATCH_END":
                if bank.end_batch():
                    failed_batches.append(bank.batch_number)

            else:
                try:
                    process_operation(bank, operation)

                except BankError as error:
                    # If inside a batch, mark it for rollback.
                    if bank.batch_snapshot is not None:
                        bank.batch_failed = True
                    else:
                        print(type(error).__name__, "-", error)

        # Required output: failed batch numbers.
        for batch_number in failed_batches:
            print(f"FAILED {batch_number}")

        # Print final balances in account ID order.
        for account_id in sorted(bank.accounts):
            print(account_id, bank.accounts[account_id].balance)

    except (ValueError, BankError) as error:
        print("INPUT ERROR:", error)


if __name__ == "__main__":
    main()