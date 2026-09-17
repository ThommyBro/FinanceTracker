
from dataclasses import dataclass, field
from pyFinance.category import Category
from pyFinance.account import Account


@dataclass
class Budget:
    category: Category
    monthly_limit: float
    month: str              # ISO Format YYYY-MM-DD

    def remaining(self, account: Account) -> float: 
        ...


    def is_exceeded(self, account: Account) -> bool:
        ...


    def usage_percentage(self, account: Account) -> float:
        ...