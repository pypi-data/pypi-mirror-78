# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/devices_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DevicesWidget(object):
    def setupUi(self, DevicesWidget):
        DevicesWidget.setObjectName("DevicesWidget")
        DevicesWidget.resize(477, 548)
        DevicesWidget.setStyleSheet("#button_add_device {\n"
"    background-color: none;\n"
"    border: none;\n"
"    color: #0092FF;\n"
"}\n"
"\n"
"#button_add_device:hover {\n"
"    color: #0070DD;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(DevicesWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_edit_search = QtWidgets.QLineEdit(DevicesWidget)
        self.line_edit_search.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_edit_search.setFont(font)
        self.line_edit_search.setObjectName("line_edit_search")
        self.horizontalLayout.addWidget(self.line_edit_search)
        self.button_add_device = Button(DevicesWidget)
        self.button_add_device.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/material/add_to_queue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_add_device.setIcon(icon)
        self.button_add_device.setIconSize(QtCore.QSize(24, 24))
        self.button_add_device.setFlat(True)
        self.button_add_device.setProperty("color", QtGui.QColor(0, 146, 255))
        self.button_add_device.setObjectName("button_add_device")
        self.horizontalLayout.addWidget(self.button_add_device)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scroll_area = QtWidgets.QScrollArea(DevicesWidget)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scroll_area.setLineWidth(0)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.widget_content = QtWidgets.QWidget()
        self.widget_content.setGeometry(QtCore.QRect(0, 0, 475, 442))
        self.widget_content.setObjectName("widget_content")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_content)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.layout_content = QtWidgets.QVBoxLayout()
        self.layout_content.setContentsMargins(0, 0, 4, 0)
        self.layout_content.setSpacing(0)
        self.layout_content.setObjectName("layout_content")
        self.verticalLayout_4.addLayout(self.layout_content)
        self.scroll_area.setWidget(self.widget_content)
        self.verticalLayout_2.addWidget(self.scroll_area)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(DevicesWidget)
        QtCore.QMetaObject.connectSlotsByName(DevicesWidget)

    def retranslateUi(self, DevicesWidget):
        _translate = QtCore.QCoreApplication.translate
        DevicesWidget.setWindowTitle(_translate("DevicesWidget", "Form"))
        self.line_edit_search.setPlaceholderText(_translate("DevicesWidget", "TEXT_DEVICE_FILTER_PLACEHOLDER"))
        self.button_add_device.setToolTip(_translate("DevicesWidget", "TEXT_DEVICE_ADD_NEW_TOOLTIP"))
        self.button_add_device.setText(_translate("DevicesWidget", "ACTION_DEVICE_ADD_NEW"))
from parsec.core.gui.custom_widgets import Button
from parsec.core.gui import resources_rc
