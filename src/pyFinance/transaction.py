import re

from dataclasses import dataclass, field
from .transaction_type import TransactionType
from .category import Category



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


    def __post_init__(self):
        if not self.description.strip():
            raise ValueError("Description must not be empty")
        if self.amount <= 0:
            raise ValueError(f"Amount must be positive. You typed '{self.amount}'.")
        if not DATE_PATTERN.match(self.date):
            raise ValueError(f"Date must be in format 'YYYY-MM-DD', but got '{self.date}'.")


    def __str__(self):
        return f"{self.date} '{self.description}': {self.signed_amount} [{self.category.name}]"
    


    @property
    def is_expense(self) -> bool:
        return self.transaction_type == TransactionType.EXPENSE

    @property
    def is_income(self) -> bool:
        return self.transaction_type == TransactionType.INCOME

    @property
    def signed_amount(self) -> float:
        return -self.amount if self.is_expense else self.amount




