from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class Registration(StatesGroup):
    language = State()
    phone = State()
    code = State()
    account_type = State()

async def start_cmd(message: types.Message):
    await message.answer("Добро пожаловать в BuildBot IL!\nВыберите язык:", 
                         reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Please choose language:", 
                         reply_markup=get_language_keyboard())
    await Registration.language.set()

async def language_chosen(callback: types.CallbackQuery, state: FSMContext):
    lang = callback.data.split(":")[1]
    await state.update_data(language=lang)
    await callback.message.answer("Введите ваш номер телефона в формате +972501234567:")
    await Registration.phone.set()

async def phone_received(message: types.Message, state: FSMContext):
    phone = message.text
    # Простая валидация
    if not phone.startswith("+972") or len(phone) != 13:
        return await message.answer("Неверный формат. Введите в формате +972501234567")
    
    await state.update_data(phone=phone)
    await message.answer("Код подтверждения отправлен. Введите код: 123456")  # Для теста
    await Registration.code.set()

async def code_received(message: types.Message, state: FSMContext):
    if message.text != "123456":
        return await message.answer("Неверный код. Попробуйте снова.")
    
    await message.answer("Выберите тип аккаунта:", reply_markup=get_account_type_keyboard())
    await Registration.account_type.set()

async def account_type_chosen(callback: types.CallbackQuery, state: FSMContext):
    account_type = callback.data.split(":")[1]
    data = await state.get_data()
    await callback.message.answer(f"Регистрация завершена!\n"
                                 f"Язык: {data['language']}\n"
                                 f"Телефон: {data['phone']}\n"
                                 f"Тип: {account_type}")
    await state.finish()

def get_language_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang:ru"),
        types.InlineKeyboardButton("🇬🇧 English", callback_data="lang:en"),
        types.InlineKeyboardButton("🇮🇱 עברית", callback_data="lang:he")
    )
    return keyboard

def get_account_type_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Заказчик", callback_data="type:customer"))
    keyboard.add(types.InlineKeyboardButton("Исполнитель", callback_data="type:performer"))
    keyboard.add(types.InlineKeyboardButton("Бригада", callback_data="type:team"))
    return keyboard

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=["start"])
    dp.register_callback_query_handler(language_chosen, lambda c: c.data.startswith("lang:"), state=Registration.language)
    dp.register_message_handler(phone_received, state=Registration.phone)
    dp.register_message_handler(code_received, state=Registration.code)
    dp.register_callback_query_handler(account_type_chosen, lambda c: c.data.startswith("type:"), state=Registration.account_type)
