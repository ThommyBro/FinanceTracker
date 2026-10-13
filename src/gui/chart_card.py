from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)


class ChartCard(QFrame):

    def __init__(
        self,
        title: str,
        content: QWidget,
        control: QWidget | None = None,
    ):
        super().__init__()

        self.setObjectName("chartCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        # Header
        header_layout = QHBoxLayout()

        title_label = QLabel(title)
        title_label.setObjectName("chartCardTitle")

        header_layout.addWidget(title_label)
        header_layout.addStretch()

        if control is not None:
            header_layout.addWidget(control)

        layout.addLayout(header_layout)

        # eigentlicher Inhalt, z.B. Matplotlib Canvas
        layout.addWidget(content)