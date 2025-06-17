from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from modules.orders import service as order_service
from modules.orders import schemas as order_schemas
from core.database import get_db

class OrderCreationStates(StatesGroup):
    WORK_TYPE = State()
    BUDGET = State()
    WORKERS_NEEDED = State()
    LOCATION = State()
    PHOTOS = State()

async def start_order_creation(message: types.Message):
    await message.answer("Создание нового заказа. Выберите тип работ:", 
                         reply_markup=get_work_types_keyboard())
    await OrderCreationStates.WORK_TYPE.set()

async def handle_work_type(callback: types.CallbackQuery, state: FSMContext):
    work_type = callback.data.split(":")[1]
    await state.update_data(work_type=work_type)
    await callback.message.answer("Укажите бюджет заказа в шекелях:")
    await OrderCreationStates.BUDGET.set()

async def handle_budget(message: types.Message, state: FSMContext):
    try:
        budget = float(message.text)
        if budget <= 0:
            raise ValueError
        await state.update_data(budget=budget)
        await message.answer("Сколько рабочих требуется?")
        await OrderCreationStates.WORKERS_NEEDED.set()
    except ValueError:
        await message.answer("Неверный формат бюджета. Введите число:")

async def handle_workers_needed(message: types.Message, state: FSMContext):
    try:
        workers = int(message.text)
        if workers <= 0:
            raise ValueError
        await state.update_data(workers_needed=workers)
        await message.answer("Отправьте геолокацию объекта:", 
                            reply_markup=get_location_keyboard())
        await OrderCreationStates.LOCATION.set()
    except ValueError:
        await message.answer("Неверное количество. Введите целое число:")

async def handle_location(message: types.Message, state: FSMContext):
    if message.location:
        location = f"{message.location.latitude},{message.location.longitude}"
        await state.update_data(location=location)
        await message.answer("Загрузите 3+ фото объекта:")
        await OrderCreationStates.PHOTOS.set()
    else:
        await message.answer("Пожалуйста, отправьте геолокацию через кнопку.")

async def handle_photos(message: types.Message, state: FSMContext):
    if message.photo:
        photos = [photo.file_id for photo in message.photo]
        data = await state.get_data()
        
        order_data = order_schemas.OrderCreate(
            customer_id=message.from_user.id,
            work_type=data['work_type'],
            budget=data['budget'],
            workers_needed=data['workers_needed'],
            location=data['location'],
            photos=photos
        )
        
        async with get_db() as db:
            order = await order_service.create_order(db, order_data)
            await message.answer(f"✅ Заказ #{order.id} создан!\n"
                                f"Тип работ: {order.work_type}\n"
                                f"Бюджет: {order.budget}₪\n"
                                f"Рабочих: {order.workers_needed}")
        
        await state.finish()
    else:
        await message.answer("Пожалуйста, отправьте фото объекта.")

def get_work_types_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("Сантехника", callback_data="work:plumbing"),
        types.InlineKeyboardButton("Электрика", callback_data="work:electrical"),
        types.InlineKeyboardButton("Отделка", callback_data="work:finishing"),
        types.InlineKeyboardButton("Кровля", callback_data="work:roofing"),
        types.InlineKeyboardButton("Строительство", callback_data="work:construction")
    )
    return keyboard

def get_location_keyboard():
    keyboard = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, 
        resize_keyboard=True
    )
    keyboard.add(types.KeyboardButton("Отправить геолокацию", request_location=True))
    return keyboard

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_order_creation, commands=["new_order"])
    dp.register_callback_query_handler(handle_work_type, lambda c: c.data.startswith("work:"), state=OrderCreationStates.WORK_TYPE)
    dp.register_message_handler(handle_budget, state=OrderCreationStates.BUDGET)
    dp.register_message_handler(handle_workers_needed, state=OrderCreationStates.WORKERS_NEEDED)
    dp.register_message_handler(handle_location, content_types=["location"], state=OrderCreationStates.LOCATION)
    dp.register_message_handler(handle_photos, content_types=["photo"], state=OrderCreationStates.PHOTOS)
