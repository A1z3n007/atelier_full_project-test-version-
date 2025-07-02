from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from bot.keyboards import get_main_keyboard, get_product_keyboard
from bot.bot_db import SessionLocal
from models import Product, Order, User

router = Router()

@router.message(F.text.lower() == "/start")
async def cmd_start(message: Message):
    kb = get_main_keyboard()
    await message.answer("Привет! Добро пожаловать в ателье 🧵", reply_markup=kb)

@router.message(F.text.lower() == "каталог")
async def show_catalog(message: Message):
    db = SessionLocal()
    products = db.query(Product).all()
    if not products:
        await message.answer("Каталог пуст.")
        return
    for product in products:
        kb = get_product_keyboard(product.id)
        await message.answer(f"{product.name} — {product.price}₸", reply_markup=kb)
    db.close()

@router.callback_query(F.data.startswith("product_"))
async def show_product_detail(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    db = SessionLocal()
    product = db.query(Product).get(product_id)
    if product:
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🛒 Купить", callback_data=f"buy_{product.id}")
        ]])
        await callback.message.answer_photo(product.image_url, caption=f"{product.name} {product.description} Цена: {product.price}₸", reply_markup=kb)
    else:
        await callback.message.answer("Товар не найден.")
    db.close()

@router.callback_query(F.data.startswith("buy_"))
async def buy_product(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    db = SessionLocal()
    tg_id = callback.from_user.id
    user = db.query(User).filter_by(telegram_id=tg_id).first()
    if not user:
        user = User(username=f"user_{tg_id}", telegram_id=tg_id)
        db.add(user)
        db.commit()
    order = Order(user_id=user.id, product_id=product_id, quantity=1)
    db.add(order)
    db.commit()
    await callback.message.answer("✅ Заказ оформлен!")
    db.close()

@router.message(F.text.lower() == "мои заказы")
async def show_orders(message: Message):
    db = SessionLocal()
    tg_id = message.from_user.id
    user = db.query(User).filter_by(telegram_id=tg_id).first()
    if not user:
        await message.answer("Вы ещё ничего не заказывали.")
        return
    orders = db.query(Order).filter_by(user_id=user.id).all()
    if not orders:
        await message.answer("У вас пока нет заказов.")
    else:
        msg = "Ваши заказы:"
    for order in orders:
        msg += f"- {order.product.name} x{order.quantity} "
        await message.answer(msg)
    db.close()