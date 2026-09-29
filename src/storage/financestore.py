from abc import ABC, abstractmethod

from src.pyFinance.account import Account
from src.pyFinance.budget_tracker import Tracker
from src.pyFinance.budget import Budget
from src.pyFinance.transaction import Transaction
from src.pyFinance.category import Category


class FinanceStore(ABC):

    # =============================
    #. Abstract Methods
    # =============================
    # Methods the different stores have to implement their own way

    @abstractmethod
    def create_account(self, name: str) -> None: ...


    @abstractmethod
    def list_accounts(self) -> list[str]: ...


    @abstractmethod
    def delete_account(self, name: str) -> None: ...

    @abstractmethod
    def add_transaction(self, account_name: str, transaction: Transaction) -> None: ...


    @abstractmethod
    def get_transactions(self, account_name: str) -> list[Transaction]: ...


    @abstractmethod
    def update_transaction(self, account_name: str, transaction_id: int) -> None: ...


    @abstractmethod
    def set_budget(self, account_name: str, budget: Budget) -> None: ...


    @abstractmethod
    def get_budgets(self, account_name: str) -> list[Budget]: ...


    @abstractmethod
    def delete_budget(self, account_name: str, category: Category, month: str) -> None: ...

    # =============================
    #. Concrete Methods
    # =============================
    # direct implementet methods 
    # independent of stores
    
    def get_account(self, account_name: str) -> Account:
        return Account(account_name, self.get_transactions(account_name))

    def get_monthly_summary(self, account_name: str, month: str) -> dict[str, float]:
        account =  Account(account_name, self.get_account(account_name).filter_by_month(month))
        return dict(
            income = account.income_total,
            expenses = account.expense_total,
            balance = account.balance
        )

    def budget_status(self, account_name: str) -> list[tuple[Budget, float]]:
        account = self.get_account(account_name)
        return [(b, b.usage_percentage(account)) for b in self.get_budgets(account_name)]


    def category_breakdown(self, account_name: str) -> dict[Category, float]:
        return self.get_account(account_name).category_breakdown()

    def monthly_summary(self, account_name: str) -> dict[str, dict[str, float]]:
        return self.get_account(account_name).monthly_summary()