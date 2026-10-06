
import pytest


from src.pyFinance.transaction_type import TransactionType
from src.pyFinance.category import Category
from src.pyFinance.budget import Budget
from src.pyFinance.transaction import Transaction
from src.storage.memorystore import InMemoryStore
from src.pyFinance.exceptions import FinanceError, NotFoundError


def test_duplicate_account_raises_finance_error():
    store = InMemoryStore()

    store.create_account("My Account")

    with pytest.raises(FinanceError):
        store.create_account("My Account")

    assert store.list_accounts() == ["My Account"]




def test_update_transaction():
    store = InMemoryStore()
    store.create_account("My Account")

    transaction = Transaction(
        description="Groceries",
        amount=100,
        transaction_type=TransactionType.EXPENSE,
        category=Category.FOOD,
        date="2026-09-05",
    )

    store.add_transaction("My Account", transaction)

    transaction_id = transaction.id

    store.update_transaction(
        account_name="My Account",
        transaction_id=transaction_id,
        description="Weekly Groceries",
        amount=150,
        transaction_type=TransactionType.EXPENSE,
        category=Category.FOOD,
        date="2026-09-06",
        tags={"weekly"},
    )

    updated = store._transaction("My Account", transaction_id)

    assert updated.id == transaction_id
    assert updated.description == "Weekly Groceries"
    assert updated.amount == 150
    assert updated.date == "2026-09-06"
    assert updated.tags == {"weekly"}



def test_update_transaction_raises_valueerror():
    store = InMemoryStore()
    store.create_account("My Account")

    transaction = Transaction(
        description="Groceries",
        amount=100,
        transaction_type=TransactionType.EXPENSE,
        category=Category.FOOD,
        date="2026-09-05",
    )

    store.add_transaction("My Account", transaction)

    transaction_id = transaction.id

    with pytest.raises(ValueError) as exc:
        store.update_transaction(
            account_name="My Account",
            transaction_id=transaction_id,
            description="Groceries",
            amount=-100,
            transaction_type=TransactionType.EXPENSE,
            category=Category.FOOD,
            date="2026-09-05",
            tags=set(),
        )
    assert str(exc.value) ==  "Amount must be positive. You typed '-100'."
    assert transaction.amount == 100


def test_get_transaction_for_unknown_account_raises_NotFoundError():
    store = InMemoryStore()

    with pytest.raises(NotFoundError) as exc:
        store.get_transactions("My Account")

    assert str(exc.value) == "Account not found."

def test_budget_cycle():
    store = InMemoryStore()
    store.create_account("My Account")

    food_budget = Budget(
        Category.FOOD,
        100.0,
        "2026-12"
    )

    store.set_budget("My Account", food_budget)

    budgets = store.get_budgets("My Account")

    assert len(budgets) == 1
    assert budgets[0] == food_budget

    store.delete_budget("My Account", Category.FOOD, "2026-12")
    budgets_after_delete = store.get_budgets("My Account")
    assert len(budgets_after_delete) == 0





