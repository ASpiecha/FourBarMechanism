import classes_ext as window
import sys
from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = window.Ui_4bar_calculator()
    ui.show()
    sys.exit(app.exec_())
