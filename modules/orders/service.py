from core.database import get_db
from core.models import Order, User, OrderStatus
from .schemas import OrderCreate
from modules.payments import service as payments
from datetime import datetime

async def create_order(db, order_data: OrderCreate):
    # Проверка депозита для крупных заказов
    requires_deposit = order_data.budget > 20000
    deposit_id = None
    
    if requires_deposit:
        user = await db.get(User, order_data.customer_id)
        if not user.deposit_paid:
            # Требуем внести депозит
            deposit_id = await payments.process_deposit(user.id, 1000)
    
    # Создание объекта заказа
    order = Order(
        customer_id=order_data.customer_id,
        work_type=order_data.work_type,
        budget=order_data.budget,
        workers_needed=order_data.workers_needed,
        location=order_data.location,
        photos=order_data.photos,
        requires_deposit=requires_deposit,
        deposit_id=deposit_id,
        status=OrderStatus.ACTIVE if not requires_deposit else OrderStatus.DRAFT
    )
    
    db.add(order)
    await db.commit()
    await db.refresh(order)
    
    # Генерация договора
    if not requires_deposit:
        await generate_contract(order)
    
    return order

async def generate_contract(order):
    # Заглушка для реальной генерации договора
    contract_data = f"""
    Договор №{order.id}
    Дата: {datetime.now().strftime("%d.%m.%Y")}
    Заказчик: {order.customer_id}
    Тип работ: {order.work_type}
    Бюджет: {order.budget} шекелей
    """
    return contract_data
