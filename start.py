#!/usr/bin/env python3
"""
Скрипт для быстрого запуска ReloCompass
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_command(command, description):
    """Выполнение команды с выводом"""
    print(f"\n🚀 {description}...")
    print(f"Команда: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} завершено успешно")
        if result.stdout:
            print(f"Вывод: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при {description.lower()}: {e}")
        if e.stderr:
            print(f"Ошибка: {e.stderr}")
        return False

def check_dependencies():
    """Проверка зависимостей"""
    print("🔍 Проверка зависимостей...")
    
    # Проверяем Python
    if sys.version_info < (3, 10):
        print("❌ Требуется Python 3.10 или выше")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Проверяем pip
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
        print("✅ pip доступен")
    except subprocess.CalledProcessError:
        print("❌ pip недоступен")
        return False
    
    return True

def install_dependencies():
    """Установка зависимостей"""
    print("\n📦 Установка зависимостей...")
    
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Установка Python пакетов"):
        return False
    
    return True

def start_database():
    """Запуск базы данных"""
    print("\n🗄️ Запуск базы данных...")
    
    # Проверяем Docker
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        print("✅ Docker доступен")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker недоступен. Установите Docker Desktop")
        return False
    
    # Останавливаем существующие контейнеры
    run_command("docker-compose down", "Остановка существующих контейнеров")
    
    # Запускаем контейнеры
    if not run_command("docker-compose up -d", "Запуск контейнеров базы данных"):
        return False
    
    # Ждем запуска базы данных
    print("⏳ Ожидание запуска базы данных...")
    time.sleep(10)
    
    return True

def setup_django():
    """Настройка Django"""
    print("\n🐍 Настройка Django...")
    
    # Создаем директорию для логов
    os.makedirs("logs", exist_ok=True)
    
    # Применяем миграции
    if not run_command(f"{sys.executable} manage.py makemigrations", "Создание миграций Django"):
        return False
    
    if not run_command(f"{sys.executable} manage.py migrate", "Применение миграций Django"):
        return False
    
    # Создаем суперпользователя
    print("\n👤 Создание суперпользователя Django...")
    print("Введите данные для суперпользователя:")
    
    try:
        subprocess.run([sys.executable, "manage.py", "createsuperuser"], check=True)
        print("✅ Суперпользователь создан")
    except subprocess.CalledProcessError:
        print("⚠️ Создание суперпользователя пропущено")
    
    return True

def start_bot():
    """Запуск Telegram бота"""
    print("\n🤖 Запуск Telegram бота...")
    
    # Проверяем наличие токена
    if not os.path.exists(".env"):
        print("❌ Файл .env не найден!")
        print("Скопируйте env.example в .env и заполните BOT_TOKEN")
        return False
    
    # Запускаем бота в фоне
    try:
        process = subprocess.Popen([sys.executable, "bot/main.py"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        print(f"✅ Бот запущен (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")
        return None

def start_admin():
    """Запуск Django админки"""
    print("\n🖥️ Запуск Django админки...")
    
    try:
        process = subprocess.Popen([sys.executable, "manage.py", "runserver"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        print(f"✅ Django админка запущена (PID: {process.pid})")
        print("🌐 Админка доступна по адресу: http://localhost:8000/admin/")
        return process
    except Exception as e:
        print(f"❌ Ошибка запуска Django админки: {e}")
        return None

def main():
    """Основная функция"""
    print("🏠 ReloCompass - Запуск проекта")
    print("=" * 50)
    
    # Проверяем зависимости
    if not check_dependencies():
        return
    
    # Устанавливаем зависимости
    if not install_dependencies():
        return
    
    # Запускаем базу данных
    if not start_database():
        return
    
    # Настраиваем Django
    if not setup_django():
        return
    
    # Запускаем бота
    bot_process = start_bot()
    if not bot_process:
        return
    
    # Запускаем админку
    admin_process = start_admin()
    if not admin_process:
        return
    
    print("\n🎉 Проект успешно запущен!")
    print("\n📱 Telegram бот работает")
    print("🖥️ Django админка: http://localhost:8000/admin/")
    print("🗄️ База данных: localhost:5432")
    print("🔴 Redis: localhost:6379")
    
    print("\n⏹️ Для остановки нажмите Ctrl+C")
    
    try:
        # Ждем завершения процессов
        bot_process.wait()
        admin_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Остановка проекта...")
        
        # Останавливаем процессы
        if bot_process:
            bot_process.terminate()
        if admin_process:
            admin_process.terminate()
        
        # Останавливаем контейнеры
        run_command("docker-compose down", "Остановка контейнеров")
        
        print("✅ Проект остановлен")

if __name__ == "__main__":
    main()
