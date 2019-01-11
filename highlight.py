from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat


class Highlighter(QSyntaxHighlighter):

    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        keywordFormat = QTextCharFormat()

        keywordPatterns = []

        self.highlightingRules = [(QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]

        stri = 'Olaf'
        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(Qt.darkGreen)
        self.highlightingRules.append((QRegExp('\\b' + stri + '\\b'), quotationFormat))

        stri = 'Bergmann'
        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(Qt.darkRed)
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
