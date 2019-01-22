from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor

Activity = ["olaf"]
Agent = ["jest"]
Award = ["spoko"]
Disease = ["wielki"]
EthnicGroup = ["test"]
Event = ["dzialania"]
Language = ["programu"]
MeanOfTransportation = ["na"]
PersonFunction = ["zajecia"]
Place = ["z"]
Species = ["panem"]
Work = ["bakiem"]

class Highlighter(QSyntaxHighlighter):


    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        keywordFormat = QTextCharFormat()

        keywordPatterns = []

        self.highlightingRules = [(QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]

        for s in Activity:
            quotationFormat = QTextCharFormat()
            quotationFormat.setForeground(QColor(1, 138, 9)) ##ciemno zielony
            self.highlightingRules.append((QRegExp('\\b' + s + '\\b'), quotationFormat))

        for s in Agent:
            quotationFormat = QTextCharFormat()
            quotationFormat.setForeground(QColor(115, 77, 38)) ##brązwoy
            self.highlightingRules.append((QRegExp('\\b' + s + '\\b'), quotationFormat))

        for s in Award:
            quotationFormat = QTextCharFormat()
            quotationFormat.setForeground(QColor(223, 97, 0)) ##pomaranczowy
            self.highlightingRules.append((QRegExp('\\b' + s + '\\b'), quotationFormat))

        for s in Disease:
            quotationFormat = QTextCharFormat()
            quotationFormat.setForeground(QColor(255, 4, 38)) ##czerwony
            self.highlightingRules.append((QRegExp('\\b' + s + '\\b'), quotationFormat))

        for s in EthnicGroup:
            quotationFormat = QTextCharFormat()
            quotationFormat.setForeground(QColor(249, 225, 0)) ##żółty
            self.highlightingRules.append((QRegExp('\\b' + s + '\\b'), quotationFormat))

        for s in Event:
            quotationFormat = QTextCharFormat()
            quotationFormat.setForeground(QColor(4, 254, 0)) ##jasno zielony
            self.highlightingRules.append((QRegExp('\\b' + s + '\\b'), quotationFormat))

        for s in Language:
            quotationFormat = QTextCharFormat()
            quotationFormat.setForeground(QColor(4, 111, 150)) ##ciemny cyan
            self.highlightingRules.append((QRegExp('\\b' + s + '\\b'), quotationFormat))

        for s in MeanOfTransportation:
            quotationFormat = QTextCharFormat()
            quotationFormat.setForeground(QColor(250, 21, 154)) ##jakis róż
            self.highlightingRules.append((QRegExp('\\b' + s + '\\b'), quotationFormat))

        for s in PersonFunction:
            quotationFormat = QTextCharFormat()
            quotationFormat.setForeground(QColor(0, 2, 254)) ##ciemny niebieski
            self.highlightingRules.append((QRegExp('\\b' + s + '\\b'), quotationFormat))

        for s in Place:
            quotationFormat = QTextCharFormat()
            quotationFormat.setForeground(QColor(128, 131, 145)) ##szary
            self.highlightingRules.append((QRegExp('\\b' + s + '\\b'), quotationFormat))

        for s in Species:
            quotationFormat = QTextCharFormat()
            quotationFormat.setForeground(QColor(251, 128, 145)) ##łososiowy
            self.highlightingRules.append((QRegExp('\\b' + s + '\\b'), quotationFormat))

        for s in Work:
            quotationFormat = QTextCharFormat()
            quotationFormat.setForeground(QColor(0, 153, 255)) ##jasny niebieski
            self.highlightingRules.append((QRegExp('\\b' + s + '\\b'), quotationFormat))

        stri = 'Bergmann'
        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(QColor(255, 255, 255))
        self.highlightingRules.append((QRegExp('\\b' + stri + '\\b'), quotationFormat))


    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)
