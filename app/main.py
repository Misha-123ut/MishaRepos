from PySide6.QtWidgets import QApplication
from app.waiter import WaiterWindow  # Используем абсолютный импорт
from app.chef import ChefWindow       # Используем абсолютный импорт
from app.admin import AdminWindow     # Используем абсолютный импорт
from threading import Thread
from app.run import create_app       # Импортируем create_app из run.py

if __name__ == "__main__":
    app = QApplication([])

    # Создаем экземпляры интерфейсов
    waiter_window = WaiterWindow()
    chef_window = ChefWindow()  # Передаем список заказов
    admin_window = AdminWindow()  # Передаем waiter_window для доступа к заказам

    # Запускаем интерфейсы
    waiter_window.show()
    chef_window.show()
    admin_window.show()

    # Запуск Flask в отдельном потоке
    def run_flask():
        create_app().run(debug=True, use_reloader=False)  # Используем create_app для запуска Flask

    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    app.exec()
