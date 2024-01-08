################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
## This project can be used freely for all uses, as long as they maintain the
## respective credits only in the Python scripts, any information in the visual
## interface (GUI) can be modified without any implication.
##
## There are limitations on Qt licenses if you want to use your products
## commercially, I recommend reading them on the official website:
## https://doc.qt.io/qtforpython/licenses.html
##
################################################################################

import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeyEvent, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from ui_Formlogin import Login
# GUI FILE
from main_window import VideoWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Login()
        self.ui.setupUi(self)
        icon = QIcon()
        icon.addFile(r"icons\Video_icon-icons.com_76525.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        # REMOVE TITLE BAR
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # CREATE DROP SHADOW EFFECT
        self.shadow = self.set_drop_shadow()

        # SET DROP SHADOW EFFECT IN FRAME
        self.ui.frame_Shadow.setGraphicsEffect(self.shadow)

        # SET FUNCTION CLICK IN BUTTONS
        self.ui.pushButton_Exit.clicked.connect(self.click_exit)
        self.ui.pushButton_Login.clicked.connect(self.click_login)

        # ENABLE MODE PASSWORD IN LINE EDIT
        self.ui.lineEdit_Password.setEchoMode(QLineEdit.Password)

        # SET MOVE WINDOW
        def move_window(event):
            # IF LEFT CLICK MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.drag_pos)
                self.drag_pos = event.globalPos()
                event.accept()

        # ENABLE MOUSE MOVE FORM
        self.ui.frame_TopBar.mouseMoveEvent = move_window
        self.ui.frame_Shadow.mouseMoveEvent = move_window
        
        # SHOW FORM
        self.show()
        
    def set_drop_shadow(self):
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        return self.shadow

    def click_exit(self):
        print("click button close")
        self.close()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.click_login()
    def click_login(self):
        print("click button login")
        user = self.ui.lineEdit_Login.text()
        password = self.ui.lineEdit_Password.text()
        if user == "admin" and password == "admin":
            # Hide login
                self.close()
                camera_dialog = CameraDialog()
                result = camera_dialog.exec_()

                if result == QDialog.Accepted:
                    camera_count = camera_dialog.get_camera_count()
                    if camera_count > 10:
                        QMessageBox.warning(self, "Thông báo", f"Số lượng màn hình vượt mức", QMessageBox.Ok)
                    else:
                        window = VideoWindow(camera_count)
                        window.show()
                        print(f"Số lượng camera: {camera_count}")
                        camera_dialog.close()
                else:
                    print("Đã cancel")
        else:
            QMessageBox.warning(self, "Lỗi đăng nhập", f"Sai mật khẩu", QMessageBox.Ok)
     
        

    def mousePressEvent(self, event):
        self.drag_pos = event.globalPos()

class CameraDialog(QDialog):
    def __init__(self, parent=None):
        super(CameraDialog, self).__init__(parent)
        self.setObjectName(u"dialog_main")
        self.setFixedSize(500, 200)
        self.setWindowTitle("Sô lượng màn hình")
        icon = QIcon()
        icon.addFile(r"icons\Video_icon-icons.com_76525.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        # Tạo các widget
        self.label = QLabel("Số lượng màn hình:")
        self.line_edit = QLineEdit(self)
        self.line_edit.setStyleSheet(u"QLineEdit {\n"
            "	background-color: rgb(27, 29, 35);\n"
            "	border-radius: 5px;\n"
            "	border: 2px solid rgb(27, 29, 35);\n"
            "	padding-left: 10px;\n"
            "	color: rgb(255, 255, 255);\n"
            "}\n"
            "QLineEdit:hover {\n"
            "	border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QLineEdit:focus {\n"
            "	border: 2px solid rgb(91, 101, 124);\n"
            "}")
        self.line_edit.setValidator(QtGui.QIntValidator())  # Đảm bảo chỉ nhập số
        self.line_edit.setPlaceholderText("Nhập số lượng màn hình")
        self.line_edit.setFixedHeight(50)
        self.layout_control = QHBoxLayout()
        self.ok_button = QPushButton("OK", self)
        self.ok_button.setStyleSheet(u"QPushButton {\n"
        "    border: 2px solid rgb(27, 29, 35);\n"
        "    border-radius: 5px;\n"
        "    background-color: rgb(27, 29, 35);\n"
        "    color: white; /* Set text color to white */\n"
        "}\n"
        "QPushButton:hover {\n"
        "    background-color: rgb(57, 65, 80);\n"
        "    border: 2px solid rgb(61, 70, 86);\n"
        "}\n"
        "QPushButton:pressed {\n"
        "    background-color: rgb(35, 40, 49);\n"
        "    border: 2px solid rgb(43, 50, 61);\n"
        "}")
        self.layout_control.addWidget(self.ok_button)
        self.ok_button.setFixedSize(100, 50)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setStyleSheet(u"QPushButton {\n"
        "    border: 2px solid rgb(27, 29, 35);\n"
        "    border-radius: 5px;\n"
        "    background-color: rgb(27, 29, 35);\n"
        "    color: white; /* Set text color to white */\n"
        "}\n"
        "QPushButton:hover {\n"
        "    background-color: rgb(57, 65, 80);\n"
        "    border: 2px solid rgb(61, 70, 86);\n"
        "}\n"
        "QPushButton:pressed {\n"
        "    background-color: rgb(35, 40, 49);\n"
        "    border: 2px solid rgb(43, 50, 61);\n"
        "}")
        self.layout_control.addWidget(self.cancel_button)
        self.cancel_button.setFixedSize(100, 50)
        # Bố trí các widget trong QVBoxLayout
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addLayout(self.layout_control)

        # Kết nối sự kiện click của nút OK và Cancel
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_camera_count(self):
        return int(self.line_edit.text())
        
def init_app():
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    init_app()
    