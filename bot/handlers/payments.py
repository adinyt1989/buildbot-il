from modules.payments.service import create_bit_payment

@dp.message_handler(commands=["pay"])
async def pay_order(message: types.Message):
    payment = await create_bit_payment(1000, "order_123")
    await message.answer(f"💳 Оплатите [здесь]({payment['url']})", parse_mode="Markdown")
