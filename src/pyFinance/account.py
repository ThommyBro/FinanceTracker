import re

from dataclasses import dataclass, field
from .transaction_type import TransactionType
from .category import Category
from .transaction import Transaction




@dataclass
class Account:

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
        """Returns transactions between a given start and end date"""
        return [ta for ta in self.transactions if ta.date <= end and ta.date >= start]


    def filter_by_month(self, month: str) -> list[Transaction]:
        """
        Returns a list of transaction for a given month.
        Input format: 'YYYY-MM'
        """
        return [ta for ta in self.transactions if ta.date[:7] == month]


    def filter_by_type(self, t: TransactionType) -> list[Transaction]:
        """ Type is either Income or Expense """
        return [ta for ta in self.transactions if ta.transaction_type == t]


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

        
    def top_n_expenses(self, n: int = 5) -> list[Transaction]:
        expenses = [ta for ta in  self.transactions if ta.is_expense]
        sorted_expenses = sorted(expenses, key=lambda ta: ta.amount, reverse=True)

        return sorted_expenses[:n]


    def daily_spending(self, month: str) -> dict[str, float]:
        monthly_expenses = [ta for ta in self.filter_by_month(month) if ta.is_expense]
        daily_summary = {}

        for ta in monthly_expenses:
            day = ta.date
            daily_summary.setdefault(day, 0.0)
            daily_summary[day] += ta.amount

        return daily_summary
