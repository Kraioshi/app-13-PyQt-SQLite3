import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
     QLineEdit, QPushButton, QComboBox


class SpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Speed Calculator")
        grid = QGridLayout()

        distance = QLabel("Distance:")
        self.distance_line = QLineEdit()

        time = QLabel("Time (Hours)")
        self.time_line = QLineEdit()

        calculate = QPushButton("Convert")
        calculate.clicked.connect(self.click)
        self.result = QLabel("")

        self.box = QComboBox()
        self.box.addItems(["Kilometers", "Miles"])

        grid.addWidget(distance, 0, 0)
        grid.addWidget(time, 1, 0)
        grid.addWidget(self.distance_line, 0, 1)
        grid.addWidget(self.time_line, 1, 1)
        grid.addWidget(calculate, 2, 1)
        grid.addWidget(self.result, 3, 0, 1, 2)
        grid.addWidget(self.box, 0, 2)

        self.setLayout(grid)

    def click(self):
        v = self.box.currentIndex()
        d = int(self.distance_line.text())
        t = int(self.time_line.text())

        if v == 0:
            res = d / t
            res = round(res, 2)
            self.result.setText(f"{res} km/h")
        elif v == 1:
            res = d / t
            res = round(res * 0.621371, 2)
            self.result.setText(f"{res} mph")


app = QApplication(sys.argv)
speed = SpeedCalculator()
speed.show()
sys.exit(app.exec())
