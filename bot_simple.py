#!/usr/bin/env python3
"""
Упрощенная версия Telegram бота ReloCompass
Работает без Django ORM для быстрого запуска MVP
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Загружаем переменные окружения из .env файла
try:
    from dotenv import load_dotenv
    # Загружаем .env файл из корневой директории
    env_path = Path(__file__).parent / '.env'
    load_dotenv(env_path)
    print(f"✅ Загружен .env файл: {env_path}")
except ImportError:
    print("⚠️ python-dotenv не установлен, используем системные переменные")
except Exception as e:
    print(f"⚠️ Ошибка загрузки .env: {e}")

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Загружаем токен из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error("BOT_TOKEN не установлен!")
    logger.error("Проверьте .env файл или установите переменную BOT_TOKEN")
    sys.exit(1)

logger.info(f"✅ BOT_TOKEN загружен: {BOT_TOKEN[:10]}...")

# Состояния для FSM
class UserStates(StatesGroup):
    waiting_for_stage = State()
    waiting_for_family = State()
    waiting_for_budget = State()
    waiting_for_region = State()

# Клавиатуры
def get_main_menu():
    """Главное меню"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Каталог недвижимости", callback_data="catalog")],
        [InlineKeyboardButton(text="🛂 Виза-ассистент", callback_data="visa")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="help")]
    ])
    return keyboard

def get_stage_keyboard():
    """Клавиатура выбора стадии"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤔 Планирую переезд", callback_data="stage_planning")],
        [InlineKeyboardButton(text="🔍 Ищу недвижимость", callback_data="stage_searching")],
        [InlineKeyboardButton(text="💰 Готов к покупке", callback_data="stage_ready")]
    ])
    return keyboard

def get_family_keyboard():
    """Клавиатура выбора размера семьи"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Один", callback_data="family_1")],
        [InlineKeyboardButton(text="👥 2-3 человека", callback_data="family_2_3")],
        [InlineKeyboardButton(text="👨‍👩‍👧‍👦 4+ человека", callback_data="family_4_plus")]
    ])
    return keyboard

def get_budget_keyboard():
    """Клавиатура выбора бюджета"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💵 До $100K", callback_data="budget_100k")],
        [InlineKeyboardButton(text="💰 $100K - $300K", callback_data="budget_300k")],
        [InlineKeyboardButton(text="💎 $300K+", callback_data="budget_300k_plus")]
    ])
    return keyboard

def get_region_keyboard():
    """Клавиатура выбора региона"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏝️ Пхукет", callback_data="region_phuket")],
        [InlineKeyboardButton(text="🌴 Бали", callback_data="region_bali")],
        [InlineKeyboardButton(text="🏔️ Грузия", callback_data="region_georgia")],
        [InlineKeyboardButton(text="🏛️ Турция", callback_data="region_turkey")],
        [InlineKeyboardButton(text="🏖️ Кипр", callback_data="region_cyprus")]
    ])
    return keyboard

# Обработчики команд
async def start_command(message: types.Message, state: FSMContext):
    """Обработчик команды /start"""
    await message.answer(
        "🏠 Добро пожаловать в ReloCompass!\n\n"
        "Я помогу вам найти идеальную недвижимость для переезда.\n\n"
        "Давайте начнем с небольшого опроса:",
        reply_markup=get_stage_keyboard()
    )
    await state.set_state(UserStates.waiting_for_stage)

