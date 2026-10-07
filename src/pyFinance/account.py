import re
import json
import csv
from pathlib import Path

from dataclasses import dataclass, field
from .transaction_type import TransactionType
from .category import Category
from .transaction import Transaction
from .exceptions import (FinanceError, InvalidTransactionError, BudgetNotFoundError, NotFoundError)




@dataclass
class Account:

    name: str
    transactions: list[Transaction] = field(default_factory=list) 

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Account name must not be empty.")
    

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
        month_summary = {}
        
        for ta in self.transactions:
            month = ta.date[:7]      # takes year and month

            month_summary.setdefault(
                month, {
                    "Income": 0.0,
                    "Expense": 0.0,
                    "Balance": 0.0
                }
            )

            if ta.is_income:
                month_summary[month]["Income"] += ta.amount

            elif ta.is_expense:
                month_summary[month]["Expense"] += ta.amount

            month_summary[month]["Balance"] += ta.signed_amount
            
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


    # ========================================
    # Dictionary Import
    # ========================================

    @classmethod
    def from_dict(cls,data: dict) -> "Account":
        try:
            return cls(data["name"], [Transaction.from_dict(t) for t in data["transactions"]])
        except (KeyError, TypeError) as exc:
            raise FinanceError("Invalid account JSON structure.") from exc


    # ========================================
    # Dictionary Export
    # ========================================

    @property
    def to_dict(self) -> dict:
        return {
            "name": self.name, "transactions": [t.to_dict for t in self.transactions]
        }


    # ========================================
    # JSON Export
    # ========================================

    def save_as_json(self, filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.to_dict, f, indent=4)


    # ========================================
    # JSON Import
    # ========================================
    
    @classmethod
    def load_account(cls, file: str) -> "Account":
        try:
            with Path(file).open("r", encoding="utf-8") as f:
                data = json.load(f)
            return cls.from_dict(data)

        except (ValueError, TypeError) as exc:
            raise FinanceError(f"Cannot load JSON: {exc}") from exc
  


