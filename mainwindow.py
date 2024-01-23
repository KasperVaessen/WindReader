# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(823, 518)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer)

        self.save_csv_button = QPushButton(self.centralwidget)
        self.save_csv_button.setObjectName(u"save_csv_button")

        self.horizontalLayout_9.addWidget(self.save_csv_button)


        self.gridLayout.addLayout(self.horizontalLayout_9, 5, 0, 1, 1)

        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 6):
            self.tableWidget.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        if (self.tableWidget.rowCount() < 1):
            self.tableWidget.setRowCount(1)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setItem(0, 0, __qtablewidgetitem6)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setProperty("showDropIndicator", True)
        self.tableWidget.setDragDropOverwriteMode(True)
        self.tableWidget.setSortingEnabled(True)

        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.Lift_box = QVBoxLayout()
        self.Lift_box.setSpacing(2)
        self.Lift_box.setObjectName(u"Lift_box")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.Lift_box.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lift_entry = QLineEdit(self.centralwidget)
        self.lift_entry.setObjectName(u"lift_entry")
        self.lift_entry.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.lift_entry)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)


        self.Lift_box.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addLayout(self.Lift_box)

        self.Drag_box = QVBoxLayout()
        self.Drag_box.setSpacing(2)
        self.Drag_box.setObjectName(u"Drag_box")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.Drag_box.addWidget(self.label_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.drag_entry = QLineEdit(self.centralwidget)
        self.drag_entry.setObjectName(u"drag_entry")
        self.drag_entry.setEnabled(False)

        self.horizontalLayout_3.addWidget(self.drag_entry)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)


        self.Drag_box.addLayout(self.horizontalLayout_3)


        self.horizontalLayout.addLayout(self.Drag_box)

        self.Pressure_box = QVBoxLayout()
        self.Pressure_box.setSpacing(2)
        self.Pressure_box.setObjectName(u"Pressure_box")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")

        self.Pressure_box.addWidget(self.label_7)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pressure_entry = QLineEdit(self.centralwidget)
        self.pressure_entry.setObjectName(u"pressure_entry")
        self.pressure_entry.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.pressure_entry)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_5.addWidget(self.label_8)


        self.Pressure_box.addLayout(self.horizontalLayout_5)


        self.horizontalLayout.addLayout(self.Pressure_box)

        self.temp_box = QVBoxLayout()
        self.temp_box.setSpacing(2)
        self.temp_box.setObjectName(u"temp_box")
        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")

        self.temp_box.addWidget(self.label_11)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.temp_entry = QLineEdit(self.centralwidget)
        self.temp_entry.setObjectName(u"temp_entry")
        self.temp_entry.setEnabled(False)

        self.horizontalLayout_7.addWidget(self.temp_entry)

        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_7.addWidget(self.label_12)


        self.temp_box.addLayout(self.horizontalLayout_7)


        self.horizontalLayout.addLayout(self.temp_box)

        self.diff_press_box = QVBoxLayout()
        self.diff_press_box.setSpacing(2)
        self.diff_press_box.setObjectName(u"diff_press_box")
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")

        self.diff_press_box.addWidget(self.label_13)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.diff_pres_entry = QLineEdit(self.centralwidget)
        self.diff_pres_entry.setObjectName(u"diff_pres_entry")
        self.diff_pres_entry.setEnabled(False)

        self.horizontalLayout_8.addWidget(self.diff_pres_entry)

        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_8.addWidget(self.label_14)


        self.diff_press_box.addLayout(self.horizontalLayout_8)


        self.horizontalLayout.addLayout(self.diff_press_box)

        self.speed_box = QVBoxLayout()
        self.speed_box.setSpacing(2)
        self.speed_box.setObjectName(u"speed_box")
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")

        self.speed_box.addWidget(self.label_9)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.speed_entry = QLineEdit(self.centralwidget)
        self.speed_entry.setObjectName(u"speed_entry")
        self.speed_entry.setEnabled(False)

        self.horizontalLayout_6.addWidget(self.speed_entry)

        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_6.addWidget(self.label_10)


        self.speed_box.addLayout(self.horizontalLayout_6)


        self.horizontalLayout.addLayout(self.speed_box)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.start_measure_button = QPushButton(self.centralwidget)
        self.start_measure_button.setObjectName(u"start_measure_button")

        self.verticalLayout.addWidget(self.start_measure_button)

        self.stop_measure_button = QPushButton(self.centralwidget)
        self.stop_measure_button.setObjectName(u"stop_measure_button")

        self.verticalLayout.addWidget(self.stop_measure_button)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tare_button = QPushButton(self.centralwidget)
        self.tare_button.setObjectName(u"tare_button")

        self.verticalLayout_3.addWidget(self.tare_button)

        self.save_measurement = QPushButton(self.centralwidget)
        self.save_measurement.setObjectName(u"save_measurement")

        self.verticalLayout_3.addWidget(self.save_measurement)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 823, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.save_csv_button.setText(QCoreApplication.translate("MainWindow", u"Save to CSV", None))
#if QT_CONFIG(shortcut)
        self.save_csv_button.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Drag (N)", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Lift (N)", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Pressure (kPa)", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Temperature (K)", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Difference Pressure (Pa)", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Wind Speed (m/s)", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.label.setText(QCoreApplication.translate("MainWindow", u"Lift", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"N", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Drag", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"N", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Pressure", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"kPa", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Temperature", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"K", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Difference Pressure", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Pa", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Wind Speed", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"m/s", None))
        self.start_measure_button.setText(QCoreApplication.translate("MainWindow", u"Start Measuring", None))
        self.stop_measure_button.setText(QCoreApplication.translate("MainWindow", u"Stop Measuring", None))
        self.tare_button.setText(QCoreApplication.translate("MainWindow", u"Tare", None))
        self.save_measurement.setText(QCoreApplication.translate("MainWindow", u"Save Current", None))
    # retranslateUi

