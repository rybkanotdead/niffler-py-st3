#!/usr/bin/env python3
"""
Скрипт для регистрации нового тестового пользователя в Niffler.
Используется до запуска тестов.
"""
import os
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv('niffler-e2e-tests-python/.env')

AUTH_URL = os.getenv('AUTH_URL', 'http://auth.niffler.dc:9000')


def register_user(username: str, password: str) -> bool:
    """
    Регистрирует нового пользователя в системе.
    
    Args:
        username: Имя пользователя
        password: Пароль
        
    Returns:
        True если регистрация успешна, False в противном случае
    """
    print(f"Регистрируем пользователя: {username}")
    
    options = ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_experimental_option('prefs', {
        "credentials_enable_service": False,
        "password_manager_enabled": False,
    })
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Открываем страницу регистрации
        driver.get(f"{AUTH_URL}/register")
        wait = WebDriverWait(driver, 15)
        
        # Ждем появления формы регистрации
        username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name=username]')))
        
        # Заполняем форму регистрации
        username_field.send_keys(username)
        
        password_field = driver.find_element(By.CSS_SELECTOR, 'input[name=password]')
        password_field.send_keys(password)
        
        submit_password_field = driver.find_element(By.CSS_SELECTOR, 'input[name=passwordSubmit]')
        submit_password_field.send_keys(password)
        
        # Кликаем на кнопку Sign Up
        sign_up_btn = driver.find_element(By.CSS_SELECTOR, 'button[type=submit]')
        sign_up_btn.click()
        
        # Ждем успешной регистрации - появления сообщения об успехе
        try:
            wait_success = WebDriverWait(driver, 10)
            success_msg = wait_success.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'p[class*=form__paragraph_success]'))
            )
            print(f"✅ Пользователь {username} успешно зарегистрирован!")
            return True
        except Exception as e:
            # Проверяем, может быть пользователь уже существует
            try:
                error_msg = driver.find_element(By.CSS_SELECTOR, '.form__error')
                if "already exists" in error_msg.text or "уже существует" in error_msg.text:
                    print(f"ℹ️  Пользователь {username} уже существует")
                    return True
                else:
                    print(f"❌ Ошибка регистрации: {error_msg.text}")
                    return False
            except:
                print(f"❌ Неизвестная ошибка регистрации: {str(e)}")
                return False
                
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        return False
    finally:
        driver.quit()


def main():
    """Основная функция."""
    # Генерируем учетные данные
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    username = f'testuser_{timestamp}'
    password = 'TestPass123!'
    
    print(f"\n{'='*50}")
    print(f"Регистрация тестового пользователя")
    print(f"{'='*50}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Auth URL: {AUTH_URL}\n")
    
    # Пытаемся зарегистрировать
    if register_user(username, password):
        print(f"\n{'='*50}")
        print("Обновляем .env файл...")
        
        # Обновляем .env файл
        env_file = 'niffler-e2e-tests-python/.env'
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Заменяем учетные данные
        content = content.replace(
            f'TEST_USERNAME={os.getenv("TEST_USERNAME", "rybkanotdead")}',
            f'TEST_USERNAME={username}'
        )
        content = content.replace(
            f'TEST_PASSWORD={os.getenv("TEST_PASSWORD", "123456")}',
            f'TEST_PASSWORD={password}'
        )
        
        # Если строк нет, добавляем в конец
        if 'TEST_USERNAME=' not in content:
            content += f'\nTEST_USERNAME={username}\n'
        if 'TEST_PASSWORD=' not in content:
            content += f'TEST_PASSWORD={password}\n'
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print(f"✅ .env файл обновлен!")
        print(f"✅ Новые учетные данные:")
        print(f"   TEST_USERNAME={username}")
        print(f"   TEST_PASSWORD={password}")
        print(f"{'='*50}\n")
        
        return 0
    else:
        print(f"❌ Не удалось зарегистрировать пользователя")
        return 1


if __name__ == '__main__':
    sys.exit(main())

