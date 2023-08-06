# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/sharing_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SharingWidget(object):
    def setupUi(self, SharingWidget):
        SharingWidget.setObjectName("SharingWidget")
        SharingWidget.setEnabled(True)
        SharingWidget.resize(572, 45)
        SharingWidget.setMinimumSize(QtCore.QSize(20, 45))
        SharingWidget.setStyleSheet("#SharingWidget:!disabled\n"
"{\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"#button_delete\n"
"{\n"
"border: 0;\n"
"background: 0;\n"
"}")
        self.horizontalLayout = QtWidgets.QHBoxLayout(SharingWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 20, 0)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_name = QtWidgets.QLabel(SharingWidget)
        self.label_name.setText("")
        self.label_name.setObjectName("label_name")
        self.horizontalLayout.addWidget(self.label_name)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.combo_role = ComboBox(SharingWidget)
        self.combo_role.setMinimumSize(QtCore.QSize(150, 32))
        self.combo_role.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.combo_role.setFont(font)
        self.combo_role.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.combo_role.setObjectName("combo_role")
        self.horizontalLayout.addWidget(self.combo_role)

        self.retranslateUi(SharingWidget)
        QtCore.QMetaObject.connectSlotsByName(SharingWidget)

    def retranslateUi(self, SharingWidget):
        _translate = QtCore.QCoreApplication.translate
        SharingWidget.setWindowTitle(_translate("SharingWidget", "Form"))
from parsec.core.gui.custom_widgets import ComboBox
