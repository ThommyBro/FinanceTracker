import sqlite3
from pathlib import Path
import threading

from src.pyFinance.account import Account
from src.pyFinance.budget import Budget
from src.pyFinance.transaction import Transaction
from .financestore import FinanceStore


DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS accounts(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
account_id INTEGER NOT NULL,
description TEXT NOT NULL,
amount REAL NOT NULL,
transaction_type TEXT NOT NULL,
category TEXT NOT NULL,
date TEXT NOT NULL,
FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS transaction_tags(
transaction_id INTEGER NOT NULL,
tag TEXT NOT NULL,
PRIMARY KEY (transaction_id, tag),
FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS budgets(
id INTEGER PRIMARY KEY AUTOINCREMENT,
account_id INTEGER NOT NULL,
category TEXT NOT NULL,
monthly_limit REAL NOT NULL,
month TEXT NOT NULL,
UNIQUE(account_id, category, month),
FOREIGN KEY (account_id) REFERENCES accounts(id)
);

"""

class SQLiteStore(FinanceStore):


    # =======================================================================
    #   SQL STUFF
    # =======================================================================

    def __init__(self, path: str | Path = ":memory:"):
        self.path = str(path)
        self._lock = threading.RLock()
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript(DB_SCHEMA)
        self.conn.commit()

    def close(self) -> None:
        with self._lock:
            self.conn.close()

    def __enter__(self) -> "SQLiteStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


    # =======================================================================
    #   Implements Finance Store
    # =======================================================================
    

