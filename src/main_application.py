import csv
import os
import sys
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QHeaderView, QTableWidgetItem, QFileDialog, QMessageBox
from PySide6.QtCore import QTimer, QSettings, QRegularExpression, Qt, QPersistentModelIndex
from PySide6.QtGui import QPalette, QPainter, QBrush, QColor, QPen, QRegularExpressionValidator, QShortcut, QKeySequence
# from Measurement import MeasureWindTunnel
from mock_measurement import MeasureWindTunnel
from priv.mainwindow import Ui_MainWindow
from priv.settingswindow import Ui_Settings
from qt_material import apply_stylesheet


# A class to create a semi-transparent overlay to show when the phidgets are not connected
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

# A class to create the settings window
class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Settings()
        self.ui.setupUi(self)

# A class to create the main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize the overlay that shows when the phidgets are not connected
        self.overlay = overlay(self)
        self.overlay.showMaximized()
        self.overlay.setVisible(True)

        # Set the table to resize the columns to the content
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Set the settings file
        self.settings = QSettings("PWS_Lab", "Wind Tunnel")

        # Try to create the measurement object, if the phidget library is not installed, show an error message and exit the program
        try:
            self.meassurement = MeasureWindTunnel(self.phidget_attached, self.phidget_detached)
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Phidget library not found")
            msg.setText("The Phidget library is not installed.\n\n Please install from https://www.phidgets.com/.")
            msg.exec()
            sys.exit("Phidget library not found")

        # Connect the buttons to the functions
        self.ui.tableWidget.removeRow(0)
        self.shortcut = QShortcut(QKeySequence("del"), self)
        self.shortcut.activated.connect(self.delete)
        self.ui.tableWidget.itemChanged.connect(self.update_graph_data)
        self.ui.start_measure_button.clicked.connect(self.start_measure)
        self.ui.start_measure_button2.clicked.connect(self.start_measure)
        self.ui.stop_measure_button.clicked.connect(self.stop_measure)
        self.ui.stop_measure_button2.clicked.connect(self.stop_measure)
        self.ui.tare_button.clicked.connect(self.tare_measure)
        self.ui.save_measurement.clicked.connect(self.save_measurement)
        self.ui.save_csv_button.clicked.connect(self.save_to_csv)

        # Initialize the variables for the plots
        self.recent_lift = []
        self.recent_drag = []
        self.recent_diff_pressure = []
        self.recent_wind_speed = []
        self.cl_data = []
        self.cd_data = []
        self.alpha_data = []

        # Validate input
        reg_ex = QRegularExpression("[+-]?([0-9]*[.])?[0-9]+")
        angle_validator = QRegularExpressionValidator(reg_ex, self.ui.angle_entry)
        area_validator = QRegularExpressionValidator(reg_ex, self.ui.surface_entry)
        self.ui.angle_entry.setValidator(angle_validator)
        self.ui.surface_entry.setValidator(area_validator)

        # Connect the menu buttons to the functions
        self.ui.actionSave.triggered.connect(self.save_to_csv)
        self.ui.actionSettings.triggered.connect(lambda : self.show_settings(self.settings))

        self.init_plots()
        
    # Calibrates the load cells based on the settings
    def tare_measure(self):
        amount_samples = self.settings.value("amount_samples_calibration", 5)
        sample_rate = self.settings.value("sample_rate_calibration", 5)
        default_calibration = self.settings.value("default_calibration", "true") == "true"
        drag_gain = float(self.settings.value("drag gain", "9907.67"))
        lift_gain = float(self.settings.value("lift gain", "11148.31"))
        self.meassurement.zero_data(amount_samples, 1/sample_rate, default_calibration, drag_gain, lift_gain)

    # Creates empty plots
    def init_plots(self):
        for plot in [self.ui.plot_1, self.ui.plot_2, self.ui.plot_3, self.ui.plot_4]:
            plot.setBackground(None)
            plot.showGrid(x=True, y=True)
            plot.setStyleSheet("border: 0px")
            plot.setLabel('bottom', 'Time (s)')
        for plot in [self.ui.plot_5, self.ui.plot_6]:
            plot.setBackground(None)
            plot.showGrid(x=True, y=True)
            plot.setStyleSheet("border: 0px")
            plot.setLabel('left', 'CL')
        
        self.ui.plot_1.setTitle("Lift")
        self.ui.plot_2.setTitle("Drag")
        self.ui.plot_3.setTitle("Diff. Pressure")
        self.ui.plot_4.setTitle("Wind Speed")
        self.ui.plot_5.setTitle("Lift Coefficient vs alpha")
        self.ui.plot_6.setTitle("Lift Coefficient vs Drag Coefficient")

        self.ui.plot_1.setLabel('left', 'Lift (N)')
        self.ui.plot_2.setLabel('left', 'Drag (N)')
        self.ui.plot_3.setLabel('left', 'Diff. Pressure (Pa)')
        self.ui.plot_4.setLabel('left', 'Wind Speed (m/s)')
        self.ui.plot_5.setLabel('bottom', 'alpha (deg)')
        self.ui.plot_6.setLabel('bottom', 'CD')

        #set pen color to color primary color of style, which is saved as an environment variable.
        self.line1 = self.ui.plot_1.plot(self.recent_lift, pen=pg.mkPen('r', width=1))
        self.line2 = self.ui.plot_2.plot(self.recent_drag, pen=pg.mkPen('r', width=1))
        self.line3 = self.ui.plot_3.plot(self.recent_diff_pressure, pen=pg.mkPen('r', width=1))
        self.line4 = self.ui.plot_4.plot(self.recent_wind_speed, pen=pg.mkPen('r', width=1))
        self.line5 = self.ui.plot_5.plot(self.alpha_data, self.cl_data, pen=pg.mkPen(None), symbol ='x', symbolBrush='r')
        self.line6 = self.ui.plot_6.plot(self.cd_data,self.cl_data, pen=pg.mkPen(None), symbol ='x', symbolBrush='r')
    
    # Updates the plots with new data
    def updatePlots(self, values):
        # If data is too long, remove the oldest data point
        if len(self.recent_lift) > 100:
            self.recent_lift.pop(0)
            self.recent_drag.pop(0)
            self.recent_diff_pressure.pop(0)
            self.recent_wind_speed.pop(0)
        else:
            #update x axis, while data is not its max length
            self.x = [x/self.settings.value("sample_rate_measure", 5) for x in range(-(len(self.recent_lift)),1)]
        
        # Add new data point
        self.recent_lift.append(values[0])
        self.recent_drag.append(values[1])
        self.recent_diff_pressure.append(values[4])
        self.recent_wind_speed.append(values[5])

        # Only update the graph if the user has the graph tab open
        if self.ui.graph_tab.isVisible():
            self.line1.setData(self.x, self.recent_lift)
            self.line2.setData(self.x, self.recent_drag)
            self.line3.setData(self.x, self.recent_diff_pressure)
            self.line4.setData(self.x, self.recent_wind_speed)
    
    # Resizes the overlay to the size of the window
    def resizeEvent(self, event):
        self.overlay.resize(event.size())
        event.accept()

    # Starts the measurement
    def start_measure(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_measure)
        self.timer.start(1000/self.settings.value("sample_rate_measure", 5))
        self.ui.stop_measure_button.setEnabled(True)
        self.ui.stop_measure_button2.setEnabled(True)
        self.ui.start_measure_button.setEnabled(False)
        self.ui.start_measure_button2.setEnabled(False)

        #reset data for plots
        self.recent_diff_pressure = []
        self.recent_drag = []
        self.recent_lift = []
        self.recent_wind_speed = []
    
    # Callback function for when the phidgets are connected
    def phidget_attached(self):
        self.overlay.setVisible(False)
        self.ui.label_5.setText("Phidgets connected")
    
    # Callback function for when the phidgets are disconnected
    def phidget_detached(self):
        self.overlay.setVisible(True)
        self.ui.label_5.setText("Phidgets disconnected")
    
    # Stops the measurement
    def stop_measure(self):
        self.timer.stop()
        self.ui.stop_measure_button.setEnabled(False)
        self.ui.stop_measure_button2.setEnabled(False)
        self.ui.start_measure_button.setEnabled(True)
        self.ui.start_measure_button2.setEnabled(True)
    
    # Updates the measurement values in the fields and plots
    def update_measure(self):
        values = self.meassurement.get_values()
        self.ui.lift_entry.setText(format(values[0], '.3f'))
        self.ui.drag_entry.setText(format(values[1], '.3f'))
        self.ui.pressure_entry.setText(format(values[2], '.2f'))
        self.ui.temp_entry.setText(format(values[3], '.1f'))
        self.ui.diff_pres_entry.setText(format(values[4], '.1f'))
        self.ui.speed_entry.setText(format(values[5], '.1f'))

        self.updatePlots(values)
    
    # Saves the measurement values to the table
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

    # Saves the measurement values to a csv file
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

    # Shows the settings window
    def show_settings(self, settings):
        #Set fields to current setting values
        self.settings_window = Settings()
        self.settings_window.ui.sample_rate_calibration.setValue(settings.value("sample_rate_calibration", 5))
        self.settings_window.ui.amount_samples_calibration.setValue(settings.value("amount_samples_calibration", 5))
        self.settings_window.ui.default_calibration.setChecked(settings.value("default_calibration", "true") == "true")
        self.settings_window.ui.setting_drag_gain.setText(settings.value("drag gain", "9907.67"))
        self.settings_window.ui.setting_lift_gain.setText(settings.value("lift gain", "11148.31"))
        self.settings_window.ui.sample_rate_measure.setValue(settings.value("sample_rate_measure", 5))
        self.settings_window.ui.default_calibration.stateChanged.connect(self.change_gain_enabled)

        #validate input
        reg_ex = QRegularExpression("[+-]?([0-9]*[.])?[0-9]+")
        drag_validator = QRegularExpressionValidator(reg_ex, self.settings_window.ui.setting_drag_gain)
        lift_validator = QRegularExpressionValidator(reg_ex, self.settings_window.ui.setting_lift_gain)
        self.settings_window.ui.setting_drag_gain.setValidator(drag_validator)
        self.settings_window.ui.setting_lift_gain.setValidator(lift_validator)

        self.settings_window.show()
        self.settings_window.ui.save_settings.clicked.connect(lambda : self.save_settings(settings))

    # Enables or disables the gain fields based on the default calibration checkbox
    def change_gain_enabled(self):
        self.settings_window.ui.setting_drag_gain.setEnabled(not self.settings_window.ui.default_calibration.isChecked())
        self.settings_window.ui.setting_lift_gain.setEnabled(not self.settings_window.ui.default_calibration.isChecked())

    # Saves the settings to the settings file
    def save_settings(self, settings):
        settings.setValue("sample_rate_calibration", self.settings_window.ui.sample_rate_calibration.value())
        settings.setValue("amount_samples_calibration", self.settings_window.ui.amount_samples_calibration.value())
        settings.setValue("default_calibration", self.settings_window.ui.default_calibration.isChecked())
        settings.setValue("drag gain", self.settings_window.ui.setting_drag_gain.text())
        settings.setValue("lift gain", self.settings_window.ui.setting_lift_gain.text())
        settings.setValue("sample_rate_measure", self.settings_window.ui.sample_rate_measure.value())

        self.settings_window.close()

    # Deletes the selected row from the table
    def delete(self):
        if self.ui.tableWidget.selectionModel().hasSelection():
            indexes =[QPersistentModelIndex(index) for index in self.ui.tableWidget.selectionModel().selectedRows()]
            for index in indexes:
                self.ui.tableWidget.removeRow(index.row())

    def update_graph_data(self):
        cl_data = []
        cd_data = []
        alpha_data = []
        for row in range(self.ui.tableWidget.rowCount()):
            # Get the values from the table if present
            try:
                lift = float(self.ui.tableWidget.item(row, 0).text())
                drag = float(self.ui.tableWidget.item(row, 1).text())
                pressure = float(self.ui.tableWidget.item(row, 2).text())
                temp = float(self.ui.tableWidget.item(row, 3).text())
                speed = float(self.ui.tableWidget.item(row, 5).text())
                angle = float(self.ui.tableWidget.item(row, 6).text())
                surface = float(self.ui.tableWidget.item(row, 7).text())
            except:
                continue

            # Calulate lift coeficient and drag coeficient
            if speed > 0 and surface > 0:
                c_algGasConst = 8.31
                c_molMassa = 0.0288
                # Ideal gas law: pV = nRT
                airDensity = c_molMassa * pressure * 1000 / (c_algGasConst * temp)
                cl = lift/(0.5*airDensity*speed**2*surface)
                cd = drag/(0.5*airDensity*speed**2*surface)

                cl_data.append(cl)
                cd_data.append(cd)
                alpha_data.append(angle)
        self.line5.setData(alpha_data, cl_data)
        self.line6.setData(cd_data, cl_data)

    
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    apply_stylesheet(app, theme='light_red.xml', invert_secondary=True)

    window.show()

    sys.exit(app.exec())
