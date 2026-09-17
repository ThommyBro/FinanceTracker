import re

from dataclasses import dataclass, field
from .category import Category
from .account import Account


# Date Format: ISO Format YYYY-MM-DD
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

@dataclass
class Budget:
    category: Category
    monthly_limit: float
    month: str              

    def remaining(self, account: Account) -> float: 
        ...


    def is_exceeded(self, account: Account) -> bool:
        ...


    def usage_percentage(self, account: Account) -> float:
        ...