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
        """Budget limit minus spent in category for that month"""
        relevant_transactions = account.filter_by_category(self.category)
        monthly_budget = self.monthly_limit
        for ta in relevant_transactions:
            monthly_budget -= ta.amount
        return monthly_budget


    def is_exceeded(self, account: Account) -> bool:
        return self.remaining(account) < 0


    def usage_percentage(self, account: Account) -> float:
        return (
            round(
                (self.monthly_limit - self.remaining(account)) / self.monthly_limit * 100
            ,2)
        )