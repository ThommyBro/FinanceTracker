from abc import ABC, abstractmethod
from src.pyFinance.account import Account
from src.pyFinance.budget_tracker import Tracker


class ReportGenerator(ABC):
    """Baseclass for CSV and TXT reports"""

    @property
    @abstractmethod
    def file_extension(self) -> str: ...

    @abstractmethod
    def generate_monthly_report(self, account: Account, month: str) -> str: ...

    @abstractmethod
    def generate_category_report(self, account: Account) -> str: ...

    @abstractmethod
    def generate_budget_report(self, tracker: Tracker, account: Account) -> str: ...