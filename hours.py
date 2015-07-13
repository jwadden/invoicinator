import models

import settings

import datetime

from PyQt5.QtWidgets import *
 
class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        
        dateLabel = QLabel("Date")
        self.dateLine = QCalendarWidget()
        taskLabel = QLabel("Task:")
        self.taskLine = QLineEdit()
        startLabel = QLabel("Start:")
        self.startLine = QTimeEdit()
        endLabel = QLabel("End:")
        self.endLine = QTimeEdit()
        self.submitButton = QPushButton("Submit")
 
        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(dateLabel)
        buttonLayout1.addWidget(self.dateLine)
        buttonLayout1.addWidget(taskLabel)
        buttonLayout1.addWidget(self.taskLine)
        buttonLayout1.addWidget(startLabel)
        buttonLayout1.addWidget(self.startLine)
        buttonLayout1.addWidget(endLabel)
        buttonLayout1.addWidget(self.endLine)
        buttonLayout1.addWidget(self.submitButton)
 
        self.submitButton.clicked.connect(self.submitContact)
 
        mainLayout = QGridLayout()
        # mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addLayout(buttonLayout1, 0, 1)
 
        self.setLayout(mainLayout)
        self.setWindowTitle("Hello Qt")
 
    def submitContact(self):
        task = self.taskLine.text()
        selected_date = self.dateLine.selectedDate().toPyDate()
        start_time = self.startLine.time().toPyTime()
        end_time = self.endLine.time().toPyTime()
        
        start_date = selected_date
        
        if end_time.hour == 0 and end_time.minute == 0:
            end_date = selected_date + datetime.timedelta(1)
        else:
            end_date = selected_date
        
        start_datetime = datetime.datetime.combine(
            self.dateLine.selectedDate().toPyDate(),
            self.startLine.time().toPyTime()
        )
        
        end_datetime = datetime.datetime.combine(
            self.dateLine.selectedDate().toPyDate(),
            self.endLine.time().toPyTime()
        )
        
        task_row = session.query(models.Task).filter(models.Task.name==self.taskLine.text()).first()
        
        if not task_row:
            task_row = models.Task(name=self.taskLine.text())
            
            session.add(task_row)
            
            session.commit()
            
        work_log = models.WorkLog(task_id=task_row.id, start_time=start_datetime, end_time=end_datetime)
        
        session.add(work_log)
        
        session.commit()
        #QMessageBox.information(self, "Success!", "%s!" % str(start_time))
 
if __name__ == '__main__':
    import sys
 
    app = QApplication(sys.argv)
 
    screen = Form()
    screen.show()
    
    session = models.Session()
 
    sys.exit(app.exec_())
