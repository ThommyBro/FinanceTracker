

class FinanceError(ValueError):
    """Base class for expected validation and lookup failures."""


class InvalidTransactionError(FinanceError):
    """A transaction contains invalid input."""


class BudgetNotFoundError(FinanceError):
    """The requested budget does not exist."""


class NotFoundError(FinanceError):
    """An account or transaction no longer exists."""
