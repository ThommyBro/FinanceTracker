
from dataclasses import dataclass, field
from .transaction_type import TransactionType
from .category import Category
from .transaction import Transaction
from .budget import Budget
from .account import Account




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
