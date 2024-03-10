import os.path
import sys
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from classes_ext import Ui_4bar_calculator


class TestGUI(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.ui = Ui_4bar_calculator()
        self.ui.show()

    def tearDown(self):
        QTest.qWait(100)
        self.ui.close()

    def test_1buttons(self):
        # Test button labels
        self.assertEqual(self.ui.pushButtonCalculate.text(), "calculate")
        self.assertEqual(self.ui.pushButtonPlot.text(), "plot")
        self.assertEqual(self.ui.pushButtonSave.text(), "save")

    def test_2spinBoxes(self):
        spinBoxes = ((self.ui.a, 10, "12.1"),
                     (self.ui.b, 10, "13"),
                     (self.ui.c, 15, "19.8"),
                     (self.ui.d, 18, "20.1"),
                     (self.ui.teta2start, 100, "8.5"),
                     (self.ui.teta2end, 10, "180"))
        for box, value, newValue in spinBoxes:
            self.assertEqual(box.value(), value)
            self.clearBox(box)
            QTest.keyClicks(box, newValue)
            self.assertEqual(box.value(), float(newValue))

    def test_3plainTextEdit(self):
        # Test initial plain text edit value
        self.assertEqual(self.ui.path.toPlainText(), "E:\\solution.xlsx")
        # Test changing plain text edit value
        self.clearBox(self.ui.path)
        QTest.keyClicks(self.ui.path, "D:\\new_solution.xlsx")
        self.assertEqual(self.ui.path.toPlainText(), "D:\\new_solution.xlsx")

    def test_4calculateButtonClick(self):
        QTest.mouseClick(self.ui.pushButtonCalculate, Qt.LeftButton)
        self.assertEqual(self.ui.resultsTableWidget.item(0, 5).text(), "89.0")

    def test_5saveButtonClick(self):
        QTest.mouseClick(self.ui.pushButtonSave, Qt.LeftButton)
        self.assertTrue(os.path.exists("E:\\solution.xlsx"), "File does not exist")

    def test_6plotButtonClick(self):
        QTest.mouseClick(self.ui.pushButtonCalculate, Qt.LeftButton)
        QTest.mouseClick(self.ui.pushButtonPlot, Qt.LeftButton)
        window0 = self.ui.dialogs[0]
        self.assertTrue(window0.isVisible())

    def clearBox(self, box):
        for i in range(20):
            QTest.keyClick(box, Qt.Key_Delete)


if __name__ == '__main__':
    unittest.main()
