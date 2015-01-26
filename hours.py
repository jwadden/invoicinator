import models

import settings

from PyQt5.QtWidgets import *
 
class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        
        dateLabel = QLabel("Date")
        self.dateLine = QCalendarWidget()
        caseLabel = QLabel("Case:")
        self.caseLine = QLineEdit()
        startLabel = QLabel("Start:")
        self.startLine = QTimeEdit()
        endLabel = QLabel("End:")
        self.endLine = QTimeEdit()
        self.submitButton = QPushButton("Submit")
 
        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(dateLabel)
        buttonLayout1.addWidget(self.dateLine)
        buttonLayout1.addWidget(caseLabel)
        buttonLayout1.addWidget(self.caseLine)
        buttonLayout1.addWidget(startLabel)
        buttonLayout1.addWidget(self.endLine)
        buttonLayout1.addWidget(endLabel)
        buttonLayout1.addWidget(self.startLine)
        buttonLayout1.addWidget(self.submitButton)
 
        self.submitButton.clicked.connect(self.submitContact)
 
        mainLayout = QGridLayout()
        # mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addLayout(buttonLayout1, 0, 1)
 
        self.setLayout(mainLayout)
        self.setWindowTitle("Hello Qt")
 
    def submitContact(self):
        date = self.dateLine.selectedDate().toPyDate()
        case = self.caseLine.text()
        
        QMessageBox.information(self, "Success!",
                                    "%s!" % str(date))
 
if __name__ == '__main__':
    import sys
 
    app = QApplication(sys.argv)
 
    screen = Form()
    screen.show()
 
    sys.exit(app.exec_())
