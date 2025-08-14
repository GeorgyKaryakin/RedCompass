# ReloCompass - Telegram Bot для лидогенерации в недвижимости

## 🎯 Описание проекта
Telegram-бот для генерации лидов с нулевой рекламной стоимостью для бизнеса RED (недвижимость на Пхукете, Бали, Грузии, Турции, Кипре).

## 🏗️ Архитектура

### Модули
1. **Умный онбординг** - сбор данных пользователей без раздражения
2. **Гибридный каталог** - объекты RED Experts + клиентские бусты
3. **Визовый ассистент** - квиз для определения подходящей визы
4. **Лид-менеджмент** - автоматическая передача в AmoCRM

### Технический стек
- **Backend**: Python 3.10+, aiogram 3.x
- **База данных**: PostgreSQL + Redis (кэширование)
- **Админка**: Django Admin
- **Интеграции**: AmoCRM REST API

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка окружения
Создайте файл `.env`:
```env
# Telegram Bot
BOT_TOKEN=your_telegram_bot_token

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/relocompass
REDIS_URL=redis://localhost:6379/0

# AmoCRM
AMOCRM_DOMAIN=your_domain.amocrm.ru
AMOCRM_ACCESS_TOKEN=your_access_token

# Django
SECRET_KEY=your_django_secret_key
DEBUG=True
```

### 3. Запуск базы данных
```bash
# PostgreSQL
docker run -d --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:15

# Redis
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

### 4. Миграции
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Запуск бота
```bash
python bot/main.py
```

### 6. Запуск админки
```bash
python manage.py runserver
```

## 📊 Структура проекта
```
ReloCompass/
├── bot/                    # Telegram bot
│   ├── handlers/          # Обработчики сообщений
│   ├── keyboards/         # Клавиатуры
│   ├── models/            # Модели данных
│   └── services/          # Бизнес-логика
├── admin_panel/           # Django админка
├── database/              # Миграции и схемы
├── config/                # Конфигурация
└── tests/                 # Тесты
```

## 🔧 Основные команды бота
- `/start` - начало работы
- `/catalog` - каталог недвижимости
- `/visa` - визовый помощник
- `/help` - справка

## 📈 Метрики
- Лиды RED Experts: экономия $50/лид
- Клиентские лиды: доход $30/лид
- Время отклика: <5 секунд
- Конверсия: >15%

## 🚨 Ограничения MVP
- Запрещены интеграции с вебинарами, SIM-картами
- Только базовые сценарии лидогенерации
- Срок разработки: 14 дней
