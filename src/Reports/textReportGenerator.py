

from .reportGenerator import ReportGenerator
from src.pyFinance.account import Account 
from src.pyFinance.budget_tracker import Tracker
from src.pyFinance.category import Category
from src.pyFinance.budget import Budget

class TextReportGenerator(ReportGenerator):

    @property
    def file_extension(self) -> str:
        return ".txt"

    def generate_monthly_report(self, account: Account, month: str) -> str:
        """
        Uses Account functionality monthly_summary and filter_by_month.
        Returns only formated Data
        """
        # Header
        lines = [
                f"Monthly Report - {month}",
                "=" * 30,
                "",
                f"Account: {account.name}",
                "",
                "Transactions:"
            ]
        
        summary = account.monthly_summary()[month]
        transactions = account.filter_by_month(month)
        for ta in transactions:
            lines.append(str(ta))

        lines.extend([
                        "",
                        f"Income: {summary['Income']}",
                        f"Expense: {summary['Expense']}",
                        f"Balance: {summary['Balance']}",
                    ])

        return "\n".join(lines)


    def generate_category_report(self, account: Account) -> str:
        """
        Uses Account functionality category_breakdown.
        Returns only formated Data
        """
        # Header
        lines = [
                    f"Category Report",
                    "=" * 30,
                    "",
                    f"Account: {account.name}",
                    "",
                    "Categories:"
                ]
        categories = account.category_breakdown()
        for category, amount in categories.items():
            lines.append(f"{category.value}: {amount:.2f}")

        return "\n".join(lines)


    def generate_budget_report(self, tracker: Tracker, account: Account) -> str:
        # Header
        lines = [
                    f"Budget Report",
                    "=" * 30,
                    "",
                    f"Account: {account.name}",
                    "",
                ]

        budget_status = tracker.check_budgets(account)

        for budget, percentage in budget_status:
            lines.append(f"{budget.category.value} - {budget.month}")
            lines.append(f"Limit: {budget.monthly_limit:.2f}%")
            lines.append(f"Used: {percentage:.1f}")
            lines.append(f"Remaining: {budget.remaining(account):.2f}")
            lines.append("")

        return "\n".join(lines)