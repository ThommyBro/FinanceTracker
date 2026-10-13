APP_STYLE = """
QMainWindow {
    background-color: #f1f5f9;
}

QWidget {
    background-color: #f1f5f9;
    color: #0f172a;
    font-size: 14px;
}

/* ---------- Labels ---------- */

QLabel {
    color: #0f172a;
}


/* ---------- Buttons ---------- */

QPushButton {
    background-color: #ffffff;
    color: #0f172a;

    border: 1px solid #cbd5e1;
    border-radius: 8px;

    padding: 7px 14px;
}

QPushButton:hover {
    background-color: #e2e8f0;
}

QPushButton:pressed {
    background-color: #cbd5e1;
}

QPushButton:disabled {
    background-color: #f8fafc;
    color: #94a3b8;
    border-color: #e2e8f0;
}


/* ---------- Primary Button ---------- */

QPushButton#primaryButton {
    background-color: #2563eb;
    color: white;
    border: none;
    font-weight: bold;
}

QPushButton#primaryButton:hover {
    background-color: #3b82f6;
}


/* ---------- Delete Button ---------- */

QPushButton#dangerButton {
    background-color: #dc2626;
    color: white;
    border: none;
}

QPushButton#dangerButton:hover {
    background-color: #ef4444;
}


/* ---------- Inputs ---------- */

QComboBox,
QLineEdit,
QDateEdit,
QDoubleSpinBox {
    background-color: #ffffff;
    color: #0f172a;

    border: 1px solid #cbd5e1;
    border-radius: 7px;

    padding: 6px 10px;
}

QComboBox:hover,
QLineEdit:hover,
QDateEdit:hover,
QDoubleSpinBox:hover {
    border: 1px solid #94a3b8;
}

QComboBox:focus,
QLineEdit:focus,
QDateEdit:focus,
QDoubleSpinBox:focus {
    border: 1px solid #2563eb;
}


/* ---------- Tabs ---------- */

QTabWidget::pane {
    border: 1px solid #dbe4ee;
    border-radius: 8px;
    background-color: #ffffff;
}

QTabBar::tab {
    background-color: #e2e8f0;
    color: #475569;

    padding: 10px 18px;

    border-top-left-radius: 7px;
    border-top-right-radius: 7px;

    margin-right: 3px;
}

QTabBar::tab:selected {
    background-color: #2563eb;
    color: white;
}

QTabBar::tab:hover:!selected {
    background-color: #cbd5e1;
}


/* ---------- Tables ---------- */

QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f8fafc;

    border: 1px solid #dbe4ee;
    border-radius: 8px;

    gridline-color: #e2e8f0;

    selection-background-color: #bfdbfe;
    selection-color: #0f172a;
}

QTableWidget::item {
    padding: 6px;
}

QHeaderView::section {
    background-color: #f8fafc;
    color: #0f172a;

    border: none;
    border-bottom: 1px solid #dbe4ee;

    padding: 8px;

    font-weight: bold;
}


/* ---------- KPI Cards ---------- */

QFrame#kpiCard {
    background-color: #ffffff;

    border: 1px solid #dbe4ee;
    border-radius: 12px;

    padding: 10px;
}

QLabel#kpiTitle {
    background-color: transparent;
    color: #64748b;

    font-size: 12px;
    font-weight: bold;
}

QLabel#kpiValue {
    background-color: transparent;
    color: #0f172a;;
    
    font-size: 24px;
    font-weight: bold;
}
"""