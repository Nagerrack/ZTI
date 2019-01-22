import sys
from PyQt5 import QtWidgets as Qt5
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QColor
import highlight



class Window(Qt5.QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(100,100,916,600)
        self.la = Qt5.QLabel('Check me')
        self.le = Qt5.QTextEdit()
        self.b1 = Qt5.QPushButton('Clear')
        self.b2 = Qt5.QPushButton('Print')
        self.tx = Qt5.QTextEdit()
        self.tb = Qt5.QTableWidget()

        v_box = Qt5.QGridLayout()
        v_box.setSpacing(10)
        v_box.addWidget(self.la, 0, 0)
        v_box.addWidget(self.le, 1, 0)
        v_box.addWidget(self.b1, 2, 0)
        v_box.addWidget(self.b2, 3, 0)
        v_box.addWidget(self.tx, 4, 0)
        v_box.addWidget(self.tb, 0, 1, 0, 1)


        self.setLayout(v_box)
        self.setWindowTitle('Broader Named Entity Identification and Linking')
        self.tb.setColumnCount(4)
        self.tb.setRowCount(100)
        self.tb.setHorizontalHeaderLabels(['entity', 'class', 'URL', 'index'])
        self.b1.clicked.connect(self.btn_clk)
        self.b2.clicked.connect(self.btn_clk)


        self.show()

    def fill_table(self, lista):
        iter = 0
        dl = len(lista)-1
        for row in range(int((dl+1)/4)):
            for col in range(4):
                if iter <= dl:
                    item = QTableWidgetItem(lista[iter])
                    if col == 1:
                        if "Activity" == lista[iter]:
                            item.setForeground(QColor(1, 138, 9))

                        if "Agent" == lista[iter]:
                            item.setForeground(QColor(115, 77, 38))

                        if "Award" == lista[iter]:
                            item.setForeground(QColor(223, 97, 0))

                        if "Disease" == lista[iter]:
                            item.setForeground(QColor(255, 4, 38))

                        if "EthnicGroup" == lista[iter]:
                            item.setForeground(QColor(249, 225, 0))

                        if "Event" == lista[iter]:
                            item.setForeground(QColor(4, 254, 0))

                        if "Language" == lista[iter]:
                            item.setForeground(QColor(4, 111, 150))

                        if "MeanOfTransportation" == lista[iter]:
                            item.setForeground(QColor(250, 21, 154))

                        if "PersonFunction" == lista[iter]:
                            item.setForeground(QColor(0, 2, 254))

                        if "Place" == lista[iter]:
                            item.setForeground(QColor(128, 131, 145))

                        if "Species" == lista[iter]:
                            item.setForeground(QColor(251, 128, 145))

                        if "Work" == lista[iter]:
                            item.setForeground(QColor(0, 153, 255))

                    self.tb.setItem(row, col, item)

                    iter = iter + 1
                else:
                    iter=0
                    self.tb.setItem(row, col, QTableWidgetItem(lista[iter]))
                    iter = iter + 1


    def btn_clk(self):
        sender = self.sender()
        lista = ["a","Activity","c","d","a","Work","c","d"]
        if sender.text() == 'Print':

            print(self.le.toPlainText())
            self.highlighter = highlight.Highlighter(self.tx.document())
            self.tx.setText(self.le.toPlainText())
            self.fill_table(lista)

        else:
            self.le.clear()




app = Qt5.QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())