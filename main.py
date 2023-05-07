import sys
import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Adding toolbar

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Adding StatusBar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click

        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        # Every cell click would create edit and delete buttons in the status bar.
        # To avoid that we find children and if they exist, we remove buttons widgets and create new

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

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

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
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
    def closing(self):
        self.accept()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Search Student")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        search_button = QPushButton("Search")
        layout.addWidget(search_button)
        search_button.clicked.connect(self.search)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        # Search in DB to print in the screen
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)
        print(rows)

        # Search in the GUI table
        items = project.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            project.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Management System")
        self.setFixedWidth(200)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Get student name from selected row
        index = project.table.currentRow()

        # add name widget
        student_name = project.table.item(index, 1).text()  # (row_index, column)
        self.name = QLineEdit(student_name)
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        # get id from selected row
        self.student_id = project.table.item(index, 0).text()

        # Add course combo box
        course = project.table.item(index, 2).text()  # extracting course name from selected row
        self.course_name = QComboBox()
        courses = ["Astronomy", "Biology", "Math", "Physics", ]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course)  # Select current course

        layout.addWidget(self.course_name)

        # Add mobile widget
        mobile = project.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add update button
        submit = QPushButton("Update")
        submit.clicked.connect(self.update_student)
        layout.addWidget(submit)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),
                        self.mobile.text(),
                        self.student_id))

        # don't forget to commit :D
        connection.commit()
        cursor.close()
        connection.close()
        # to refresh the table data, calling load_data()
        project.load_data()


class DeleteDialog(QDialog):
    pass


app = QApplication(sys.argv)
project = MainWindow()
project.load_data()
project.show()
sys.exit(app.exec())
