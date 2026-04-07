import sys

from PyQt5.QtWidgets import QApplication

from styles import apply_style
from ui_main import POSApp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_style(app)

    win = POSApp()
    win.show()

    sys.exit(app.exec_())
