import sys
import subprocess
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
)

class AuthWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setGeometry(100, 100, 300, 200)
        self.setMaximumSize(400, 300) 

        self.username_label = QLabel("Имя пользователя:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.open_explorer)  
        self.close_button = QPushButton("Закрыть")
        self.close_button.clicked.connect(self.close_application) 
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.close_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setStyleSheet("background-color: lightblue;")

    def open_explorer(self):
        subprocess.run("explorer", shell=True)

    def close_application(self):
        QMessageBox.warning(self, "Ошибка", "Мойша ЛОХ.")

    def closeEvent(self, event):
        event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())
