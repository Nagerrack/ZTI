import sys
from PyQt5 import QtWidgets as Qt5
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
    def btn_clk(self):
        sender = self.sender()
        if sender.text() == 'Print':

            print(self.le.toPlainText())
            self.highlighter = highlight.Highlighter(self.tx.document())
            self.tx.setText(self.le.toPlainText())
        else:
            self.le.clear()

app = Qt5.QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())