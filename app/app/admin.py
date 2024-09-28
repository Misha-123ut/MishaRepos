import requests
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QTableWidget, 
                               QPushButton, QLineEdit, QComboBox, QTableWidgetItem, QLabel)
from PySide6.QtCore import QTimer

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Администратор")
        layout = QVBoxLayout()

        # Вкладки
        self.tab_widget = QTabWidget()

        # Вкладка пользователей
        self.users_tab = QWidget()
        users_layout = QVBoxLayout()

        # Таблица пользователей
        self.user_table = QTableWidget(0, 3)  # Увеличиваем количество колонок на 3 (ID, Пользователь, Роль)
        self.user_table.setHorizontalHeaderLabels(["ID", "Пользователь", "Роль"])  # Заголовки столбцов
        users_layout.addWidget(self.user_table)

        # Поле для ввода имени пользователя
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите имя пользователя")
        users_layout.addWidget(self.username_input)

        # Выбор роли пользователя
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Официант", "Повар", "Администратор"])
        users_layout.addWidget(self.role_combo)

        # Кнопка для добавления пользователя
        self.add_user_btn = QPushButton("Добавить пользователя")
        users_layout.addWidget(self.add_user_btn)

        # Кнопка для увольнения пользователя
        self.fire_user_btn = QPushButton("Уволить пользователя")
        users_layout.addWidget(self.fire_user_btn)

        # Привязка кнопок к методам
        self.add_user_btn.clicked.connect(self.add_user)
        self.fire_user_btn.clicked.connect(self.fire_user)

        self.users_tab.setLayout(users_layout)
        self.tab_widget.addTab(self.users_tab, "Пользователи")

        # Вкладка заказов
        self.orders_tab = QWidget()
        orders_layout = QVBoxLayout()

        # Таблица заказов
        self.order_table = QTableWidget(0, 3)  # Увеличиваем количество колонок для статуса оплаты
        self.order_table.setHorizontalHeaderLabels(["Заказ", "Статус", "Оплачено"])  # Заголовки столбцов
        orders_layout.addWidget(self.order_table)

        self.orders_tab.setLayout(orders_layout)
        self.tab_widget.addTab(self.orders_tab, "Заказы")

        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        # Обновление таблицы пользователей и заказов при запуске
        self.update_user_table()
        self.update_order_table()

        # Таймер для автоматического обновления таблиц
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_order_table)
        self.timer.start(3000)  # Обновление каждые 3000 мс (3 секунды)

    def add_user(self):
        username = self.username_input.text()
        role = self.role_combo.currentText()

        if username:
            user_data = {
                "username": username,
                "role": role
            }
            response = requests.post('http://127.0.0.1:5000/users', json=user_data)
            if response.status_code == 201:
                self.update_user_table()  # Обновляем таблицу пользователей после добавления
                self.username_input.clear()  # Очищаем поле ввода после добавления пользователя
            else:
                print("Ошибка при добавлении пользователя")

    def fire_user(self):
        current_row = self.user_table.currentRow()
        if current_row == -1:
            return  # Если не выбран ни один пользователь

        user_id = self.user_table.item(current_row, 0).text()  # Предполагаем, что ID пользователя в первой колонке
        response = requests.delete(f'http://127.0.0.1:5000/users/{user_id}')

        if response.status_code == 200:
            self.update_user_table()  # Обновляем таблицу пользователей после увольнения

    def update_user_table(self):
        # Логика для обновления таблицы пользователей
        response = requests.get('http://127.0.0.1:5000/users')
        if response.status_code == 200:
            users = response.json()
            self.user_table.setRowCount(len(users))
            for row, user in enumerate(users):
                self.user_table.setItem(row, 0, QTableWidgetItem(str(user['id'])))  # ID пользователя
                self.user_table.setItem(row, 1, QTableWidgetItem(user['username']))  # Имя пользователя
                self.user_table.setItem(row, 2, QTableWidgetItem(user['role']))  # Роль пользователя

    def update_order_table(self):
        # Логика для обновления таблицы заказов
        response = requests.get('http://127.0.0.1:5000/orders')
        if response.status_code == 200:
            orders = response.json()
            self.order_table.setRowCount(len(orders))
            for row, order in enumerate(orders):
                self.order_table.setItem(row, 0, QTableWidgetItem(f"{order['table_number']} ({order['guests']} чел.)"))  # Заказ
                self.order_table.setItem(row, 1, QTableWidgetItem(order["status"]))  # Статус
                paid_status = "Да" if order["is_paid"] else "Нет"  # Оплачено или нет
                self.order_table.setItem(row, 2, QTableWidgetItem(paid_status))  # Отображаем статус оплаты
