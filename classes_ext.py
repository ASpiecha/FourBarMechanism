from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDoubleSpinBox, QLabel, QMessageBox

from functions_ext import optimizer, saveListToExcel

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Ui_4bar_calculator(QtWidgets.QMainWindow):
    configuration = []
    chartOmega = []
    chartEpsilon = []
    solutionToPlot1 = 1

    def __init__(self):
        super().__init__()
        self.setWindowTitle("4 bar mechanism calculator")
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.setupUi()

    def setupUi(self):
        self.headerNames = ['a', 'b', 'c', 'd', 'angleOfA', 'angleOfB']
        xLabel = 10
        xBox = 130
        xStep = 60
        y = 190
        yStep = 40
        self.setObjectName("4bar_calculator")
        self.resize(400, 580)
        self.centralwidget.setObjectName("centralwidget")
        self.photo = QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(61, 0, 277, 158))
        self.photo.setText("")
        self.photo.setPixmap(QPixmap("4bar2.png"))
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")

        self.pushButtonCalculate = self.createPushButton("calculate", self.calculate, xLabel, y+yStep*7)
        self.pushButtonPlot = self.createPushButton("plot", self.plotClicked, xLabel+xStep*4, y+yStep*7)
        self.pushButtonSave = self.createPushButton("save", self.saveToExcel, xLabel+xStep*2, y+yStep*7)

        self.a = self.createSpinBox("a", xBox, y, 10.0)
        self.b = self.createSpinBox("b", xBox, y+yStep, 10.0)
        self.c = self.createSpinBox("c", xBox, y+yStep*2, 15.0)
        self.d = self.createSpinBox("d", xBox, y+yStep*3, 18.0)

        self.teta2start = self.createSpinBox("teta2start", xBox, y+yStep*4, 100.0, -180.0, 180.0)

        self.teta2end = self.createSpinBox("teta2end", xBox, y+yStep*5, 10.0, -180.0, 180.0)

        self.path = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.path.setGeometry(QtCore.QRect(xBox, y+yStep*6, 260, 31))
        self.path.setObjectName("path")
        self.path.setPlainText("E:\\solution.xlsx")

        self.label_a = self.createLabel("a [cm]", xLabel, y)
        self.label_b = self.createLabel("b [cm]", xLabel, y+yStep)
        self.label_c = self.createLabel("c [cm]", xLabel, y+yStep*2)
        self.label_d = self.createLabel("d [cm]", xLabel, y+yStep*3)
        self.label_teta2start = self.createLabel("teta2start [deg]", xLabel, y+yStep*4)
        self.label_teta2end = self.createLabel("teta2end [deg]", xLabel, y+yStep*5)
        self.label_path = self.createLabel("path", xLabel, y+yStep*6)

        self.resultsTableWidget = self.createTableWidget(xLabel, y, yStep)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 945, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.dialogs = list()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setTabOrdering()

    def createPushButton(self, text, func, x, y):
        pushButton = QtWidgets.QPushButton(text, self.centralwidget)
        pushButton.setGeometry(QtCore.QRect(x, y, 100, 31))
        pushButton.clicked.connect(func)
        return pushButton

    def createLabel(self, text, x, y):
        label = QLabel(text, self.centralwidget)
        label.setGeometry(QtCore.QRect(x, y, 90, 20))
        label.setObjectName("label_" + text.replace(" ", ""))
        return label

    def createSpinBox(self, name, x, y, value, minimum=0.0, maximum=100.0):
        spinBox = QDoubleSpinBox(self.centralwidget)
        spinBox.setGeometry(QtCore.QRect(x, y, 100, 31))
        spinBox.setProperty("minimum", minimum)
        spinBox.setProperty("maximum", maximum)
        spinBox.setProperty("value", value)
        spinBox.setObjectName(name)
        return spinBox

    def createTableWidget(self, x, y, yStep):
        tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        tableWidget.setGeometry(QtCore.QRect(x, y+yStep*8, 380, 50))
        tableWidget.setObjectName("resultsListWidget")
        tableWidget.setRowCount(1)
        tableWidget.setColumnCount(6)
        for i in range(6):
            tableWidget.setColumnWidth(i, 60)
        tableWidget.setRowHeight(0, 20)
        tableWidget.setHorizontalHeaderLabels(self.headerNames)
        return tableWidget

    def setTabOrdering(self):
        order = [self.a, self.b, self.c, self.d, self.teta2start, self.teta2end, self.path]
        for i in (range(len(order) - 1)):
            self.setTabOrder(order[i], order[i+1])

    def calculate(self):
        a = self.a.value()
        b = self.b.value()
        c = self.c.value()
        d = self.d.value()
        teta2Start = self.teta2start.value()
        teta2End = self.teta2end.value()
        self.configuration, Ui_4bar_calculator.chartOmega, Ui_4bar_calculator.chartEpsilon \
            = optimizer(a, b, c, d, teta2Start, teta2End)
        if not self.configuration:
            QMessageBox.warning(self.centralwidget, "Error", "Unable to perform calculations")
        self.resultsTableWidget.clearContents()
        for i, item in enumerate(self.configuration):
            self.resultsTableWidget.setItem(0, i, QtWidgets.QTableWidgetItem(str(item)))

    def saveToExcel(self):
        path1 = self.path.toPlainText()
        if path1[-5:] != '.xlsx':
            path1 = path1 + '.xlsx'
        saveListToExcel(self.configuration, self.headerNames, path1)

    def plotClicked(self):
        dialog = PlotWindow()
        self.dialogs.append(dialog)
        dialog.show()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=7, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        super().__init__(fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        ax1 = self.figure.add_subplot(211)
        ax1.plot(Ui_4bar_calculator.chartOmega, 'r-')
        ax1.set_title('Relative angular velocity of b to a')
        ax2 = self.figure.add_subplot(212)
        ax2.plot(Ui_4bar_calculator.chartEpsilon, 'b-')
        ax2.set_title('Relative angular acceleration of b to a')
        ax1.grid()
        ax2.grid()
        self.draw()


class PlotWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 700)
        PlotCanvas(self)

