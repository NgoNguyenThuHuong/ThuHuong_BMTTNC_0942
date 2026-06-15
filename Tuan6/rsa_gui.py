# -*- coding: utf-8 -*-

import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

# Thêm thư mục hiện tại vào sys.path để import local module
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from rsa_cipher import RSACipher

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Đảm bảo lưu và tải khóa từ thư mục Tuan6
        self.cipher = RSACipher(key_dir=current_dir)

        MainWindow.setObjectName("RSACipher")
        MainWindow.resize(800, 389)
        MainWindow.setWindowTitle("RSA Cipher")
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Ô nhập Plain Text
        self.txt_encrypt = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_encrypt.setGeometry(QtCore.QRect(100, 80, 231, 81))
        self.txt_encrypt.setObjectName("txt_encrypt")
        
        # Tiêu đề ứng dụng
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(350, 20, 71, 16))
        font = QtGui.QFont()
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        # Các nút Encrypt và Decrypt
        self.btn_encrypt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_encrypt.setGeometry(QtCore.QRect(130, 310, 75, 23))
        self.btn_encrypt.setObjectName("btn_encrypt")
        
        self.btn_decrypt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_decrypt.setGeometry(QtCore.QRect(220, 310, 75, 23))
        self.btn_decrypt.setObjectName("btn_decrypt")
        
        # Các nút Sign và Verify
        self.btn_sign = QtWidgets.QPushButton(self.centralwidget)
        self.btn_sign.setGeometry(QtCore.QRect(480, 310, 75, 23))
        self.btn_sign.setObjectName("btn_sign")
        
        self.btn_verify = QtWidgets.QPushButton(self.centralwidget)
        self.btn_verify.setGeometry(QtCore.QRect(570, 310, 75, 23))
        self.btn_verify.setObjectName("btn_verify")
        
        # Ô nhập Cipher Text
        self.txt_decrypt = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_decrypt.setGeometry(QtCore.QRect(100, 190, 231, 81))
        self.txt_decrypt.setObjectName("txt_decrypt")
        
        # Ô nhập/Hiển thị Information
        self.txt_info = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_info.setGeometry(QtCore.QRect(450, 80, 231, 81))
        self.txt_info.setObjectName("txt_info")
        
        # Ô nhập/Hiển thị Signature
        self.txt_sign = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_sign.setGeometry(QtCore.QRect(450, 190, 231, 81))
        self.txt_sign.setObjectName("txt_sign")
        
        # Nút sinh khóa
        self.btn_gen_keys = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gen_keys.setGeometry(QtCore.QRect(430, 20, 95, 23))
        self.btn_gen_keys.setObjectName("btn_gen_keys")
        
        # Các nhãn text
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
        
        # Kết nối sự kiện của các nút
        self.btn_gen_keys.clicked.connect(self.handle_generate_keys)
        self.btn_encrypt.clicked.connect(self.handle_encrypt)
        self.btn_decrypt.clicked.connect(self.handle_decrypt)
        self.btn_sign.clicked.connect(self.handle_sign)
        self.btn_verify.clicked.connect(self.handle_verify)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "RSA CIPHER"))
        self.btn_encrypt.setText(_translate("MainWindow", "Encrypt"))
        self.btn_decrypt.setText(_translate("MainWindow", "Decrypt"))
        self.btn_sign.setText(_translate("MainWindow", "Sign"))
        self.btn_verify.setText(_translate("MainWindow", "Verify"))
        self.btn_gen_keys.setText(_translate("MainWindow", "Generate Keys"))

    # ==================== LOGIC XỬ LÝ SỰ KIỆN MÃ HÓA / GIẢI MÃ / KÝ SỐ LOCAL ====================
    def handle_generate_keys(self):
        try:
            self.cipher.generate_keys()
            self.txt_info.setText("Sinh cặp khóa RSA thành công và đã lưu tại Tuan6/public.pem & private.pem")
            QMessageBox.information(None, "Thông báo", "Sinh cặp khóa RSA thành công!")
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Không thể sinh cặp khóa: {str(e)}")

    def handle_encrypt(self):
        message = self.txt_encrypt.toPlainText()
        if not message: 
            QMessageBox.warning(None, "Cảnh báo", "Vui lòng nhập Plain Text để mã hóa!")
            return
        try:
            # Tải khóa (nếu chưa có thì hàm tự động sinh khóa)
            private_key, public_key = self.cipher.load_keys()
            ciphertext = self.cipher.encrypt(message, public_key)
            self.txt_decrypt.setText(ciphertext.hex())
            self.txt_info.setText("Mã hóa thông điệp thành công.")
        except Exception as e:
            self.txt_info.setText(f"Lỗi mã hóa: {str(e)}")
            QMessageBox.critical(None, "Lỗi", f"Có lỗi xảy ra: {str(e)}")

    def handle_decrypt(self):
        ciphertext_hex = self.txt_decrypt.toPlainText().strip()
        if not ciphertext_hex:
            QMessageBox.warning(None, "Cảnh báo", "Vui lòng nhập Cipher Text dưới dạng Hex để giải mã!")
            return
        try:
            private_key, public_key = self.cipher.load_keys()
            ciphertext = bytes.fromhex(ciphertext_hex)
            decrypted_bytes = self.cipher.decrypt(ciphertext, private_key)
            self.txt_encrypt.setText(decrypted_bytes.decode('utf-8'))
            self.txt_info.setText("Giải mã dữ liệu thành công.")
        except Exception as e:
            self.txt_info.setText(f"Lỗi giải mã: {str(e)}")
            QMessageBox.critical(None, "Lỗi", f"Giải mã thất bại. Vui lòng kiểm tra lại bản mã Hex hoặc khóa.")

    def handle_sign(self):
        message = self.txt_encrypt.toPlainText()
        if not message:
            QMessageBox.warning(None, "Cảnh báo", "Vui lòng nhập dữ liệu vào ô Plain Text để thực hiện ký!")
            return
        try:
            private_key, public_key = self.cipher.load_keys()
            signature = self.cipher.sign(message, private_key)
            self.txt_sign.setText(signature.hex())
            self.txt_info.setText("Tạo chữ ký số (Signature) thành công.")
        except Exception as e:
            self.txt_info.setText(f"Lỗi tạo chữ ký: {str(e)}")
            QMessageBox.critical(None, "Lỗi", f"Có lỗi xảy ra: {str(e)}")

    def handle_verify(self):
        message = self.txt_encrypt.toPlainText()
        signature_hex = self.txt_sign.toPlainText().strip()
        if not message or not signature_hex:
            QMessageBox.warning(None, "Cảnh báo", "Vui lòng nhập đầy đủ Plain Text và Signature để xác thực!")
            return
        try:
            private_key, public_key = self.cipher.load_keys()
            signature = bytes.fromhex(signature_hex)
            is_verified = self.cipher.verify(message, signature, public_key)
            if is_verified:
                self.txt_info.setText("Kết quả xác thực: CHỮ KÝ HỢP LỆ!")
                QMessageBox.information(None, "Thành công", "Chữ ký hợp lệ!")
            else:
                self.txt_info.setText("Cảnh báo: Chữ ký KHÔNG hợp lệ!")
                QMessageBox.warning(None, "Thất bại", "Chữ ký không hợp lệ!")
        except Exception as e:
            self.txt_info.setText(f"Lỗi xác thực: {str(e)}")
            QMessageBox.critical(None, "Lỗi", f"Có lỗi xảy ra trong quá trình xác thực: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
