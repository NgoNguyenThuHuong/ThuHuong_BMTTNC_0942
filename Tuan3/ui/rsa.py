# -*- coding: utf-8 -*-

import os
import sys
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

# Cấu hình môi trường hiển thị hệ thống
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "../platforms"

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("RSACipher")
        MainWindow.resize(800, 389)
        
        # Đổi tên tiêu đề hiển thị cửa sổ ứng dụng thành RSA Cipher
        MainWindow.setWindowTitle("RSA Cipher")
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.txt_encrypt = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_encrypt.setGeometry(QtCore.QRect(100, 80, 231, 81))
        self.txt_encrypt.setObjectName("txt_encrypt")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(350, 20, 71, 16))
        self.label.setObjectName("label")
        
        self.btn_encrypt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_encrypt.setGeometry(QtCore.QRect(130, 310, 75, 23))
        self.btn_encrypt.setObjectName("btn_encrypt")
        
        self.btn_decrypt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_decrypt.setGeometry(QtCore.QRect(220, 310, 75, 23))
        self.btn_decrypt.setObjectName("btn_decrypt")
        
        self.btn_sign = QtWidgets.QPushButton(self.centralwidget)
        self.btn_sign.setGeometry(QtCore.QRect(480, 310, 75, 23))
        self.btn_sign.setObjectName("btn_sign")
        
        self.btn_verify = QtWidgets.QPushButton(self.centralwidget)
        self.btn_verify.setGeometry(QtCore.QRect(570, 310, 75, 23))
        self.btn_verify.setObjectName("btn_verify")
        
        self.txt_decrypt = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_decrypt.setGeometry(QtCore.QRect(100, 190, 231, 81))
        self.txt_decrypt.setObjectName("txt_decrypt")
        
        self.txt_info = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_info.setGeometry(QtCore.QRect(450, 80, 231, 81))
        self.txt_info.setObjectName("txt_info")
        
        self.txt_sign = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_sign.setGeometry(QtCore.QRect(450, 190, 231, 81))
        self.txt_sign.setObjectName("txt_sign")
        
        self.btn_gen_keys = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gen_keys.setGeometry(QtCore.QRect(430, 20, 81, 23))
        self.btn_gen_keys.setObjectName("btn_gen_keys")
        
        # Tạo thêm các nhãn text bị thiếu để hiển thị lên màn hình
        self.lbl_plain = QtWidgets.QLabel(self.centralwidget)
        self.lbl_plain.setGeometry(QtCore.QRect(20, 80, 70, 20))
        self.lbl_plain.setText("Plain Text")
        
        self.lbl_cipher = QtWidgets.QLabel(self.centralwidget)
        self.lbl_cipher.setGeometry(QtCore.QRect(20, 190, 70, 20))
        self.lbl_cipher.setText("Cipher Text")
        
        self.lbl_info = QtWidgets.QLabel(self.centralwidget)
        self.lbl_info.setGeometry(QtCore.QRect(370, 80, 70, 20))
        self.lbl_info.setText("Information")
        
        self.lbl_signature = QtWidgets.QLabel(self.centralwidget)
        self.lbl_signature.setGeometry(QtCore.QRect(370, 190, 70, 20))
        self.lbl_signature.setText("Signature")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # Kết nối API URL hệ thống
        self.API_URL = "http://127.0.0.1:5000/api/rsa"
        self.init_logic()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "RSA CIPHER"))
        self.btn_encrypt.setText(_translate("MainWindow", "Encrypt"))
        self.btn_decrypt.setText(_translate("MainWindow", "Decrypt"))
        self.btn_sign.setText(_translate("MainWindow", "Sign"))
        self.btn_verify.setText(_translate("MainWindow", "Verify"))
        self.btn_gen_keys.setText(_translate("MainWindow", "Generate Keys"))

    # ==================== LOGIC KẾT NỐI API FLASK ====================
    def init_logic(self):
        self.btn_gen_keys.clicked.connect(self.handle_generate_keys)
        self.btn_encrypt.clicked.connect(self.handle_encrypt)
        self.btn_decrypt.clicked.connect(self.handle_decrypt)
        self.btn_sign.clicked.connect(self.handle_sign)
        self.btn_verify.clicked.connect(self.handle_verify)

    def handle_generate_keys(self):
        try:
            response = requests.get(f"{self.API_URL}/generate_keys")
            if response.status_code == 200:
                self.txt_info.setText(response.json().get("message", "Keys generated!"))
                QMessageBox.information(None, "Thông báo", "Sinh cặp khóa RSA thành công!")
        except Exception:
            QMessageBox.critical(None, "Lỗi kết nối", "Vui lòng khởi động file api.py trước!")

    def handle_encrypt(self):
        message = self.txt_encrypt.toPlainText()
        if not message: return
        try:
            response = requests.post(f"{self.API_URL}/encrypt", json={"message": message, "key_type": "public"})
            if response.status_code == 200:
                self.txt_decrypt.setText(response.json().get("encrypted_message", ""))
                self.txt_info.setText("Mã hóa thông điệp thành công.")
        except Exception as e:
            self.txt_info.setText(str(e))

    def handle_decrypt(self):
        ciphertext = self.txt_decrypt.toPlainText().strip()
        if not ciphertext: return
        try:
            response = requests.post(f"{self.API_URL}/decrypt", json={"ciphertext": ciphertext, "key_type": "private"})
            if response.status_code == 200:
                self.txt_encrypt.setText(response.json().get("decrypted_message", ""))
                self.txt_info.setText("Giải mã dữ liệu thành công.")
        except Exception as e:
            self.txt_info.setText(str(e))

    def handle_sign(self):
        message = self.txt_encrypt.toPlainText()
        if not message: return
        try:
            response = requests.post(f"{self.API_URL}/sign", json={"message": message})
            if response.status_code == 200:
                self.txt_sign.setText(response.json().get("signature", ""))
                self.txt_info.setText("Tạo chữ ký số (Signature) thành công.")
        except Exception as e:
            self.txt_info.setText(str(e))

    def handle_verify(self):
        message = self.txt_encrypt.toPlainText()
        signature = self.txt_sign.toPlainText().strip()
        if not message or not signature: return
        try:
            response = requests.post(f"{self.API_URL}/verify", json={"message": message, "signature": signature})
            if response.status_code == 200:
                if response.json().get("is_verified", False):
                    self.txt_info.setText("Kết quả xác thực: CHỮ KÝ HỢP LỆ!")
                    QMessageBox.information(None, "Thành công", "Chữ ký hợp lệ!")
                else:
                    self.txt_info.setText("Cảnh báo: Chữ ký KHÔNG hợp lệ!")
                    QMessageBox.warning(None, "Thất bại", "Chữ ký không hợp lệ!")
        except Exception as e:
            self.txt_info.setText(str(e))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())