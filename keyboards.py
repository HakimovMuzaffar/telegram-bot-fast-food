from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database import *

def phone_button():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text="Kontakt jo'natish 📞", request_contact=True)]
    ], resize_keyboard=True)


def generate_main_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text='💸 Buyurtma berish')],
        [KeyboardButton(text='📃 tarix'), KeyboardButton(text='🛒 Savat'), KeyboardButton(text='🚩 Manzil')],
        [KeyboardButton(text='✍️ Fikringizni qoldiring')]
    ], resize_keyboard=True)

def generate_category_menu():
    markup = InlineKeyboardMarkup(row_width=3)
    markup.row(
        InlineKeyboardMarkup(text='Menu  🧾', url='https://telegra.ph/LoooK-12-14' )
    )

    catrgories = get_all_catrgories()
    button = []
    for catrgory in catrgories:
        btn = InlineKeyboardButton(text=catrgory[1], callback_data=f'category_{catrgory[0]}')
        button.append(btn)
    markup.add(*button)
    return markup


def products_by_category(categories_id):
    markup = InlineKeyboardMarkup(row_width=3)
    products = get_products_by_category_id(categories_id)
    button = []
    for product in products:
        btn = InlineKeyboardButton(text=product[1], callback_data=f'product_{product[0]}')
        button.append(btn)
    markup.add(*button)
    markup.row(
        InlineKeyboardButton(text='Ortga', callback_data='main_menu')
    )
    return markup


# def generate_product_detail_menu(product_id, categories_id):
#     markup = InlineKeyboardMarkup(row_width=3)
#     numbers = [i for i in range(1, 10)]
#     buttons = []
#     for number in numbers:
#         btn = InlineKeyboardButton(text=str(number), callback_data=f'cart_{product_id}_{number}')
#         buttons.append(btn)
#
#     markup.add(*buttons)
#     markup.row(
#         InlineKeyboardButton(text='Ortga', callback_data=f'back_{categories_id}')
#     )
#     return markup


def generate_product_detail_menu(product_id, categories_id):
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton(text="+1", callback_data=f"add_1_{product_id}"),
        InlineKeyboardButton(text="+3", callback_data=f"add_3_{product_id}"),
        InlineKeyboardButton(text="+5", callback_data=f"add_5_{product_id}"),
        InlineKeyboardButton(text="+7", callback_data=f"add_7_{product_id}"),
        InlineKeyboardButton(text="+10", callback_data=f"add_10_{product_id}")
    )
    markup.row(
        InlineKeyboardButton(text="Ortga", callback_data=f"back_{categories_id}")
    )
    return markup


def generate_cart_menu(cart_id):
    print(f"generate_cart_menu chaqirildi. cart_id: {cart_id}")
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='🚀 Buyurtmani tasdiqlash', callback_data=f'order_{cart_id}')
    )

    cart_products = get_cart_product_for_delete(cart_id)

    for cart_product_id, product_name in cart_products:
        print(f"Qo'shilayotgan tugma: ➖1 {product_name}, cart_product_id: {cart_product_id}")
        markup.row(
            InlineKeyboardButton(text=f'➖1 {product_name}', callback_data=f'decrease_1_{cart_product_id}'),
            InlineKeyboardButton(text=f'➖3 {product_name}', callback_data=f'decrease_3_{cart_product_id}'),
            InlineKeyboardButton(text=f'❌ {product_name}', callback_data=f'delete_{cart_product_id}')
        )
    return markup





