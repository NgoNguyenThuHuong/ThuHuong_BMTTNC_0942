# -*- coding: utf-8 -*-

import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

# Thêm thư mục hiện tại vào sys.path để import local module
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from railfence_cipher import RailFenceCipher

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.cipher = RailFenceCipher()

        MainWindow.setObjectName("RailFenceCipher")
        MainWindow.resize(600, 450)
        MainWindow.setWindowTitle("Rail Fence Cipher")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Main Title Label
        self.lbl_title = QtWidgets.QLabel(self.centralwidget)
        self.lbl_title.setGeometry(QtCore.QRect(20, 20, 560, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.lbl_title.setFont(font)
        self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_title.setObjectName("lbl_title")

        # Plain Text Label and Box
        self.lbl_plain = QtWidgets.QLabel(self.centralwidget)
        self.lbl_plain.setGeometry(QtCore.QRect(30, 70, 100, 20))
        self.lbl_plain.setObjectName("lbl_plain")
        
        self.txt_plain = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_plain.setGeometry(QtCore.QRect(30, 95, 540, 80))
        self.txt_plain.setObjectName("txt_plain")

        # Key Label and Input
        self.lbl_key = QtWidgets.QLabel(self.centralwidget)
        self.lbl_key.setGeometry(QtCore.QRect(30, 190, 100, 20))
        self.lbl_key.setObjectName("lbl_key")

        self.spin_key = QtWidgets.QSpinBox(self.centralwidget)
        self.spin_key.setGeometry(QtCore.QRect(140, 185, 100, 30))
        self.spin_key.setMinimum(2)
        self.spin_key.setMaximum(100)
        self.spin_key.setProperty("value", 3)
        self.spin_key.setObjectName("spin_key")

        # Cipher Text Label and Box
        self.lbl_cipher = QtWidgets.QLabel(self.centralwidget)
        self.lbl_cipher.setGeometry(QtCore.QRect(30, 230, 100, 20))
        self.lbl_cipher.setObjectName("lbl_cipher")

        self.txt_cipher = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_cipher.setGeometry(QtCore.QRect(30, 255, 540, 80))
        self.txt_cipher.setObjectName("txt_cipher")

        # Action Buttons
        self.btn_encrypt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_encrypt.setGeometry(QtCore.QRect(60, 360, 120, 35))
        self.btn_encrypt.setObjectName("btn_encrypt")

        self.btn_decrypt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_decrypt.setGeometry(QtCore.QRect(240, 360, 120, 35))
        self.btn_decrypt.setObjectName("btn_decrypt")

        self.btn_clear = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clear.setGeometry(QtCore.QRect(420, 360, 120, 35))
        self.btn_clear.setObjectName("btn_clear")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        # Kết nối sự kiện của nút
        self.btn_encrypt.clicked.connect(self.handle_encrypt)
        self.btn_decrypt.clicked.connect(self.handle_decrypt)
        self.btn_clear.clicked.connect(self.handle_clear)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_title.setText(_translate("MainWindow", "RAIL FENCE CIPHER"))
        self.lbl_plain.setText(_translate("MainWindow", "Plain Text:"))
        self.lbl_key.setText(_translate("MainWindow", "Key (Rails):"))
        self.lbl_cipher.setText(_translate("MainWindow", "Cipher Text:"))
        self.btn_encrypt.setText(_translate("MainWindow", "Encrypt (Mã hóa)"))
        self.btn_decrypt.setText(_translate("MainWindow", "Decrypt (Giải mã)"))
        self.btn_clear.setText(_translate("MainWindow", "Clear (Xóa)"))

    def handle_encrypt(self):
        plain_text = self.txt_plain.toPlainText()
        if not plain_text:
            QMessageBox.warning(None, "Cảnh báo", "Vui lòng nhập Plain Text để mã hóa!")
            return
        
        num_rails = self.spin_key.value()
        try:
            cipher_text = self.cipher.rail_fence_encrypt(plain_text, num_rails)
            self.txt_cipher.setPlainText(cipher_text)
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Có lỗi xảy ra: {str(e)}")

    def handle_decrypt(self):
        cipher_text = self.txt_cipher.toPlainText()
        if not cipher_text:
            QMessageBox.warning(None, "Cảnh báo", "Vui lòng nhập Cipher Text để giải mã!")
            return
        
        num_rails = self.spin_key.value()
        try:
            plain_text = self.cipher.rail_fence_decrypt(cipher_text, num_rails)
            self.txt_plain.setPlainText(plain_text)
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Có lỗi xảy ra: {str(e)}")

    def handle_clear(self):
        self.txt_plain.clear()
        self.txt_cipher.clear()
        self.spin_key.setValue(3)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
