import re

from dataclasses import dataclass, field
from .transaction_type import TransactionType
from .category import Category
from .transaction import Transaction




@dataclass
class Account:
    """
    ...
    """
    
    name: str
    transactions: list[Transaction] = field(default_factory=list) 
    

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)


    @property
    def balance(self) -> float:
        return sum(ta.signed_amount for ta in self.transactions)


    @property
    def income_total(self) -> float:
        return sum(ta.amount for ta in self.transactions if ta.is_income)


    @property
    def expense_total(self) -> float:
        return sum(ta.amount for ta in self.transactions if ta.is_expense)



    # --- Filter methods --- #

    def filter_by_category(self, category) -> list[Transaction]:
        return [ta for ta in self.transactions if ta.category == category]


    def filter_by_date(self, start: str, end: str) -> list[Transaction]:
        return [ta for ta in self.transactions if ta.date <= end and ta.date >= start]


    def filter_by_type(self, t: TransactionType) -> list[Transaction]:
        return [ta for ta in self.transactions if ta.category == t]


    def search(self, query: str) -> list[Transaction]:
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        return [ta for ta in self.transactions if pattern.search(ta.description)]


    # --- Summaries --- #
    def monthly_summary(self) -> dict[str, dict]:
        month_summary = {f"{m:02d}": {"Income": 0.0, "Expenses": 0.0, "Balance": 0.0}
                   for m in range(1,13)
                   }
        for ta in self.transactions:
            month = ta.date.split("-")[1]
            if ta.is_income:
                month_summary[month]["Income"] += ta.amount
            elif ta.is_expense:
                month_summary[month]["Expenses"] += ta.amount
            month_summary[month]["Balance"] = self.balance

        return month_summary


    def category_breakdown(self) -> dict[Category, float]:
        cat_summary = {}
        for ta in self.transactions:
            cat_summary.setdefault(ta.category, 0.0)
            cat_summary[ta.category] += ta.signed_amount

        return cat_summary

        

    


    
    """
    All methods must be tested!
    """