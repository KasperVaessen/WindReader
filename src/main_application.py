import csv
import os
import sys
import pyqtgraph as pg
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from Measurement import MeasureMock, MeasureWindTunnel
from priv.mainwindow import Ui_MainWindow

class overlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, Qt.transparent)

        self.setPalette(palette)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(0, 0, 0, 127)))
        font = painter.font()
        font.setPointSize(20)
        painter.setFont(font)
        painter.drawText(event.rect(), Qt.AlignCenter, "Phidgets not connected")
        painter.setPen(QPen(Qt.NoPen))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.overlay = overlay(self)
        self.overlay.showMaximized()
        self.overlay.setVisible(True)

        self.meassurement = MeasureMock(self.phidget_attached, self.phidget_detached)

        self.ui.tableWidget.removeRow(0)
        self.ui.start_measure_button.clicked.connect(self.start_measure)
        self.ui.stop_measure_button.clicked.connect(self.stop_measure)
        self.ui.tare_button.clicked.connect(self.meassurement.zero_data)
        self.ui.save_measurement.clicked.connect(self.save_measurement)
        self.ui.save_csv_button.clicked.connect(self.save_to_csv)

        self.recent_lift = []
        self.recent_drag = []
        self.recent_diff_pressure = []
        self.recent_wind_speed = []

        self.init_plots()
        
    def init_plots(self):
        for plot in [self.ui.plot_1, self.ui.plot_2, self.ui.plot_3, self.ui.plot_4]:
            plot.setBackground('w')
            plot.showGrid(x=True, y=True)
            plot.setLabel('bottom', 'Time (s)')
        
        self.ui.plot_1.setTitle("Lift")
        self.ui.plot_2.setTitle("Drag")
        self.ui.plot_3.setTitle("Diff. Pressure")
        self.ui.plot_4.setTitle("Wind Speed")

        self.ui.plot_1.setLabel('left', 'Lift (N)')
        self.ui.plot_2.setLabel('left', 'Drag (N)')
        self.ui.plot_3.setLabel('left', 'Diff. Pressure (Pa)')
        self.ui.plot_4.setLabel('left', 'Wind Speed (m/s)')

        self.line1 = self.ui.plot_1.plot(self.recent_lift, pen=pg.mkPen('b', width=1))
        self.line2 = self.ui.plot_2.plot(self.recent_drag, pen=pg.mkPen('b', width=1))
        self.line3 = self.ui.plot_3.plot(self.recent_diff_pressure, pen=pg.mkPen('b', width=1))
        self.line4 = self.ui.plot_4.plot(self.recent_wind_speed, pen=pg.mkPen('b', width=1))
    
    def updatePlots(self, values):
        if len(self.recent_lift) > 100:
            self.recent_lift.pop(0)
            self.recent_drag.pop(0)
            self.recent_diff_pressure.pop(0)
            self.recent_wind_speed.pop(0)
        else:
            self.x = [x*0.2 for x in range(-(len(self.recent_lift)),1)]
        self.recent_lift.append(values[0])
        self.recent_drag.append(values[1])
        self.recent_diff_pressure.append(values[4])
        self.recent_wind_speed.append(values[5])

        self.line1.setData(self.x, self.recent_lift)
        self.line2.setData(self.x, self.recent_drag)
        self.line3.setData(self.x, self.recent_diff_pressure)
        self.line4.setData(self.x, self.recent_wind_speed)
    
    
    def resizeEvent(self, event):
        self.overlay.resize(event.size())
        event.accept()


    def start_measure(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_measure)
        self.timer.start(200)
    
    def phidget_attached(self):
        self.overlay.setVisible(False)
        self.ui.label_5.setText("Phidgets connected")
    
    def phidget_detached(self):
        self.overlay.setVisible(True)
        self.ui.label_5.setText("Phidgets disconnected")
    
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

        self.updatePlots(values)
    
    def save_measurement(self):
        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1, 0, QTableWidgetItem(self.ui.lift_entry.text()))
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1, 1, QTableWidgetItem(self.ui.drag_entry.text()))
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1, 2, QTableWidgetItem(self.ui.pressure_entry.text()))
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1, 3, QTableWidgetItem(self.ui.temp_entry.text()))
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1, 4, QTableWidgetItem(self.ui.diff_pres_entry.text()))
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1, 5, QTableWidgetItem(self.ui.speed_entry.text()))
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1, 6, QTableWidgetItem(self.ui.angle_entry.text()))
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1, 7, QTableWidgetItem(self.ui.surface_entry.text()))
    
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
