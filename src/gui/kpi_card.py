from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class KpiCard(QFrame):

    def __init__(self, title: str, value: str = "0.00 €"):
        super().__init__()

        self.setObjectName("kpiCard")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("kpiTitle")

        self.value_label = QLabel(value)
        self.value_label.setObjectName("kpiValue")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)


    def set_value(self, value: str) -> None:
        self.value_label.setText(value)