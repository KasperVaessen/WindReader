import csv
import os
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Measurement import MeasureMock

from mainwindow import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.meassurement = MeasureMock()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.removeRow(0)
        self.ui.start_measure_button.clicked.connect(self.start_measure)
        self.ui.stop_measure_button.clicked.connect(self.stop_measure)
        self.ui.tare_button.clicked.connect(self.meassurement.zero_data)
        self.ui.save_measurement.clicked.connect(self.save_measurement)
        self.ui.save_csv_button.clicked.connect(self.save_to_csv)
    
    def start_measure(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_measure)
        self.timer.start(200)
    
    def stop_measure(self):
        self.timer.stop()
    
    def update_measure(self):
        values = self.meassurement.get_values()
        self.ui.lift_entry.setText(format(values[0], '.3f'))
        self.ui.drag_entry.setText(format(values[1], '.3f'))
        self.ui.pressure_entry.setText(format(values[2], '.2f'))
        self.ui.temp_entry.setText(format(values[3], '.1f'))
        self.ui.diff_pres_entry.setText(format(values[4], '.1f'))
        self.ui.speed_entry.setText(format(values[5], '.1f'))
    
    def save_measurement(self):
        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1, 0, QTableWidgetItem(self.ui.lift_entry.text()))
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1, 1, QTableWidgetItem(self.ui.drag_entry.text()))
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1, 2, QTableWidgetItem(self.ui.pressure_entry.text()))
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1, 3, QTableWidgetItem(self.ui.temp_entry.text()))
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1, 4, QTableWidgetItem(self.ui.diff_pres_entry.text()))
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1, 5, QTableWidgetItem(self.ui.speed_entry.text()))
    
    def save_to_csv(self):
        path, ok = QFileDialog.getSaveFileName(
            self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if ok:
            columns = range(self.ui.tableWidget.columnCount())
            header = [self.ui.tableWidget.horizontalHeaderItem(column).text() for column in columns]
            with open(path, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=";", dialect='excel', lineterminator='\n')
                writer.writerow(header)
                for row in range(self.ui.tableWidget.rowCount()):
                    writer.writerow(self.ui.tableWidget.item(row, column).text() for column in columns)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
