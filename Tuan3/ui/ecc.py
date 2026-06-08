# -*- coding: utf-8 -*-

import sys
import os

from PyQt5 import QtCore, QtWidgets

ROOT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from cipher.ecc.ecc_cipher import ECCCipher


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        self.ecc = ECCCipher()

        MainWindow.setObjectName("ECC Cipher")
        MainWindow.resize(522, 328)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 10, 100, 20))

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 80, 20))

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 150, 80, 20))

        self.btn_gen_keys = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gen_keys.setGeometry(QtCore.QRect(344, 10, 120, 25))

        self.btn_sign = QtWidgets.QPushButton(self.centralwidget)
        self.btn_sign.setGeometry(QtCore.QRect(140, 240, 75, 25))

        self.btn_verify = QtWidgets.QPushButton(self.centralwidget)
        self.btn_verify.setGeometry(QtCore.QRect(300, 240, 75, 25))

        self.txt_info = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_info.setGeometry(QtCore.QRect(100, 50, 351, 81))

        self.txt_sign = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_sign.setGeometry(QtCore.QRect(100, 150, 351, 81))

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        # Kết nối sự kiện nút
        self.btn_gen_keys.clicked.connect(self.generate_keys)
        self.btn_sign.clicked.connect(self.sign_message)
        self.btn_verify.clicked.connect(self.verify_signature)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def generate_keys(self):

        self.ecc.generate_keys()

        QtWidgets.QMessageBox.information(
            None,
            "ECC",
            "Generate Keys Success"
        )

    def sign_message(self):

        try:
            keys = self.ecc.load_keys()

            message = self.txt_info.toPlainText()

            if not message:
                QtWidgets.QMessageBox.warning(
                    None,
                    "ECC",
                    "Please enter information"
                )
                return

            signature = self.ecc.sign(
                message,
                keys["private_key"]
            )

            self.txt_sign.setPlainText(
                signature.hex()
            )

            QtWidgets.QMessageBox.information(
                None,
                "ECC",
                "Sign Success"
            )

        except Exception as e:

            QtWidgets.QMessageBox.critical(
                None,
                "Error",
                str(e)
            )

    def verify_signature(self):

        try:
            keys = self.ecc.load_keys()

            message = self.txt_info.toPlainText()

            signature_hex = self.txt_sign.toPlainText()

            if not signature_hex:
                QtWidgets.QMessageBox.warning(
                    None,
                    "ECC",
                    "Signature is empty"
                )
                return

            signature = bytes.fromhex(signature_hex)

            result = self.ecc.verify(
                message,
                signature,
                keys["public_key"]
            )

            if result:
                QtWidgets.QMessageBox.information(
                    None,
                    "ECC",
                    "Verify Success"
                )
            else:
                QtWidgets.QMessageBox.warning(
                    None,
                    "ECC",
                    "Verify Failed"
                )

        except Exception as e:

            QtWidgets.QMessageBox.critical(
                None,
                "Error",
                str(e)
            )

    def retranslateUi(self, MainWindow):

        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(
            _translate("MainWindow", "ECC Cipher")
        )

        self.label.setText(
            _translate("MainWindow", "ECC CIPHER")
        )

        self.label_2.setText(
            _translate("MainWindow", "Information")
        )

        self.label_3.setText(
            _translate("MainWindow", "Signature")
        )

        self.btn_gen_keys.setText(
            _translate("MainWindow", "Generate Keys")
        )

        self.btn_sign.setText(
            _translate("MainWindow", "Sign")
        )

        self.btn_verify.setText(
            _translate("MainWindow", "Verify")
        )


if __name__ == "__main__":

    import sys

    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()

    sys.exit(app.exec_())