from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# Путь к драйверу Microsoft Edge
driver_path = 'msedgedriver.exe'

# Инициализация драйвера Microsoft Edge
options = webdriver.EdgeOptions()
driver = webdriver.Edge(service=Service(driver_path), options=options)

# Открытие веб-страницы
driver.get('https://example.com')

# Установка значения в cookie
cookie = {'name': 'myCookie', 'value': 'cookieValue'}
driver.add_cookie(cookie)

# Получение значения из cookie
cookies = driver.get_cookies()
for cookie in cookies:
    if cookie['name'] == 'myCookie':
        stored_value = cookie['value']
        print("Stored value in cookie:", stored_value)
        break

# Удаление значения из cookie
driver.delete_cookie('myCookie')

# Закрытие браузера
driver.quit()
