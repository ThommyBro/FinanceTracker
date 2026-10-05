
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
        for budget in self.budgets:
            if category == budget.category and month == budget.month:
                budget.monthly_limit = monthly_limit
                return
        self.budgets.append(Budget(category, monthly_limit, month))


    def delete_budget(self, category: Category, month: str) -> None:
        exists = [b for b in self.budgets if (b.category, b.month) == (category, month)]
        if not exists:
            raise ValueError("Budget not found")
        self.budgets.remove(exists[0])


    def check_budgets(self, account: Account) -> list[tuple[Budget, float]]:
        return [(b, b.usage_percentage(account)) for b in self.budgets]


    def exceeded_budgets(self, account: Account) -> list[Budget]:
        return [b for b in self.budgets if b.is_exceeded(account)]
