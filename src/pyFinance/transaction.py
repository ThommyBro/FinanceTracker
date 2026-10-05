import re

from dataclasses import dataclass, field
from .transaction_type import TransactionType
from .category import Category
from .exceptions import (InvalidTransactionError, FinanceError)



DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class Transaction:
    """
    - Description: str
    - Amount: float
    - Transaction Type: Transaction_Type
    - Category: Category
    - date: str
    - tags: set
    """
    
    description: str
    amount: float
    transaction_type: TransactionType
    category: Category
    date: str
    tags: set[str] = field(default_factory=set) 
    id: int | None = field(default=None)


    def __post_init__(self):
        """See static Method _validate(self)"""
        self._validate(self.description, self.amount, self.date)


    def __str__(self):
        return f"{self.date} '{self.description}': {self.signed_amount} [{self.category.name}]"


    @staticmethod
    def _validate(description: str, amount: float, date: str) -> None:
        """
        Use this, so updates for transactions can also be checked with this method.
        """
        if not description.strip():
            raise ValueError("Description must not be empty")
        if amount <= 0:
            raise ValueError(f"Amount must be positive. You typed '{amount}'.")
        if not DATE_PATTERN.match(date):
            raise ValueError(f"Date must be in format 'YYYY-MM-DD', but got '{date}'.")
    


    @property
    def is_expense(self) -> bool:
        return self.transaction_type == TransactionType.EXPENSE

    @property
    def is_income(self) -> bool:
        return self.transaction_type == TransactionType.INCOME

    @property
    def signed_amount(self) -> float:
        return -self.amount if self.is_expense else self.amount

    
    def update(self, description: str, amount: float, transaction_type: TransactionType, category: Category, date: str, tags: set[str]) -> None:
        # validate values before storage
        self._validate(description, amount, date)

        # after validation set new values
        self.description = description
        self.amount = amount
        self.transaction_type = transaction_type
        self.category = category
        self.date = date
        self.tags = set(tags)






    # ========================================
    # Dictionary Import
    # ========================================

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """Needs to be so explicit because the tags structure is a list in export but needs to be a set for imports."""
        try:
            return cls(
                description=data["description"],
                amount=data["amount"],
                transaction_type=TransactionType(data["transaction_type"]),
                category=Category(data["category"]),
                date=data["date"],
                tags=set(data.get("tags", [])),
            )

        except (KeyError, TypeError, ValueError) as exc:
            raise InvalidTransactionError(
                f"Invalid transaction object: {exc}"
            ) from exc

    # ========================================
    # Dictionary Export
    # ========================================

    @property
    def to_dict(self) -> dict:
        """sorted(self.tags) hilft bei der JSON Serialisierung. Allg. können von json.dump keine sets genutzt werden."""
        return {
            "description": self.description, "amount": self.amount, "transaction_type": self.transaction_type.value,
            "category": self.category.value, "date": self.date, "tags": sorted(self.tags)
        }




