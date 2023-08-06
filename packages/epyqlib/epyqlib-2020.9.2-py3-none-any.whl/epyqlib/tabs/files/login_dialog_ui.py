# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_root_dialog(object):
    def setupUi(self, root_dialog):
        root_dialog.setObjectName("root_dialog")
        root_dialog.resize(474, 248)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(root_dialog.sizePolicy().hasHeightForWidth())
        root_dialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(root_dialog)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(root_dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.password = QtWidgets.QLineEdit(root_dialog)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 2, 1, 1, 1)
        self.lbl_error_message = QtWidgets.QLabel(root_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_error_message.sizePolicy().hasHeightForWidth())
        self.lbl_error_message.setSizePolicy(sizePolicy)
        self.lbl_error_message.setMinimumSize(QtCore.QSize(0, 30))
        self.lbl_error_message.setTextFormat(QtCore.Qt.RichText)
        self.lbl_error_message.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lbl_error_message.setWordWrap(True)
        self.lbl_error_message.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lbl_error_message.setObjectName("lbl_error_message")
        self.gridLayout.addWidget(self.lbl_error_message, 3, 0, 1, 2)
        self.username = QtWidgets.QLineEdit(root_dialog)
        self.username.setObjectName("username")
        self.gridLayout.addWidget(self.username, 1, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, 16, 0, 16)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.big_label = QtWidgets.QLabel(root_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.big_label.sizePolicy().hasHeightForWidth())
        self.big_label.setSizePolicy(sizePolicy)
        self.big_label.setTextFormat(QtCore.Qt.RichText)
        self.big_label.setObjectName("big_label")
        self.horizontalLayout_3.addWidget(self.big_label)
        self.spacer_label = QtWidgets.QLabel(root_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spacer_label.sizePolicy().hasHeightForWidth())
        self.spacer_label.setSizePolicy(sizePolicy)
        self.spacer_label.setStyleSheet("color: rgba(0,0,0,0%)")
        self.spacer_label.setTextFormat(QtCore.Qt.RichText)
        self.spacer_label.setObjectName("spacer_label")
        self.horizontalLayout_3.addWidget(self.spacer_label)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 2)
        self.button_box = QtWidgets.QDialogButtonBox(root_dialog)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.gridLayout.addWidget(self.button_box, 4, 0, 1, 2)
        self.label = QtWidgets.QLabel(root_dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.gridLayout.setRowStretch(0, 1)

        self.retranslateUi(root_dialog)
        QtCore.QMetaObject.connectSlotsByName(root_dialog)
        root_dialog.setTabOrder(self.username, self.password)

    def retranslateUi(self, root_dialog):
        _translate = QtCore.QCoreApplication.translate
        root_dialog.setWindowTitle(_translate("root_dialog", "Dialog"))
        self.label_2.setText(_translate("root_dialog", "Password:"))
        self.lbl_error_message.setText(_translate("root_dialog", "<html><head/><body><p><span style=\" color:#fc0107;\">Error: Sample error here. and then some more and then some more and then some more and then some more and then some more and then</span></p></body></html>"))
        self.big_label.setText(_translate("root_dialog", "<html><head/><body><p>Login to EPC Sync</p></body></html>"))
        self.spacer_label.setText(_translate("root_dialog", "<html><head/><body><p>Login to EPC Sync</p></body></html>"))
        self.label.setText(_translate("root_dialog", "Username:"))
