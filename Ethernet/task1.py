from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time

# Путь к драйверу Microsoft Edge
driver_path = 'msedgedriver.exe'

# Инициализация драйвера Microsoft Edge
options = webdriver.EdgeOptions()
driver = webdriver.Edge(service=Service(driver_path), options=options)

# Открытие веб-страницы
driver.get('https://example.com')

# Установка значения в LocalStorage
script_set_value = """
localStorage.setItem('myKey', 'myValue');
"""
driver.execute_script(script_set_value)

# Получение значения из LocalStorage
script_get_value = """
return localStorage.getItem('myKey');
"""
stored_value = driver.execute_script(script_get_value)
print("Stored value in LocalStorage:", stored_value)

# Удаление значения из LocalStorage
script_remove_value = """
localStorage.removeItem('myKey');
"""
driver.execute_script(script_remove_value)

# Закрытие браузера
driver.quit()
