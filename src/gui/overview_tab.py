from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QComboBox
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import seaborn as sns


class OverviewTab(QWidget):

    def __init__(self, store):
        super().__init__()

        self.store = store
        self.current_account_name: str | None = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("Overview")
        layout.addWidget(title)

        self.month_box = QComboBox()
        layout.addWidget(self.month_box)
        self.month_box.currentTextChanged.connect(self.update_chart)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.canvas)



    

    def set_account(self, account_name: str) -> None:
        self.refresh(account_name)
       


    def update_chart(self, month: str | None = None) -> None:
        if self.current_account_name is None: return

        month = self.month_box.currentText()

        if not month: return

        account = self.store.get_account(self.current_account_name)
        breakdown = account.category_breakdown(month, expenses_only =True)
        
        sorted_data = sorted(breakdown.items(), key=lambda item: abs(item[1]), reverse=True)
        categories = [category.value for category, _ in sorted_data]
        amounts = [abs(amount) for _,amount in sorted_data]


        self.figure.clear()
        ax = self.figure.add_subplot(111)

        
        self.figure.set_facecolor("#ffffff")
        ax.set_facecolor("#ffffff")

        # color highest value darker
        colors = [ "#2563eb" if i == 0 else "#93c5fd" for i in range(len(categories))]

        sns.barplot(
            x=amounts,
            y=categories,
            hue=categories,
            palette=colors,
            legend=False,
            ax=ax,
            width=0.62
        )

        # Label values at the bars
        for container in ax.containers:
            ax.bar_label(container, fmt="%.2f €", padding=6, fontsize=10, color="#475569")

        ax.set_title(f"Expenses by category - {month}", loc="left", fontsize=16, fontweight="bold", color="#0f172a", pad=18)
        ax.text(0, 1.01, month, transform=ax.transAxes, fontsize=10, color="#64748b")

        ax.set_xlabel("")
        ax.set_ylabel("")

        ax.tick_params(
            axis="y",
            labelsize=10,
            colors="#334155",
            length=0
        )

        ax.tick_params(
            axis="x",
            labelsize=10,
            colors="#94a3b8",
            length=0
        )

        ax.grid(axis="x", linestyle="--", alpha=0.15)
        ax.grid(axis="y", visible=False)

        sns.despine(ax=ax, left=True, bottom=True)

        # leafs a little space at the right border
        if amounts:
            ax.set_xlim(0, max(amounts) * 1.18)

        self.figure.tight_layout(pad=2)
        self.canvas.draw_idle()
        


    def refresh(self, account_name: str | None = None) -> None:
        if account_name is not None:
            self.current_account_name = account_name

        if self.current_account_name is None: return

        transactions = self.store.get_transactions(self.current_account_name)
        current_month = self.month_box.currentText()

        months = sorted({ta.date[:7] for ta in transactions})

        self.month_box.blockSignals(True)

        self.month_box.clear()
        self.month_box.addItems(months)

        if current_month in months:
            self.month_box.setCurrentText(current_month)
        elif months:
            self.month_box.setCurrentIndex(0)

        self.month_box.blockSignals(False)

        print("months:", months)
        print("selected:", self.month_box.currentText())
        self.update_chart()