


from .financestore import FinanceStore
from src.pyFinance.exceptions import NotFoundError, FinanceError
from src.pyFinance.account import Account
from src.pyFinance.budget_tracker import Tracker
from src.pyFinance.transaction import Transaction
from src.pyFinance.budget import Budget
from src.pyFinance.transaction_type import TransactionType
from src.pyFinance.category import Category



class InMemoryStore(FinanceStore):
    def __init__(self) -> None:
        self.accounts: dict[str, Account] = {}
        self.trackers: dict[str, Tracker] = {}
        self._next_transaction_id = 1


    def _account(self, name: str) -> Account:
        try:
            return self.accounts[name]
        except KeyError as exc:
            raise NotFoundError("Account not found.") from exc


    def _transaction(self, account_name: str, transaction_id: int) -> Transaction:
        account = self._account(account_name)

        for ta in account.transactions:
            if ta.id == transaction_id:
                return ta

        raise NotFoundError(f"Transaction with ID {transaction_id} not found.")
      

    def _tracker(self, name: str) -> Tracker:
        try:
            return self.trackers[name]
        except KeyError as exc:
            raise NotFoundError("Budget tracker not found.") from exc


    # ========================================================
    # Account actions
    # ========================================================

    def create_account(self, name: str) -> None:
        if name in self.accounts:
            raise FinanceError("An account with that name already exists.")
        self.accounts[name] = Account(name)
        self.trackers[name] = Tracker()


    def list_accounts(self) -> list[str]:
        return sorted(self.accounts)


    def delete_account(self, name: str) -> None:
        self._account(name)
        del self.accounts[name]
        del self.trackers[name]

    # ========================================================
    # Transactions
    # ========================================================

    def add_transaction(self, account_name: str, transaction: Transaction) -> None:
        account = self._account(account_name)
        transaction.id = self._next_transaction_id
        self._next_transaction_id += 1
        account.add_transaction(transaction)        


    def update_transaction(self, account_name: str, transaction_id: int, description: str, amount: float, transaction_type: TransactionType, category: Category, date: str, tags: set[str]) -> None:
        transaction = self._transaction(account_name, transaction_id)

        # use udpate method from transaction so new values get validated
        transaction.update(description, amount, transaction_type, category, date, tags)


    def get_transactions(self, account_name: str) -> list[Transaction]:
        account = self._account(account_name)
        # return a copy via list
        return list(account.transactions)


    # ========================================================
    # Budgets
    # ========================================================

    def set_budget(self, account_name: str, budget: Budget) -> None:
        tracker = self._tracker(account_name)
        tracker.set_budget(budget.category, budget.monthly_limit, budget.month)


    def get_budgets(self, account_name: str) -> list[Budget]:
        tracker = self._tracker(account_name)
        return list(tracker.budgets)


    def delete_budget(self, account_name: str, category: Category, month: str) -> None:
        budgets = self._tracker(account_name).budgets

        for budget in budgets:
            if category == budget.category and month == budget.month:
                budgets.remove(budget)
                return
        raise NotFoundError("Budget ot found.")        



    