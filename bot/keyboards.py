from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(text="Каталог"),
            KeyboardButton(text="Мои заказы")
        ]],
        resize_keyboard=True
    )

def get_product_keyboard(product_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Подробнее", callback_data=f"product_{product_id}")
    ]])
