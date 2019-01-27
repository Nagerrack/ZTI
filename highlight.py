from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor

from configuration_data import types

colors = [QColor(1, 138, 9),
          QColor(115, 77, 38),
          QColor(223, 97, 0),
          QColor(255, 4, 38),
          QColor(249, 225, 0),
          QColor(4, 254, 0),
          QColor(4, 111, 150),
          QColor(250, 21, 154),
          QColor(0, 2, 254),
          QColor(128, 131, 145),
          QColor(251, 128, 145),
          QColor(0, 153, 255)
          ]

color_dict = dict(zip(types, colors))


# entity_dict = {entity_type: [] for entity_type in types}


# entity_dict['Event'].extend('Battle of Kursk'.split())
# entity_dict['Species'].extend('Cheetah Cat Dog'.split())


class Highlighter(QSyntaxHighlighter):

    def __init__(self, parent=None, ):
        super(Highlighter, self).__init__(parent)

        keyword_format = QTextCharFormat()

        keyword_patterns = []

        self.highlightingRules = [(QRegExp(pattern), keyword_format)
                                  for pattern in keyword_patterns]

    def define_highlighting_rules(self, entity_dict):
        for entity_type in entity_dict:
            for item in entity_dict[entity_type]:
                quotation_format = QTextCharFormat()
                quotation_format.setForeground(color_dict.get(entity_type, QColor(0, 0, 0)))
                self.highlightingRules.append((QRegExp('\\b' + item + '\\b'), quotation_format))

    def highlightBlock(self, text):
        for pattern, text_format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, text_format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)
