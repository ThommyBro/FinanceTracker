from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
)

from src.pyFinance.account import Account


class ImportExportTab(QWidget):

    transactions_imported = Signal(str)

    def __init__(self, store):
        super().__init__()

        self.store = store
        self.current_account_name: str | None = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("Import / Export")
        layout.addWidget(title)

        self.import_button = QPushButton(
            "Import Transactions from CSV"
        )
        layout.addWidget(self.import_button)

        self.status_label = QLabel("No file imported.")
        layout.addWidget(self.status_label)

        layout.addStretch()

        self.import_button.clicked.connect(self.import_csv)



    def set_account(self, account_name: str) -> None:
        self.current_account_name = account_name



    def import_csv(self) -> None:
        if self.current_account_name is None:
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Transactions",
            "",
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try: 
            imported_account = Account.load_from_csv(file_path, self.current_account_name)

            for transaction in imported_account.transactions:
                self.store.add_transaction(
                    self.current_account_name,
                    transaction
                )

            count = len(imported_account.transactions)

            self.status_label.setText(f"Imported {count} transactions.")
            self.transactions_imported.emit(self.current_account_name)

        except Exception as exc:
            QMessageBox.critical(
                self,
                "Import Error",
                str(exc)
            )