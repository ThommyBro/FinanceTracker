from abc import ABC, abstractmethod

from src.pyFinance.account import Account
from src.pyFinance.budget_tracker import Tracker
from src.pyFinance.budget import Budget
from src.pyFinance.transaction import Transaction


class FinanceStore(ABC):

    @abstractmethod
    def add_transaction(self, account_name: str, transaction: Transaction) -> None: ...


    @abstractmethod
    def get_transactions(self, account_name: str) -> list[Transaction]: ...


    @abstractmethod
    def get_monthly_summary(self, account_name: str, month: str) -> dict: ... 