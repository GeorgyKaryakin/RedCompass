#!/usr/bin/env python3
"""
Скрипт запуска ReloCompass MVP
Запускает Django админку и Telegram бота
"""

import subprocess
import time
import sys
import os

def print_banner():
    """Вывод баннера"""
    print("""
🏠 ReloCompass MVP - Запуск
==================================================
🚀 Быстрый запуск без Docker
""")

def start_django():
    """Запуск Django сервера"""
    print("🌐 Запуск Django админки...")
    try:
        process = subprocess.Popen([
            sys.executable, "manage.py", "runserver", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Ждем немного для запуска
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Django админка запущена на http://localhost:8000")
            print("   Логин: admin")
            print("   Пароль: admin123")
            return process
        else:
            print("❌ Django не удалось запустить")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка запуска Django: {e}")
        return None

def start_bot():
    """Запуск Telegram бота"""
    print("🤖 Запуск Telegram бота...")
    try:
        process = subprocess.Popen([
            sys.executable, "bot_simple.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Ждем немного для запуска
        time.sleep(2)
        
        if process.poll() is None:
            print("✅ Telegram бот запущен")
            return process
        else:
            print("❌ Бот не удалось запустить")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")
        return None

def main():
    """Основная функция"""
    print_banner()
    
    print("🔍 Проверка готовности...")
    
    # Проверяем наличие файлов
    required_files = [
        "manage.py",
        "bot_simple.py", 
        ".env",
        "requirements.txt"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} не найден")
            return False
    
    print("\n🚀 Запуск сервисов...")
    
    # Запускаем Django
    django_process = start_django()
    if not django_process:
        return False
    
    # Запускаем бота
    bot_process = start_bot()
    if not bot_process:
        django_process.terminate()
        return False
    
    print("\n🎉 Все сервисы запущены!")
    print("\n📱 Доступные сервисы:")
    print("   🌐 Django админка: http://localhost:8000/admin")
    print("   🤖 Telegram бот: активен")
    print("\n📋 Инструкции:")
    print("   1. Откройте админку в браузере")
    print("   2. Войдите с логином admin/admin123")
    print("   3. Протестируйте бота командой /start")
    print("\n🛑 Для остановки нажмите Ctrl+C")
    
    try:
        # Ждем завершения процессов
        while True:
            time.sleep(1)
            
            # Проверяем статус процессов
            if django_process.poll() is not None:
                print("❌ Django остановлен")
                break
                
            if bot_process.poll() is not None:
                print("❌ Бот остановлен")
                break
                
    except KeyboardInterrupt:
        print("\n\n🛑 Остановка сервисов...")
        
        # Останавливаем Django
        if django_process:
            django_process.terminate()
            django_process.wait(timeout=5)
            print("✅ Django остановлен")
        
        # Останавливаем бота
        if bot_process:
            bot_process.terminate()
            bot_process.wait(timeout=5)
            print("✅ Бот остановлен")
        
        print("👋 Все сервисы остановлены")
        return True
    
    return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
