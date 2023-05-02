import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setFixedWidth(500)
        self.setFixedHeight(500)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setFixedWidth(200)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # add name widget
        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        # Add course combo box
        self.course_name = QComboBox()
        courses = ["Astronomy", "Biology", "Math", "Physics", ]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add submit button
        submit = QPushButton("Submit")
        submit.clicked.connect(self.add_student)
        layout.addWidget(submit)

        # Add cancel button
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.closing)
        layout.addWidget(cancel)

        self.setLayout(layout)

    def add_student(self):
        name = self.name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        if name != "" and mobile != "":
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                           (name, course, mobile))
            connection.commit()
            cursor.close()
            connection.close()
            project.load_data()
            self.closing()  # close after submit

    # close Dialog window
    def closing(self):   # Should be a better way idk?
        self.accept()



app = QApplication(sys.argv)
project = MainWindow()
project.load_data()
project.show()
sys.exit(app.exec())
