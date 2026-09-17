
from dataclasses import dataclass, field
from src.pyFinance.transaction_type import TransactionType
from src.pyFinance.category import Category
from src.pyFinance.transaction import Transaction
from src.pyFinance.budget import Budget
from src.pyFinance.account import Account




@dataclass
class Tracker:
    """
    ...
    """
    budgets: list[Budget] = field(default_factory=list) 
    


    def set_budget(self, category: Category, monthly_limit: float, month: str) -> None:
        ...


    def check_budget(self, account: Account) -> list[tuple[Budget, float]]:
        ...


    def exceeded_budgets(self, account: Account) -> list[Budget]:
        ...
