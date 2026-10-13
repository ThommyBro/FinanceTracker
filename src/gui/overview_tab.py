from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
from datetime import datetime

import seaborn as sns

from .chart_card import ChartCard


class OverviewTab(QWidget):

    def __init__(self, store):
        super().__init__()

        self.store = store
        self.current_account_name: str | None = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("")
        layout.addWidget(title)

        # Box for charts
        self.month_box = QComboBox()
        self.month_box.setMinimumWidth(130)
        # Expenses
        self.figure = Figure(facecolor="#ffffff")
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(350)
        self.expense_chart_card = ChartCard(title="Expenses by Category", content=self.canvas, control=self.month_box,)
        
        # Trends
        self.trend_figure = Figure(facecolor="#ffffff")
        self.trend_canvas = FigureCanvas(self.trend_figure)
        self.trend_canvas.setMinimumHeight(350)
        self.trend_chart_card = ChartCard(title="Income vs. Expenses", content=self.trend_canvas, )

        # Add Charts combined
        charts_layout = QHBoxLayout()
        charts_layout.addWidget(self.expense_chart_card,1)
        charts_layout.addWidget(self.trend_chart_card,1)
        layout.addLayout(charts_layout)


        # Updates for Expense Chart
        self.month_box.currentTextChanged.connect(self.update_chart)



    

    def set_account(self, account_name: str) -> None:
        self.refresh(account_name)
       


    def update_chart(self, month: str | None = None) -> None:
        if self.current_account_name is None: return

        month = self.month_box.currentText()

        if not month: return

        account = self.store.get_account(self.current_account_name)
        breakdown = account.category_breakdown(month, expenses_only =True)

        # Emty Chart if no data is available
        if not breakdown:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.set_facecolor("#ffffff")
            ax.text(0.5, 0.5,
                "No expense data available",
                ha="center",
                va="center",
                fontsize=13,
                color="#64748b",
                transform=ax.transAxes,
            )

            ax.axis("off")
            self.canvas.draw_idle()
            return
        
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


    def update_trend_chart(self) -> None:
        if self.current_account_name is None: return

        account = self.store.get_account(self.current_account_name)
        summary = account.monthly_summary()

        # Empty Chart if no data is available
        if not summary:
            self.trend_figure.clear()
            ax = self.trend_figure.add_subplot(111)
            ax.set_facecolor("#ffffff")
            ax.text(
                0.5,
                0.5,
                "No transaction data available",
                ha="center",
                va="center",
                fontsize=13,
                color="#64748b",
                transform=ax.transAxes,
            )

            ax.axis("off")
            self.trend_canvas.draw_idle()
            return
        
        months = sorted(summary.keys())
        month_labels = [
            datetime.strptime(month, "%Y-%m").strftime("%b %y")
            for month in months
        ]

        incomes = [summary[month]["Income"] for month in months]
        expenses = [summary[month]["Expense"] for month in months]

        self.trend_figure.clear()
        ax = self.trend_figure.add_subplot(111)
        ax.set_facecolor("#ffffff")

        sns.lineplot(
            x=month_labels,
            y=incomes,
            marker="o",
            linewidth=2.5,
            label="Income",
            color="#2563eb",
            ax=ax,
        )

        sns.lineplot(
            x=month_labels,
            y=expenses,
            marker="o",
            linewidth=2.5,
            label="Expenses",
            color="#ef4444",
            ax=ax,
        )

        ax.set_xlabel("")
        ax.set_ylabel("",loc="top")
        ax.tick_params(axis="x", colors="#64748b", rotation=45,)
        ax.tick_params(axis="y", colors="#64748b",)

        ax.grid(axis="y", linestyle="--", alpha=0.15,)
        ax.grid(axis="x", visible=False,)
        sns.despine(ax=ax,left=True, bottom=True,)
        ax.legend(frameon=False,)

        def euro_formatter(value, _):
            return f"{value:,.0f} €"

        ax.yaxis.set_major_formatter(
            FuncFormatter(euro_formatter)
        )
        self.trend_figure.tight_layout(pad=1.5)

        self.trend_canvas.draw_idle()
        


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

        self.update_chart()
        self.update_trend_chart()