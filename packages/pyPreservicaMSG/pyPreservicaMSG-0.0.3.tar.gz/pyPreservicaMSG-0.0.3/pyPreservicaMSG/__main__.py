import sys

from pyPreservicaMSG.gui import MyWidget
from PySide2.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.setFixedSize(800, 600)
    widget.show()

    sys.exit(app.exec_())
