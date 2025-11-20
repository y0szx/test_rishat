# Django + Stripe API

## !---Примечание---!

НЕВОЗМОЖНО ПРОВЕСТИ ОПЛАТУ ЗАКАЗА, В КОТОРОМ НАХОДЯТСЯ ПРЕДМЕТЫ С РАЗНЫМИ ВАЛЮТАМИ

API доступно по адресу: https://test-rishat-yusupov.amvera.io/

## Доступные эндпоинты

- `.../admin` - админ панель (креды для входа в админку `admin:admin`);
- `.../item/<id>` - страница с информацией о предмете и кнопкой "Купить";
- `.../buy/<id>` - возвращает stripe session id для оплаты отдельного предмета;
- `.../order/<id>` - страница с информацией о заказе и кнопкой "Купить";
- `.../buy_order/<id>` - возвращает stripe session id для оплаты заказа.

## Локальный запуск

```bash
# Клонировать репозиторий
git clone https://github.com/y0szx/test_rishat.git
cd test_rishat
```

В корне проекта создать файл `.env` по примеру `.env.example`:
```
SECRET_API_KEY=sk_test_2yQ...
PUBLISHABLE_API_KEY=pk_test_9Ky...
SERVER_BASE_URL=http://localhost:8000
```

```bash
# Запустить проект
docker-compose up --build

# API доступно на http://localhost:8000
```

## База данных

База данных состоит из таблиц Item, Order, OrderItem, Tax, Discount.

Таблица `Item`:
```
name: str
description: str
price: float
currency: str
tax: str, ForeignKey(Tax)
discount: str, ForeignKey(Discount)
```

Таблица `Order`:
```
tax: str, ForeignKey(Tax)
discount: str, ForeignKey(Discount)
```

Таблица `OrderItem`:
```
order: str, ForeignKey(Order)
item: str, ForeignKey(Item)
quantity: int
```

Таблица `Tax`:
```
name: str
percentage: int
stripe_tax_rate_id: str
```

Таблица `Discount`:
```
name: str
coupon_id: str
```
