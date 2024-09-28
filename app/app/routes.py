from flask import Blueprint, jsonify, request
from .models import Session, Order, User  # Импортируем модели Order и User

app = Blueprint('app', __name__)

@app.route('/orders', methods=['GET'])
def get_orders():
    session = Session()
    orders = session.query(Order).all()
    session.close()
    return jsonify([{
        'id': order.id,
        'table_number': order.table_number,
        'guests': order.guests,
        'dishes': order.dishes.split(','),
        'status': order.status,
        'is_paid': order.is_paid  # Добавляем статус оплаты
    } for order in orders])


# Маршрут для создания нового заказа
@app.route('/orders', methods=['POST'])
def create_order():
    session = Session()
    data = request.json
    order = Order(
        table_number=data['table_number'],
        guests=data['guests'],
        dishes=','.join(data['dishes'])
    )
    session.add(order)
    session.commit()
    session.close()
    return jsonify({'id': order.id}), 201

@app.route('/users', methods=['POST'])
def create_user():
    session = Session()
    data = request.json
    user = User(
        username=data['username'],
        role=data['role']
    )
    session.add(user)
    session.commit()  # Фиксируем изменения в базе данных

    user_id = user.id  # Получаем ID пользователя до закрытия сессии
    session.close()  # Закрываем сессию

    return jsonify({'id': user_id}), 201  # Возвращаем ID после закрытия сессии


# Маршрут для получения всех пользователей
@app.route('/users', methods=['GET'])
def get_users():
    session = Session()
    users = session.query(User).all()
    session.close()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'role': user.role
    } for user in users])


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()

    if not user:
        session.close()
        return jsonify({"error": "User not found"}), 404

    # Удаляем пользователя
    session.delete(user)
    session.commit()
    session.close()

    return jsonify({"message": "User deleted"}), 200

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    session = Session()
    order = session.query(Order).filter_by(id=order_id).first()

    if not order:
        session.close()
        return jsonify({"error": "Order not found"}), 404

    data = request.json
    order.status = data.get('status', order.status)  # Обновляем статус заказа
    session.commit()
    session.close()

    return jsonify({"message": "Order updated"}), 200


@app.route('/orders/<int:order_id>/paid', methods=['PUT'])
def mark_order_paid(order_id):
    session = Session()
    order = session.query(Order).filter_by(id=order_id).first()

    if not order:
        session.close()
        return jsonify({"error": "Order not found"}), 404

    order.is_paid = True  # Меняем статус на "оплачен"
    session.commit()
    session.close()

    return jsonify({"message": "Order marked as paid"}), 200
