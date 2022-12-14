from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import pprint as pp
from bs4 import BeautifulSoup
import time

# Set up chrome driver options
ua = UserAgent()
user_agent = ua.random

options = webdriver.ChromeOptions()
# options.add_argument(f'user-agent={user_agent}')
# options.add_argument("--incognito")
# options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
# options.add_argument("--headless")  # Comment this line to see script running in Chrome.
options.add_experimental_option("detach", True)

# Locate driver in path and input options parameters
chrome_driver_path = 'chrome_d.exe'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.delete_cookie('_GRECAPTCHA')

keywords = ['joyas',
            'playeras',
            'gorras',
            'sexshop',
            'vape',
            'lentes',
            'anillos',
            'regalos',
            'novedades',
            'papeleria',
            'ropa',
            'vestidos',
            'fajas',
            'suplementos',
            'juguetes',
            'libros',
            'dulces',
            'talabarteria',
            'imprenta',
            'tenis',
            'zapatos',
            'esoteria',
            'velas',
            'cuarzos',
            'mochilas']
cities = ["mty", "cdmx"]
keyword = keywords[0]
city = cities[0]

q = f"{keyword} {city}"

url = f"https://www.google.com/search?q={q}&tbm=lcl&start={0}"

driver.get(url)

wait = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".a-no-hover-decoration"))
    )

boxes = driver.find_elements(By.CSS_SELECTOR, ".a-no-hover-decoration")


for box in boxes:
    info = box.text.splitlines()
    if len(info) == 2 or len(info) == 0:
        continue

    print('------------')
    print(info)

    name = info[0]
    rating = info[1]


    data = {
        "name": name,
        "rating": rating,
        "business_type": business_type,
        "address": address,
    }

    pp.pprint(data)
    print('------------')










