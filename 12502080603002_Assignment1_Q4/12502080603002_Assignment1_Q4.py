import csv
from datetime import datetime


def validate_transaction(row):
    """Validate one transaction and return its numeric amount."""

    # Check required fields
    if not row.get("tid") or not row.get("acc"):
        raise ValueError("Missing transaction_id or account_id")

    transaction_type = row.get("type", "").strip().upper()

    if transaction_type not in ("CREDIT", "DEBIT"):
        raise ValueError("Invalid transaction type")

    # Amount must be numeric and greater than zero
    try:
        amount = float(row["amount"])
    except (ValueError, TypeError):
        raise ValueError("Amount is not numeric")

    if amount <= 0:
        raise ValueError("Amount must be greater than zero")

    # Validate timestamp format
    try:
        datetime.strptime(row["time"], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise ValueError("Invalid timestamp")

    return amount


def process_csv(filename):
    balances = {}

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # Create the three required output files
        with open("credit.csv", "w", newline="", encoding="utf-8") as credit_file, \
             open("debit.csv", "w", newline="", encoding="utf-8") as debit_file, \
             open("error.csv", "w", newline="", encoding="utf-8") as error_file:

            credit_writer = csv.DictWriter(
                credit_file,
                fieldnames=reader.fieldnames
            )

            debit_writer = csv.DictWriter(
                debit_file,
                fieldnames=reader.fieldnames
            )

            error_writer = csv.writer(error_file)

            credit_writer.writeheader()
            debit_writer.writeheader()
            error_writer.writerow(reader.fieldnames + ["reason"])

            for row in reader:
                try:
                    amount = validate_transaction(row)
                    account = row["acc"].strip()
                    transaction_type = row["type"].strip().upper()

                    # Update account-wise net balance
                    if transaction_type == "CREDIT":
                        balances[account] = balances.get(account, 0) + amount
                        credit_writer.writerow(row)
                    else:
                        balances[account] = balances.get(account, 0) - amount
                        debit_writer.writerow(row)

                except (ValueError, KeyError) as error:
                    # Store invalid rows but continue with remaining rows
                    error_writer.writerow(
                        list(row.values()) + [str(error)]
                    )

    return balances


def main():
    filename = input("Enter CSV file path: ").strip()

    try:
        balances = process_csv(filename)

        print("\nAccount-wise balance changes:")

        # Sort by absolute balance change in descending order
        result = sorted(
            balances.items(),
            key=lambda item: abs(item[1]),
            reverse=True
        )

        for account, balance in result:
            if balance.is_integer():
                balance = int(balance)
            print(account, balance)

        print("\nFiles created: credit.csv, debit.csv, error.csv")

    except FileNotFoundError:
        print("Error: Input file not found.")
    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    main()