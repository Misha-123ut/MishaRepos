import requests
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem
from PySide6.QtCore import QTimer

class ChefWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Повар")
        layout = QVBoxLayout()

        # Таблица текущих заказов
        self.order_table = QTableWidget(0, 2)
        self.order_table.setHorizontalHeaderLabels(["ID", "Статус"])  # Предполагаем, что ID заказа в первой колонке
        layout.addWidget(self.order_table)

        # Кнопки для изменения статуса заказа
        self.mark_cooking_btn = QPushButton("Готовится")
        self.mark_ready_btn = QPushButton("Готово")
        layout.addWidget(self.mark_cooking_btn)
        layout.addWidget(self.mark_ready_btn)

        # Привязка кнопок к методам обновления статуса
        self.mark_cooking_btn.clicked.connect(lambda: self.update_order_status('Готовится'))
        self.mark_ready_btn.clicked.connect(lambda: self.update_order_status('Готово'))

        self.setLayout(layout)

        self.update_order_table()

        # Таймер для автоматического обновления таблиц
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_order_table)
        self.timer.start(3000)  # Обновление каждые 3000 мс (3 секунды)

    def update_order_status(self, status):
        # Получаем текущий выбранный заказ
        current_row = self.order_table.currentRow()
        if current_row == -1:
            return  # Ничего не выбрано

        order_id = self.order_table.item(current_row, 0).text()  # Предполагаем, что ID заказа в первой колонке
        response = requests.put(f'http://127.0.0.1:5000/orders/{order_id}', json={'status': status})
        
        if response.status_code == 200:
            self.update_order_table()  # Обновляем таблицу после изменения статуса

    def update_order_table(self):
        # Обновляем таблицу текущих заказов
        response = requests.get('http://127.0.0.1:5000/orders')
        if response.status_code == 200:
            orders = response.json()
            self.order_table.setRowCount(len(orders))
            for row, order in enumerate(orders):
                self.order_table.setItem(row, 0, QTableWidgetItem(str(order['id'])))  # ID заказа
                self.order_table.setItem(row, 1, QTableWidgetItem(order['status']))    # Статус заказа
