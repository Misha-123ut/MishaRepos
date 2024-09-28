import requests
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGroupBox,
                               QComboBox, QSpinBox, QLineEdit, QListWidget, 
                               QPushButton, QTableWidget, QLabel, QTableWidgetItem)
from PySide6.QtCore import QTimer

class WaiterWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Официант")
        layout = QVBoxLayout()

        new_order_group = QGroupBox("Создание нового заказа")
        new_order_layout = QVBoxLayout()

        self.table_combo = QComboBox()
        self.table_combo.addItems(["Стол 1", "Стол 2", "Стол 3"])
        new_order_layout.addWidget(QLabel("Выберите столик"))
        new_order_layout.addWidget(self.table_combo)

        self.guest_spin = QSpinBox()
        self.guest_spin.setRange(1, 10)
        new_order_layout.addWidget(QLabel("Количество гостей"))
        new_order_layout.addWidget(self.guest_spin)

        self.dish_input = QLineEdit()
        self.dish_input.setPlaceholderText("Название блюда")
        new_order_layout.addWidget(self.dish_input)

        self.add_dish_btn = QPushButton("Добавить блюдо")
        new_order_layout.addWidget(self.add_dish_btn)

        self.dish_list = QListWidget()
        new_order_layout.addWidget(self.dish_list)

        self.add_dish_btn.clicked.connect(self.add_dish)

        self.create_order_btn = QPushButton("Создать заказ")
        self.clear_form_btn = QPushButton("Очистить форму")
        new_order_layout.addWidget(self.create_order_btn)
        new_order_layout.addWidget(self.clear_form_btn)

        self.create_order_btn.clicked.connect(self.create_order)
        self.clear_form_btn.clicked.connect(self.clear_form)

        new_order_group.setLayout(new_order_layout)
        layout.addWidget(new_order_group)

        # Таблица текущих заказов
        self.order_table = QTableWidget(0, 3)  # Увеличиваем количество колонок
        self.order_table.setHorizontalHeaderLabels(["Заказ", "Статус", "Оплачено"])  # Добавляем заголовок "Оплачено"
        layout.addWidget(self.order_table)

        # Кнопка для отметки заказа как оплаченного
        self.mark_paid_btn = QPushButton("Оплачено")
        layout.addWidget(self.mark_paid_btn)
        self.mark_paid_btn.clicked.connect(self.mark_order_paid)

        self.setLayout(layout)

        self.orders = []  # Хранилище для заказов
        self.update_order_table()  # Обновляем таблицу сразу при инициализации

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_order_table)
        self.timer.start(3000)  # Обновление каждые 3000 мс (3 секунды)

    def add_dish(self):
        dish_name = self.dish_input.text()
        if dish_name:
            self.dish_list.addItem(dish_name)
            self.dish_input.clear()

    def create_order(self):
        table = self.table_combo.currentText()
        guests = self.guest_spin.value()
        dishes = [self.dish_list.item(i).text() for i in range(self.dish_list.count())]

        if dishes:
            order_data = {
                "table_number": table,
                "guests": guests,
                "dishes": dishes
            }
            response = requests.post('http://127.0.0.1:5000/orders', json=order_data)
            if response.status_code == 201:
                self.update_order_table()  # Обновляем таблицу после создания заказа
                self.clear_form()

    def update_order_table(self):
        response = requests.get('http://127.0.0.1:5000/orders')
        if response.status_code == 200:
            self.orders = response.json()
            self.order_table.setRowCount(len(self.orders))
            for row, order in enumerate(self.orders):
                self.order_table.setItem(row, 0, QTableWidgetItem(f"{order['table_number']} ({order['guests']} чел.)"))
                self.order_table.setItem(row, 1, QTableWidgetItem(order["status"]))
                # Добавляем статус оплаты
                paid_status = "Да" if order["is_paid"] else "Нет"
                self.order_table.setItem(row, 2, QTableWidgetItem(paid_status))  # Отображаем статус оплаты

    def mark_order_paid(self):
        current_row = self.order_table.currentRow()
        if current_row == -1:
            return  # Если ничего не выбрано

        order_id = self.orders[current_row]['id']  # Получаем ID заказа
        response = requests.put(f'http://127.0.0.1:5000/orders/{order_id}/paid', json={})
        
        if response.status_code == 200:
            self.update_order_table()  # Обновляем таблицу после изменения статуса

    def clear_form(self):
        self.table_combo.setCurrentIndex(0)
        self.guest_spin.setValue(1)
        self.dish_list.clear()
