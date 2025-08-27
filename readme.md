Django-приложение с интеграцией Stripe для обработки платежей. Реализует функционал покупки товаров и заказов с поддержкой скидок, налогов и мультивалютности.

## 🌟 Основные возможности

- Покупка отдельных товаров через Stripe Checkout Session
- Покупка заказов с множественными товарами
- Поддержка скидок и налогов
- Мультивалютность (USD, EUR)
- Два способа оплаты: Checkout Session и Payment Intent
- Полная интеграция с Django Admin

## 🎯 Бонусные функции реализованы

- ✅ Environment variables
- ✅ Django Admin панель
- ✅ Модель Order с множественными товарами
- ✅ Модели Discount и Tax
- ✅ Мультивалютность (USD, EUR)
- ✅ Payment Intent API

## 🚀 Быстрый старт

# 1. Установка зависимостей

### Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/macOS
### или
venv\Scripts\activate     # Windows
###  Установка зависимостей
pip install -r requirements.txt

# 🛠 API-эндпоинты
### Товары (Items)
GET /item/<id>/ - Просмотр товара с кнопкой покупки (Checkout Session)
GET /buy/<id>/ - Создание Stripe Checkout Session для товара
GET /payment-intent/<id>/ - Создание Stripe Payment Intent для товара
GET /item-payment-intent/<id>/ - Просмотр товара с формой Payment Intent
### Заказы (Orders)
GET /order/<id>/ - Просмотр заказа с кнопкой покупки
GET /order/buy/<id>/ - Создание Stripe Checkout Session для заказа
### Статусные страницы
GET /success/ - Успешная оплата
GET /cancel/ - Отмена оплаты
# 💳 Тестирование Stripe
### Для тестирования используйте тестовые данные карт:

Номер карты: 4242 4242 4242 4242
Дата истечения: Любая будущая дата
CVC: Любые 3 цифры
Имя владельца: Любое имя
administration
Перейдите в админку: http://localhost:8000/admin/
Войдите с данными суперпользователя
Создайте товары, скидки, налоги и заказы

# 📦 Зависимости
### Django 4.2
### Stripe 5.5.0
### python-decouple 3.8

# P.S.
Данная работа выполнения как тестовое задание.