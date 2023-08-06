# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/timestamped_workspace_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TimestampedWorkspaceWidget(object):
    def setupUi(self, TimestampedWorkspaceWidget):
        TimestampedWorkspaceWidget.setObjectName("TimestampedWorkspaceWidget")
        TimestampedWorkspaceWidget.resize(565, 501)
        TimestampedWorkspaceWidget.setStyleSheet("#button_show {\n"
"    text-transform: uppercase;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(TimestampedWorkspaceWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(TimestampedWorkspaceWidget)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_info = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_info.setFont(font)
        self.label_info.setWordWrap(True)
        self.label_info.setObjectName("label_info")
        self.verticalLayout_2.addWidget(self.label_info)
        self.widget_reencrypt = QtWidgets.QWidget(self.widget)
        self.widget_reencrypt.setObjectName("widget_reencrypt")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_reencrypt)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(20)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.widget_reencrypt)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.calendar_widget = QtWidgets.QCalendarWidget(self.widget_reencrypt)
        self.calendar_widget.setStyleSheet("")
        self.calendar_widget.setObjectName("calendar_widget")
        self.verticalLayout_4.addWidget(self.calendar_widget)
        self.label_2 = QtWidgets.QLabel(self.widget_reencrypt)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.time_edit = QtWidgets.QTimeEdit(self.widget_reencrypt)
        self.time_edit.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.time_edit.setFont(font)
        self.time_edit.setObjectName("time_edit")
        self.verticalLayout_4.addWidget(self.time_edit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_show = QtWidgets.QPushButton(self.widget_reencrypt)
        self.button_show.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        self.button_show.setFont(font)
        self.button_show.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_show.setIconSize(QtCore.QSize(20, 20))
        self.button_show.setObjectName("button_show")
        self.horizontalLayout_2.addWidget(self.button_show)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.widget_reencrypt)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(TimestampedWorkspaceWidget)
        QtCore.QMetaObject.connectSlotsByName(TimestampedWorkspaceWidget)

    def retranslateUi(self, TimestampedWorkspaceWidget):
        _translate = QtCore.QCoreApplication.translate
        TimestampedWorkspaceWidget.setWindowTitle(_translate("TimestampedWorkspaceWidget", "Form"))
        self.label_info.setText(_translate("TimestampedWorkspaceWidget", "TEXT_WORKSPACE_TIMESTAMPED_INSTRUCTIONS"))
        self.label.setText(_translate("TimestampedWorkspaceWidget", "TEXT_WORKSPACE_TIMESTAMPED_SELECT_DATE"))
        self.label_2.setText(_translate("TimestampedWorkspaceWidget", "TEXT_WORKSPACE_TIMESTAMPED_SELECT_TIME"))
        self.button_show.setText(_translate("TimestampedWorkspaceWidget", "ACTION_WORKSPACE_TIMESTAMPED_MOUNT"))
