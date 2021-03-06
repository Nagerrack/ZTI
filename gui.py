import sys

from PyQt5 import QtWidgets as Qt5
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QTableWidgetItem

import highlight
from sparql_queries import get_url_by_name
from tagger import use_tagger


# test = [('a', 'Agent', 'url1', '0'),
#         ('b', 'MeanOfTransportation', 'url2', '1'),
#         ('b', 'MeanOfTransportation', 'url2', '1'),
#         ('b', 'MeanOfTransportation', 'url2', '1'),
#         ('b', 'MeanOfTransportation', 'url2', '1'),
#         ('b', 'MeanOfTransportation', 'url2', '1'),
#         ('b', 'MeanOfTransportaaaation', 'url2', '1'),
#         ('b', 'MeanOfTransportation', 'url2', '1'),
#         ('b', 'MeanOfTransportation', 'url2', '1'),
#         ('c', 'PersonFunction', 'url3', '1')]


def prepare_highlight(tagged):
    entity_dict = {entity_type: [] for _, entity_type in tagged}
    for word, current_class in tagged:
        entity_dict[current_class].append(word)

    return entity_dict


def cluster_entities(tagged):
    entities = []
    entity = ''
    prev_class = 'Other'
    for word, curr_class in tagged:
        if curr_class != 'Other':
            if entity == '':
                entity += word
            else:
                if prev_class == curr_class:
                    entity += ' ' + word
                else:
                    if entity != '':
                        entities.append(entity)
                    entity = ''
        else:
            if entity != '':
                entities.append(entity)
            entity = ''
        prev_class = curr_class

    print(entities)
    return entities


def correct_type(entity_class, url):
    return


def get_table_data(tagged, sourcetext):
    entities = []
    entity_text = ''
    entity_class = ''
    entity_url = 'URL'
    entity_begin = 0
    entity_end = 0

    prev_class = 'Other'
    for word, curr_class in tagged:
        if curr_class != 'Other':
            if entity_text == '':
                entity_text += word
                entity_class = curr_class
            else:
                if prev_class == curr_class:
                    entity_text += ' ' + word
                else:
                    if entity_text != '':
                        entity_begin = sourcetext.find(entity_text)
                        entity_end = entity_begin + len(entity_text) - 1
                        # if entity_class in ['Not_found', 'Not_on_wiki', 'Other']:
                        entity_url = get_url_by_name(entity_text)
                        # else:
                        #    entity_url = get_url_by_name_with_specified_type(entity_text, entity_class)
                        # if entity_class in ['Not_found', 'Not_on_wiki']:
                        #     if entity_url != "No data found":
                        #         entity_class = get_type_from_db_corrected(entity_url)
                        entities.append(
                            (entity_text, entity_class, str(entity_url), str(entity_begin) + "," + str(entity_end)))
                    entity_text = ''
        else:
            if entity_text != '':
                entity_begin = sourcetext.find(entity_text)
                entity_end = entity_begin + len(entity_text) - 1
                # if entity_class in ['Not_found', 'Not_on_wiki', 'Other']:
                entity_url = get_url_by_name(entity_text)
                # else:
                #    entity_url = get_url_by_name_with_specified_type(entity_text, entity_class)
                # if entity_class in ['Not_found', 'Not_on_wiki']:
                #     if entity_url != "No data found":
                #         entity_class = get_type_from_db_corrected(entity_url)
                entities.append((entity_text, entity_class, str(entity_url), str(entity_begin) + "," + str(entity_end)))
            entity_text = ''
        prev_class = curr_class

    print(entities)
    return entities


class Window(Qt5.QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 916, 600)
        self.label = Qt5.QLabel('Check me')
        self.input_text = Qt5.QTextEdit()
        self.button1 = Qt5.QPushButton('Clear')
        self.button2 = Qt5.QPushButton('Print')
        self.output_text = Qt5.QTextEdit()
        self.table = Qt5.QTableWidget()

        v_box = Qt5.QGridLayout()
        v_box.setSpacing(10)
        v_box.addWidget(self.label, 0, 0)
        v_box.addWidget(self.input_text, 1, 0)
        v_box.addWidget(self.button1, 2, 0)
        v_box.addWidget(self.button2, 3, 0)
        v_box.addWidget(self.output_text, 4, 0)
        v_box.addWidget(self.table, 0, 1, 0, 1)

        self.setLayout(v_box)
        self.setWindowTitle('Broader Named Entity Identification and Linking')
        self.table.setColumnCount(4)
        self.table.setRowCount(100)
        self.table.setHorizontalHeaderLabels(['entity', 'class', 'URL', 'index'])
        self.button1.clicked.connect(self.btn_clk)
        self.button2.clicked.connect(self.btn_clk)
        self.show()

    def fill_table(self, list_of_entities):
        for i, row in enumerate(list_of_entities):
            for j, item in enumerate(row):
                table_item = QTableWidgetItem(item)
                if j == 1:
                    table_item.setForeground(highlight.color_dict.get(item, QColor(0, 0, 0)))
                    table_item.setFont(QFont("Times", weight=QFont.Bold))
                self.table.setItem(i, j, table_item)

        self.table.resizeColumnsToContents()

    def btn_clk(self):
        sender = self.sender()

        if sender.text() == 'Print':

            sourcetext = self.input_text.toPlainText()
            print(sourcetext)
            output = use_tagger(sourcetext)
            self.highlighter = highlight.Highlighter(self.output_text.document())
            self.highlighter.define_highlighting_rules(prepare_highlight(output))

            print(prepare_highlight(output))

            myFont = QFont()
            myFont.setBold(True)
            self.label.setFont(myFont)
            self.output_text.setFont(myFont)

            self.output_text.setText(sourcetext)  # str(output)
            self.fill_table(get_table_data(output, sourcetext))

        else:
            self.input_text.clear()


app = Qt5.QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())