async def handle_stage_selection(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора стадии"""
    stage = callback.data.replace("stage_", "")
    await state.update_data(stage=stage)
    
    await callback.message.edit_text(
        "Отлично! Теперь расскажите о составе семьи:",
        reply_markup=get_family_keyboard()
    )
    await state.set_state(UserStates.waiting_for_family)

async def handle_family_selection(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора размера семьи"""
    family = callback.data.replace("family_", "")
    await state.update_data(family=family)
    
    await callback.message.edit_text(
        "Отлично! Теперь выберите ваш бюджет:",
        reply_markup=get_budget_keyboard()
    )
    await state.set_state(UserStates.waiting_for_budget)

async def handle_budget_selection(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора бюджета"""
    budget = callback.data.replace("budget_", "")
    await state.update_data(budget=budget)
    
    await callback.message.edit_text(
        "Отлично! Теперь выберите предпочитаемый регион:",
        reply_markup=get_region_keyboard()
    )
    await state.set_state(UserStates.waiting_for_region)

async def handle_region_selection(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора региона"""
    region = callback.data.replace("region_", "")
    await state.update_data(region=region)
    
    # Получаем все данные
    user_data = await state.get_data()
    
    await callback.message.edit_text(
        f"🎉 Отлично! Ваш профиль создан:\n\n"
        f"📋 Стадия: {user_data.get('stage', 'Не указано')}\n"
        f"👥 Семья: {user_data.get('family', 'Не указано')}\n"
        f"💰 Бюджет: {user_data.get('budget', 'Не указано')}\n"
        f"🌍 Регион: {user_data.get('region', 'Не указано')}\n\n"
        f"Теперь вы можете использовать все функции бота!",
        reply_markup=get_main_menu()
    )
    
    # Сбрасываем состояние
    await state.clear()
    
    # Логируем создание пользователя
    logger.info(f"User {callback.from_user.id} completed onboarding: {user_data}")

async def handle_catalog(callback: types.CallbackQuery):
    """Обработка каталога недвижимости"""
    await callback.message.edit_text(
        "🏠 Каталог недвижимости\n\n"
        "В разработке...\n\n"
        "Здесь будет отображаться каталог недвижимости с приоритетом:\n"
        "1. RED Experts (собственные объекты)\n"
        "2. Буст-объекты\n"
        "3. Остальные объекты\n\n"
        "Вернуться в главное меню:",
        reply_markup=get_main_menu()
    )

async def handle_visa(callback: types.CallbackQuery):
    """Обработка виза-ассистента"""
    await callback.message.edit_text(
        "🛂 Виза-ассистент\n\n"
        "В разработке...\n\n"
        "Здесь будет 3-вопросный квиз для определения подходящего типа визы.\n\n"
        "Вернуться в главное меню:",
        reply_markup=get_main_menu()
    )

async def handle_stats(callback: types.CallbackQuery):
    """Обработка статистики"""
    await callback.message.edit_text(
        "📊 Статистика\n\n"
        "В разработке...\n\n"
        "Здесь будет отображаться статистика пользователей и лидов.\n\n"
        "Вернуться в главное меню:",
        reply_markup=get_main_menu()
    )

async def handle_help(callback: types.CallbackQuery):
    """Обработка помощи"""
    await callback.message.edit_text(
        "❓ Помощь\n\n"
        "🤖 ReloCompass - бот для генерации лидов в сфере недвижимости\n\n"
        "📱 Основные команды:\n"
        "/start - Начать работу с ботом\n"
        "/menu - Главное меню\n"
        "/help - Эта справка\n\n"
        "Вернуться в главное меню:",
        reply_markup=get_main_menu()
    )

async def handle_menu(callback: types.CallbackQuery):
    """Обработка главного меню"""
    await callback.message.edit_text(
        "🏠 Главное меню\n\n"
        "Выберите нужную функцию:",
        reply_markup=get_main_menu()
    )

async def handle_unknown(callback: types.CallbackQuery):
    """Обработка неизвестных callback'ов"""
    await callback.answer("Неизвестная команда", show_alert=True)

# Основная функция
async def main():
    """Основная функция запуска бота"""
    logger.info("Запуск упрощенной версии бота...")
    
    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Регистрация обработчиков
    dp.message.register(start_command, Command("start"))
    dp.callback_query.register(handle_stage_selection, lambda c: c.data.startswith("stage_"))
    dp.callback_query.register(handle_family_selection, lambda c: c.data.startswith("family_"))
    dp.callback_query.register(handle_budget_selection, lambda c: c.data.startswith("budget_"))
    dp.callback_query.register(handle_region_selection, lambda c: c.data.startswith("region_"))
    dp.callback_query.register(handle_catalog, lambda c: c.data == "catalog")
    dp.callback_query.register(handle_visa, lambda c: c.data == "visa")
    dp.callback_query.register(handle_stats, lambda c: c.data == "stats")
    dp.callback_query.register(handle_help, lambda c: c.data == "help")
    dp.callback_query.register(handle_menu, lambda c: c.data == "menu")
    dp.callback_query.register(handle_unknown)
    
    # Запуск бота
    logger.info("Бот запущен в режиме polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        sys.exit(1)
