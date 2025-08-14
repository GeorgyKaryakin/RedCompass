#!/usr/bin/env python3
"""
Упрощенный скрипт запуска ReloCompass MVP
Запускает бота и Django админку без Docker
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

def print_banner():
    """Вывод баннера"""
    print("""
🏠 ReloCompass - Запуск MVP
==================================================
🚀 Быстрый запуск без Docker
""")

def check_dependencies():
    """Проверка зависимостей"""
    print("🔍 Проверка зависимостей...")
    
    # Проверяем Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Требуется Python 3.8+")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Проверяем pip
    try:
        import pip
        print("✅ pip доступен")
    except ImportError:
        print("❌ pip не найден")
        return False
    
    return True

def install_dependencies():
    """Установка зависимостей"""
    print("\n📦 Установка зависимостей...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Зависимости установлены")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки зависимостей: {e}")
        return False

def setup_django():
    """Настройка Django"""
    print("\n🔧 Настройка Django...")
    
    try:
        # Создаем миграции
        subprocess.run([sys.executable, "manage.py", "makemigrations"], 
                      check=True, capture_output=True)
        print("✅ Миграции созданы")
        
        # Применяем миграции
        subprocess.run([sys.executable, "manage.py", "migrate"], 
                      check=True, capture_output=True)
        print("✅ Миграции применены")
        
        # Создаем суперпользователя
        print("👤 Создание суперпользователя Django...")
        print("Введите данные для суперпользователя (или нажмите Enter для пропуска):")
        
        try:
            subprocess.run([sys.executable, "manage.py", "createsuperuser", "--noinput"], 
                          check=True, capture_output=True)
            print("✅ Суперпользователь создан")
        except subprocess.CalledProcessError:
            print("ℹ️ Создание суперпользователя пропущено")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка настройки Django: {e}")
        return False

def start_services():
    """Запуск сервисов"""
    print("\n🚀 Запуск сервисов...")
    
    processes = []
    
    try:
        # Запускаем Django сервер
        print("🌐 Запуск Django админки...")
        django_process = subprocess.Popen([
            sys.executable, "manage.py", "runserver", "8000"
        ])
        processes.append(("Django", django_process))
        print("✅ Django админка запущена на http://localhost:8000")
        
        # Ждем немного для запуска Django
        time.sleep(3)
        
        # Запускаем Telegram бота
        print("🤖 Запуск Telegram бота...")
        bot_process = subprocess.Popen([
            sys.executable, "bot/main.py"
        ])
        processes.append(("Bot", bot_process))
        print("✅ Telegram бот запущен")
        
        print("\n🎉 Все сервисы запущены!")
        print("📱 Telegram бот: активен")
        print("🌐 Django админка: http://localhost:8000/admin")
        print("\nДля остановки нажмите Ctrl+C")
        
        # Ждем сигнала остановки
        while True:
            time.sleep(1)
            # Проверяем, что процессы еще работают
            for name, process in processes:
                if process.poll() is not None:
                    print(f"❌ {name} остановлен неожиданно")
                    return False
        
    except KeyboardInterrupt:
        print("\n\n🛑 Остановка сервисов...")
        
        for name, process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {name} остановлен")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"⚠️ {name} принудительно остановлен")
        
        print("👋 Все сервисы остановлены")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка запуска сервисов: {e}")
        return False

def main():
    """Основная функция"""
    print_banner()
    
    # Проверяем зависимости
    if not check_dependencies():
        print("❌ Проверка зависимостей не пройдена")
        return False
    
    # Устанавливаем зависимости
    if not install_dependencies():
        print("❌ Установка зависимостей не удалась")
        return False
    
    # Настраиваем Django
    if not setup_django():
        print("❌ Настройка Django не удалась")
        return False
    
    # Запускаем сервисы
    return start_services()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
