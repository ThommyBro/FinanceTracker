from src.pyFinance.account import Account
from src.pyFinance.transaction import Transaction
from src.pyFinance.budget import Budget
from src.pyFinance.transaction_type import TransactionType
from src.pyFinance.category import Category


def make_transaction(
    description: str,
    amount: float,
    date: str,
    transaction_type: TransactionType = TransactionType.EXPENSE,
    category: Category = Category.OTHER,
) -> Transaction:

    return Transaction(
        description=description,
        amount=amount,
        transaction_type=transaction_type,
        category=category,
        date=date,
    )


def main():

    account = Account(name="My Account")
    budget = Budget(Category.FOOD, 300.0, "2026-09")

    transactions = [
        make_transaction(
            "Salary",
            3000,
            "2026-09-01",
            TransactionType.INCOME,
            Category.SALARY,
        ),
        make_transaction(
            "Rent",
            900,
            "2026-09-02",
            category=Category.HOUSING,
        ),
        make_transaction(
            "Groceries",
            100,
            "2026-09-05",
            category=Category.FOOD,
        ),
        make_transaction(
            "Restaurant",
            100,
            "2026-09-05",
            category=Category.FOOD,
        ),
        make_transaction(
            "New Bike",
            500,
            "2026-09-12",
            category=Category.OTHER,
        ),
    ]

    for transaction in transactions:
        account.add_transaction(transaction)

    print(f"Account: {account.name}")
    print(f"Income: {account.income_total}")
    print(f"Expenses: {account.expense_total}")
    print(f"Balance: {account.balance}")
    print(f"\nBudget for Food: {budget.monthly_limit}")
    print(f"\nRemaining for Food: {budget.remaining(account)}")
    print(f"\nIs Exceeded: {budget.is_exceeded(account)}")
    print(f"\nUsage percentage: {budget.usage_percentage(account)}")


    # print("\nDaily spending:")
    # print(account.daily_spending("2026-09"))

    # print("\nTop expenses:")
    # for transaction in account.top_n_expenses():
    #     print(f"{transaction.description}: {transaction.amount}")


if __name__ == "__main__":
    main()