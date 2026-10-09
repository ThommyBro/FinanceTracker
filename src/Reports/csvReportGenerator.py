import csv
import io

from src.pyFinance.budget_tracker import Tracker
from src.pyFinance.account import Account
from .reportGenerator import ReportGenerator

class CsvReportGenerator(ReportGenerator):

    @property
    def file_extension(self) -> str:
        return ".csv"

    def generate_monthly_report(self, account: Account, month: str) -> str:
        output = io.StringIO()
        writer = csv.writer(output)

        transactions = account.filter_by_month(month)
        summary = account.monthly_summary()[month]

        # Table Header
        writer.writerow([]) #  Empty Row
        writer.writerow(["Date", "Description", "Type", "Category", "Amount"])

        for ta in transactions:
            writer.writerow([ta.date, ta.description, ta.transaction_type.value, ta.category.value, ta.signed_amount])
        writer.writerow([])
        writer.writerow(["Summary"])
        writer.writerow(["Income", summary["Income"]])
        writer.writerow(["Expense", summary["Expense"]])
        writer.writerow(["Balance", summary["Balance"]])

        return output.getvalue()


    def generate_category_report(self, account: Account) -> str:
        output = io.StringIO()
        writer = csv.writer(output)

        categories = account.category_breakdown()

        # Table Header
        writer.writerow(["Category", "Amount"])

        for category, amount in categories.items():
            writer.writerow([category.value, amount])

        return output.getvalue()


    def generate_budget_report(self, tracker: Tracker, account: Account) -> str:
        output = io.StringIO()
        writer = csv.writer(output)

        budget_status = tracker.check_budgets(account)

        # Table Header
        writer.writerow(["Category", "Month", "Limit", "Used %", "Remaining"])
        for budget, percentage in budget_status:
            writer.writerow([
                            budget.category.value,
                            budget.month,
                            budget.monthly_limit,
                            percentage,
                            budget.remaining(account)
                            ])
            
        return output.getvalue()


        
