from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QFontDatabase


def apply_style(app: QApplication):
    app.setStyle("Fusion")
    app.setFont(QFont("JetBrainsMonoNLNerdFontPropo", 10))

    font_id = QFontDatabase.addApplicationFont("fonts/JetBrainsMonoNLNerdFontPropo-Regular.ttf")
    if font_id != -1:
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(family))

    app.setStyleSheet("""
    * { font-family: 'JetBrainsMonoNLNerdFontPropo', sans-serif; }

    QMainWindow { background-color: #f5f6f9; }

    /* Cards & Containers */
    QFrame#sidebar {
        background-color: #ffffff;
        border-right: 1px solid #e5e7e9;
    }
    QFrame#card {
        background-color: #ffffff;
        border-radius: 12px;
        border: 1px solid #e5e7e9;
    }

    /* Sidebar Menus */
    QPushButton#menuBtn {
        text-align: left;
        padding: 12px 16px;
        background: transparent;
        color: #6d7588;
        border: none;
        font-size: 14px;
        font-weight: 600;
        border-radius: 8px;
    }
    QPushButton#menuBtn:hover {
        background-color: #f3f4f5;
        color: #31353b;
    }
    QPushButton#menuBtnActive {
        text-align: left;
        padding: 12px 16px;
        background-color: #eaf7eb;
        color: #42b549;
        border: none;
        font-size: 14px;
        font-weight: bold;
        border-radius: 8px;
    }

    /* Inputs */
    QLineEdit {
        background-color: #ffffff;
        border: 1px solid #e5e7e9;
        border-radius: 8px;
        padding: 10px 14px;
        color: #31353b;
        font-size: 13px;
    }
    QLineEdit:focus { border: 1px solid #42b549; }

    QLineEdit#searchBar {
        border-radius: 20px;
        background-color: #ffffff;
    }

    /* Buttons */
    QPushButton {
        border-radius: 8px;
        padding: 10px 18px;
        font-size: 13px;
        font-weight: bold;
    }
    QPushButton#btnPrimary {
        background-color: #42b549;
        color: white;
        border: none;
    }
    QPushButton#btnPrimary:hover { background-color: #35943b; }
    QPushButton#btnPrimary:disabled { background-color: #a8d5ab; }

    QPushButton#btnSecondary {
        background-color: #ffffff;
        color: #31353b;
        border: 1px solid #d6dce5;
    }
    QPushButton#btnSecondary:hover { background-color: #f3f4f5; }

    QPushButton#btnDanger {
        background-color: #ffffff;
        color: #ef144a;
        border: 1px solid #ef144a;
    }
    QPushButton#btnDanger:hover { background-color: #ffeaef; }

    QPushButton#btnImport {
        background-color: #1e88e5;
        color: white;
        border: none;
    }
    QPushButton#btnImport:hover { background-color: #1565c0; }

    /* Table System */
    QTableWidget {
        background-color: transparent;
        border: none;
        color: #31353b;
        outline: none;
    }
    QTableWidget::item {
        border-bottom: 1px solid #f0f0f0;
        padding: 5px;
        color: #31353b;
    }
    QTableWidget::item:selected {
        background-color: #eaf7eb;
        color: #42b549;
    }
    QHeaderView::section {
        background-color: #f8f9fa;
        color: #6d7588;
        padding: 14px 10px;
        font-weight: 700;
        border: none;
        border-bottom: 1px solid #e5e7e9;
        font-size: 13px;
        text-align: left;
    }

    /* Message Box */
    QMessageBox { background-color: white; }
    QMessageBox QLabel { color: #31353b; font-size: 13px; }
    QMessageBox QPushButton { min-width: 80px; background-color: #42b549; color: white; border: none; }
    QMessageBox QPushButton:hover { background-color: #35943b; }

    /* Scrollbars */
    QScrollBar:vertical {
        border: none;
        background: transparent;
        width: 8px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #d6dce5;
        border-radius: 4px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover { background: #b0b8c3; }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
    """)
