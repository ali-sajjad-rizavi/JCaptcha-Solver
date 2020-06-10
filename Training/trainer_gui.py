# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'jcaptcha_trainer.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import os


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, trainer_app):
        self.trainer_app = trainer_app
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(261, 214)
        MainWindow.setWindowIcon(QtGui.QIcon('icon/robot.ico'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.captchaBox = QtWidgets.QLabel(self.centralwidget)
        self.captchaBox.setGeometry(QtCore.QRect(50, 30, 151, 101))
        self.captchaBox.setText("")
        self.captchaBox.setPixmap(QtGui.QPixmap('Training Images/' + os.listdir('Training Images')[0]))
        self.captchaBox.setObjectName("captchaBox")
        #---------------------------------------------------------------------
        self.answer_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.answer_lineEdit.setGeometry(QtCore.QRect(80, 150, 91, 31))
        #---------------------------------------------------------------------
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        self.answer_lineEdit.setFont(font)
        self.answer_lineEdit.setObjectName("answer_lineEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 150, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        #---------------------------------------
        self.remaining_label = QtWidgets.QLabel(self.centralwidget)
        self.remaining_label.setGeometry(QtCore.QRect(150, 3, 100, 31))
        self.remaining_label.setFont(font)
        self.remaining_label.setText('Remaining: 0000')
        #---------------------------------------
        self.failed_label = QtWidgets.QLabel(self.centralwidget)
        self.failed_label.setGeometry(QtCore.QRect(10, 3, 80, 31))
        self.failed_label.setFont(font)
        self.failed_label.setText('Failed: 0000')
        #--------------------------------------------------------------
        self.next_Button = QtWidgets.QPushButton(self.centralwidget)
        self.next_Button.setGeometry(QtCore.QRect(180, 150, 51, 31))
        self.next_Button.setObjectName("next_Button")
        self.next_Button.clicked.connect(self.trainer_app.storeTrainingData)
        self.answer_lineEdit.returnPressed.connect(self.next_Button.click)
        #--------------------------------------------------------------
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "JCaptcha Trainer"))
        self.label_2.setText(_translate("MainWindow", "Answer:"))
        self.next_Button.setText(_translate("MainWindow", "Next"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, None)
    MainWindow.show()
    sys.exit(app.exec_())
