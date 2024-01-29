# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(699, 300)
        self.verticalLayout = QVBoxLayout(Settings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Settings)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.default_calibration = QCheckBox(Settings)
        self.default_calibration.setObjectName(u"default_calibration")
        self.default_calibration.setChecked(True)
        self.default_calibration.setTristate(False)

        self.verticalLayout.addWidget(self.default_calibration)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.setting_drag_gain = QLineEdit(Settings)
        self.setting_drag_gain.setObjectName(u"setting_drag_gain")
        self.setting_drag_gain.setEnabled(False)

        self.gridLayout.addWidget(self.setting_drag_gain, 1, 1, 1, 1)

        self.label_3 = QLabel(Settings)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)

        self.label_2 = QLabel(Settings)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.setting_lift_gain = QLineEdit(Settings)
        self.setting_lift_gain.setObjectName(u"setting_lift_gain")
        self.setting_lift_gain.setEnabled(False)

        self.gridLayout.addWidget(self.setting_lift_gain, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.label_4 = QLabel(Settings)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.sample_rate_calibration = QSpinBox(Settings)
        self.sample_rate_calibration.setObjectName(u"sample_rate_calibration")
        self.sample_rate_calibration.setMinimum(1)
        self.sample_rate_calibration.setValue(5)

        self.verticalLayout.addWidget(self.sample_rate_calibration)

        self.label_5 = QLabel(Settings)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout.addWidget(self.label_5)

        self.amount_samples_calibration = QSpinBox(Settings)
        self.amount_samples_calibration.setObjectName(u"amount_samples_calibration")
        self.amount_samples_calibration.setMinimum(1)
        self.amount_samples_calibration.setMaximum(99)
        self.amount_samples_calibration.setValue(5)

        self.verticalLayout.addWidget(self.amount_samples_calibration)

        self.label_6 = QLabel(Settings)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.verticalLayout.addWidget(self.label_6)

        self.label_7 = QLabel(Settings)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout.addWidget(self.label_7)

        self.sample_rate_measure = QSpinBox(Settings)
        self.sample_rate_measure.setObjectName(u"sample_rate_measure")
        self.sample_rate_measure.setMinimum(1)
        self.sample_rate_measure.setValue(5)

        self.verticalLayout.addWidget(self.sample_rate_measure)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.save_settings = QPushButton(Settings)
        self.save_settings.setObjectName(u"save_settings")

        self.horizontalLayout.addWidget(self.save_settings)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Settings)

        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Settings", None))
        self.label.setText(QCoreApplication.translate("Settings", u"Calibrarion Settings", None))
        self.default_calibration.setText(QCoreApplication.translate("Settings", u"Calibrate sensors using default factory settings", None))
        self.label_3.setText(QCoreApplication.translate("Settings", u"drag gain", None))
        self.label_2.setText(QCoreApplication.translate("Settings", u"lift gain", None))
        self.label_4.setText(QCoreApplication.translate("Settings", u"Sample rate (Hz)", None))
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("Settings", u"Amount of Samples", None))
#if QT_CONFIG(tooltip)
        self.amount_samples_calibration.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("Settings", u"Measuring Settings", None))
        self.label_7.setText(QCoreApplication.translate("Settings", u"Sample rate (Hz)", None))
        self.save_settings.setText(QCoreApplication.translate("Settings", u"Save Settings", None))
    # retranslateUi

