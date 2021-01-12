from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

from selenium.webdriver.support.ui import WebDriverWait


opts = Options()
opts.add_argument("user-agent=...")


driver = webdriver.Chrome("./chromedriver.exe", options=opts)


driver.get("https://www.devoto.com.uy/almacen?sc=3")


driver.maximize_window()
time.sleep(10)  # or a random  >10 and < 14


iter = 1
while True:
	scrollHeight = driver.execute_script("return document.documentElement.scrollHeight")
	Height = 250 * iter
	driver.execute_script("window.scrollTo(0, " + str(Height) + ");")
	if Height > scrollHeight:
		print('End of page')
		break
	time.sleep(1)
	iter += 1


body = driver.execute_script("return document.body")
source = body.get_attribute('innerHTML')



soup = BeautifulSoup(source, "html.parser")

for producto in soup.find_all(class_= "Product-head"):
	Nombre_producto = producto.find('h3', class_="Product-title").text
	Precio_1 = producto.find_next_sibling('div', class_="Product-control")
	Precio_2 = Precio_1.find('div', class_="Product-prices")
	Precio = Precio_2.find('span').text
	print(Nombre_producto)
	print(Precio)


