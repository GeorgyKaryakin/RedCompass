#!/usr/bin/env python3
"""
Скрипт для создания суперпользователя Django
"""

import os
import sys
import django

# Добавляем корневую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    """Создание суперпользователя"""
    try:
        # Проверяем, существует ли уже суперпользователь
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Суперпользователь уже существует")
            return True
        
        # Создаем суперпользователя
        user = User.objects.create_superuser(
            username='admin',
            email='admin@relocompass.com',
            password='admin123'
        )
        
        print(f"✅ Суперпользователь создан:")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Password: admin123")
        print("\n⚠️ Не забудьте изменить пароль после первого входа!")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания суперпользователя: {e}")
        return False

if __name__ == "__main__":
    print("👤 Создание суперпользователя Django...")
    
    if create_superuser():
        print("\n🎉 Готово! Теперь можно войти в админку:")
        print("   URL: http://localhost:8000/admin")
        print("   Username: admin")
        print("   Password: admin123")
    else:
        print("\n❌ Не удалось создать суперпользователя")
        sys.exit(1)
