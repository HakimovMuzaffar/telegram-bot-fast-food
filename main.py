from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, CallbackQuery, LabeledPrice
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import *
from database import *
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')
PAYMENT = os.getenv('PAYMENT')
CHANNEL_ID = os.getenv('CHANNEL_ID')

storage = MemoryStorage()

bot = Bot(TOKEN, parse_mode='HTML')

dp = Dispatcher(bot, storage=storage)


class CommentState(StatesGroup):
    waiting_for_comment = State()


@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    full_name = message.from_user.full_name
    await message.answer(f'Salom <b>{full_name}</b> Loookga xush kelibsiz! 🥙🥪🌮')
    await register_user(message)


async def register_user(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    user = first_name_user(chat_id)
    if user:
        await message.answer(f'Xush kelibsiz {full_name} 😎')
        await show_main_menu(message)
    else:
        first_register_user(chat_id,full_name)
        await message.answer("Ro'yxatdan o'tishingiz uchun kontaktingizni jo'nating 📲", reply_markup=phone_button())


@dp.message_handler(content_types=['contact'])
async def finish_register(message: Message):
    chat_id = message.chat.id
    phone = message.contact.phone_number
    update_user_to_finish_register(chat_id, phone)
    await create_cart_for_user(message)
    await message.answer("Ro'yxatdan mufaqiyatli o'ttingiz ✔")
    await show_main_menu(message)


async def create_cart_for_user(message: Message):
    chat_id = message.chat.id
    try:
        insert_to_cart(chat_id)
    except:
        pass


async def show_main_menu(message):
    await message.answer("Bo'limni tanlang", reply_markup=generate_main_menu())


@dp.message_handler(lambda message: '💸 Buyurtma berish' in message.text)
async def make_order(message: Message):
    await message.answer('Kategoriyani tanlang', reply_markup=generate_category_menu())


@dp.callback_query_handler(lambda call: 'category' in call.data)
async def show_products(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, categories_id = call.data.split('_')
    categories_id = int(categories_id)
    await bot.edit_message_text('Maxsulot tanlang', chat_id,message_id, reply_markup=products_by_category(categories_id))


@dp.callback_query_handler(lambda call: 'main_menu' in call.data)
async def return_to_main_menu(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text='Kategoriyani tanlang',
                                reply_markup=generate_category_menu())


@dp.callback_query_handler(lambda call: 'product' in call.data)
async def show_detail_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, product_id = call.data.split('_')
    product_id = int(product_id)

    product = get_product_detail(product_id)
    await bot.delete_message(chat_id, message_id)
    with open(product[4], mode='rb') as img:
        await bot.send_photo(chat_id=chat_id, photo=img, caption=f'''{product[2]}

Narxi: {product[3]}''', reply_markup=generate_product_detail_menu(product_id=product_id, categories_id=product[1]))


@dp.callback_query_handler(lambda call: 'back' in call.data)
async def return_to_category(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, categories_id = call.data.split('_')
    await bot.delete_message(chat_id, message_id)
    await bot.send_message(chat_id, 'Maxsulot tanlang', reply_markup=products_by_category(categories_id))


# @dp.callback_query_handler(lambda call: 'cart' in call.data)
# async def add_product_cart(call: CallbackQuery):
#     chat_id = call.message.chat.id
#     _, product_id, quantity = call.data.split('_')
#     product_id, quantity = int(product_id), int(quantity)
#
#     cart_id = get_user_cart_id(chat_id)
#     product = get_product_detail(product_id)
#
#     final_price = quantity * product[3]
#
#     if insert_or_update_cart_product(cart_id, product[2], quantity, final_price):
#         await bot.answer_callback_query(call.id, "Maxsulot qo'shildi")
#     else:
#         await bot.answer_callback_query(call.id, "Soni o'zgardi")

@dp.callback_query_handler(lambda call: call.data.startswith('add_'))
async def add_product_to_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    data = call.data.split('_')
    quantity = int(data[1])
    product_id = int(data[2])

    product = get_product_detail(product_id)
    product_name = product[2]
    price = product[3]

    add_product_to_cart_db(chat_id, product_name, quantity, price)

    await call.answer(f" Savatga {quantity} dona {product_name} qo'shildi", show_alert=True)


@dp.message_handler(regexp='🛒 Savat')
async def show_cart(message: Message, edit_message: bool = False):
    chat_id = message.chat.id
    cart_id = get_user_cart_id(chat_id)

    try:
        update_total_product_total_price(cart_id)
    except Exception as e:
        print(e)
        await message.answer('Savat bo`sh')
        return

    cart_products = get_cart_products(cart_id)
    total_products, total_price = get_total_products_price(cart_id)

    if total_products and total_price:
        text = 'Sizning savat: \n\n'
        i = 0
        for product_name, quantity, final_price in cart_products:
            i += 1
            text += f"""{i}. {product_name}

Soni: {quantity}
Umumiy summa: {final_price}\n\n"""

        text += f"""Umumiy soni: {total_products}
Umumiy to'lashingiz kerak bo'lgan summa: {total_price}"""

        if edit_message:
            await bot.edit_message_text(text, chat_id, message.message_id, reply_markup=generate_cart_menu(cart_id))
        else:
            await bot.send_message(chat_id, text, reply_markup=generate_cart_menu(cart_id))
    else:
        await bot.delete_message(chat_id, message.message_id)
        await bot.send_message(chat_id, 'Savat bo`sh')


@dp.callback_query_handler(lambda call: 'delete' in call.data)
async def delete_cart_product(call: CallbackQuery):
    _, cart_product_id = call.data.split('_')
    message = call.message
    cart_product_id = int(cart_product_id)

    delete_cart_product_from_database(cart_product_id)

    await bot.answer_callback_query(call.id, text='Maxsulot ochirildi')
    await show_cart(message, edit_message=True)


@dp.callback_query_handler(lambda call: 'order' in call.data)
async def create_order(call: CallbackQuery):
    chat_id = call.message.chat.id

    _, cart_id = call.data.split('_')
    cart_id = int(cart_id)

    time_order = datetime.now().strftime('%H:%M')
    date_order = datetime.now().strftime('%d.%m.%Y')

    cart_products = get_cart_products(cart_id)
    total_products, total_price = get_total_products_price(cart_id)

    save_order_check(cart_id, total_products, total_price, time_order, date_order)
    order_check_id = get_order_check_id(cart_id)

    if total_products and total_price:
        text = 'Sizning savat: \n\n'
        i = 0
        for product_name, quantity, final_price in cart_products:
            i += 1
            text += f"""{i}. {product_name}

Soni: {quantity}
Umumiy summa: {final_price}\n\n"""
            save_order(order_check_id, product_name, quantity, final_price)
        text += f"""Umumiy soni: {total_products}
Umumiy to'lashingiz kerak bo'lgan summa: {total_price}"""

        await bot.send_invoice(
            chat_id=chat_id,
            title=f'Buyurtma raqami №{cart_id}',
            description=text,
            payload='bot-defined invoice payload',
            provider_token=PAYMENT,
            currency='UZS',
            prices=[
                LabeledPrice(label='Umumiy summa', amount=int(total_price * 100)),
                LabeledPrice(label='Yetqazib berish', amount=1500000)
            ],
            start_parameter='start_parameter'
        )


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query_handler):
    try:
        await bot.answer_pre_checkout_query(pre_checkout_query_handler.id, ok=True)
    except Exception as e:
        await bot.answer_pre_checkout_query(pre_checkout_query_handler.id, ok=False,
                                            error_message=f"Xato yuz berdi: {str(e)}")



@dp.message_handler(content_types=['successful_payment'])
async def get_payment(message):
    chat_id = message.chat.id
    cart_id = get_user_cart_id(chat_id)
    await bot.send_message(chat_id, "To'lov muvaffaqiyatli amalga oshirildi!")
    drop_cart_products_default(cart_id)


@dp.callback_query_handler(lambda call: 'decrease' in call.data)
async def decrease_cart_product(call: CallbackQuery):
    try:
        print(f"Callback data: {call.data}")
        _, amount, cart_product_id = call.data.split('_')
        cart_product_id = int(cart_product_id)
        amount = int(amount)

        decrease_cart_product_quantity(cart_product_id, amount)

        await bot.answer_callback_query(call.id, text=f'Mahsulot miqdori {amount} ga kamaytirildi')
        await show_cart(call.message, edit_message=True)
    except ValueError as e:
        print(f"ValueError: {e}")
        await bot.answer_callback_query(call.id, text=str(e))
    except Exception as e:
        print(f"Exception: {e}")
        await bot.answer_callback_query(call.id, text="Noma'lum xatolik yuz berdi.")


@dp.message_handler(lambda message: '📃 tarix' in message.text)
async def show_history_orders(message: Message):
    chat_id = message.chat.id

    # 1. Foydalanuvchi savat ID sini olish
    cart_id = get_user_cart_id(chat_id)
    if not cart_id:
        await message.reply("Hozircha buyurtmalar tarixi mavjud emas.")
        return

    # 2. Order check ID larni olish
    order_check_ids = get_order_check(cart_id)
    if not order_check_ids:
        await message.reply("Buyurtmalar tarixi topilmadi.")
        return

    # 3. Buyurtma ma'lumotlarini yig'ish
    for order_check in order_check_ids:
        text = f"""🗓 Sana: {order_check[-1]}
⏰ Vaqt: {order_check[-2]}
📦 Umumiy soni: {order_check[3]}
💳 Umumiy summasi: {order_check[2]} so'm\n\n"""

        # Tafsilotlarini olish
        detail_orders = get_detail_order(order_check[0])
        for detail in detail_orders:
            text += f"""📌 Maxsulot: {detail[0]}
🔢 Soni: {detail[1]}
💰 Umumiy summasi: {detail[2]} so'm\n\n"""

        # Xabar yuborish
        await bot.send_message(chat_id, text)


@dp.message_handler(regexp='🚩 Manzil')
async def send_location(message: types.Message):
    chat_id = message.chat.id
    latitude = 41.254734618998455
    longitude = 69.2031473190866

    await bot.send_location(
        chat_id=message.chat.id,
        latitude=latitude,
        longitude=longitude,
    )
    await bot.send_message(chat_id, "Kutib qolamiz!")


@dp.message_handler(regexp='✍️ Fikringizni qoldiring')
async def comment_sent(message: types.Message):
    chat_id = message.chat.id
    await message.answer("Maxsulot haqida fikringizni qoldiring 🖊")
    await CommentState.waiting_for_comment.set()

# Foydalanuvchining izohini qabul qilish
@dp.message_handler(state=CommentState.waiting_for_comment, content_types=types.ContentType.TEXT)
async def user_comment(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    message_text = message.text
    cart_id = get_user_cart_id(chat_id)
    user_data = get_user_info(cart_id)

    await bot.send_message(
        CHANNEL_ID,
        f"""Ism Familiya: {user_data[0]} 
Tel raqam: {user_data[3]} 
Username: https://t.me/{message.from_user.username } 
Qoldirgan izohi:
========================================
{message_text}"""
    )

    await bot.send_message(chat_id, "Rahmat izoh uchun!")
    await state.finish()

# Foydalanuvchining savat ID sini olish
def get_user_cart_id(chat_id):
    return 1  # faqat savat ID ni qaytaradi

# Foydalanuvchining ma'lumotlarini olish
def get_user_info(cart_id):
    # Dummy ma'lumotlar
    return ["Ism Familiya", "", "", "Tel raqam"]  # Ma'lumotlar to'plami













executor.start_polling(dp, skip_updates=True)