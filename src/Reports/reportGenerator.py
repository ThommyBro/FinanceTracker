from abc import ABC, abstractmethod
from pyFinance.account import Account
from pyFinance.budget_tracker import Tracker


class ReportGenerator(ABC):
    """Baseclass for CSV and TXT reports"""

    @abstractmethod
    def generate_monthly_report(self, account: Account, month: str) -> str: ...

    @abstractmethod
    def generate_category_report(self, account: Account) -> str: ...

    @abstractmethod
    def generate_budget_report(self, tracker: Tracker, account: Account) -> str: ...