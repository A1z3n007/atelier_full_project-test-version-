
# Atelier Telegram Bot + Flask Web App

Полный проект для ателье: включает веб-сайт на Flask и Telegram-бота на Aiogram.

## 🔗 Компоненты

### 🖥 Flask-сайт:
- Регистрация / вход
- Каталог товаров
- Корзина и оформление заказа
- Админ-панель

### 🤖 Telegram-бот:
- Команды: `/start`, `Каталог`, `Мои заказы`
- Инлайн-кнопки: "Подробнее", "Купить"
- Заказ через Telegram
- Синхронизация с базой данных

---

## 🚀 Установка

1. Установите зависимости:

```bash
pip install -r requirements.txt
```

2. Создайте базу данных PostgreSQL и настройте строку подключения в `app.py` и `bot_db.py`:

```
postgresql+psycopg2://username:password@localhost:PORT/DB_NAME
```

3. Запустите сайт:

```bash
python app.py
```

4. Запустите Telegram-бота:

```bash
python bot/main.py
```

---

## 📁 Структура проекта

```
project/
├── app.py
├── models.py
├── bot/
│   ├── main.py
│   ├── handlers.py
│   ├── keyboards.py
│   ├── config.py
│   └── bot_db.py
├── templates/
│   └── base.html, ...
├── static/
│   └── style_base.css
├── requirements.txt
└── README.md
```

---

## ✅ Зависимости

- Flask
- SQLAlchemy
- Aiogram 3.x
- Psycopg2-binary

---

Разработано специально для ознакомления и для копирования 💪
##copyright by @ERNUR
