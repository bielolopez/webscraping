from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

from selenium.webdriver.support.ui import WebDriverWait
# Specifying incognito mode as you launch your browser[OPTIONAL]
# option = webdriver.ChromeOptions()
# option.add_argument("--incognito")

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")


driver = webdriver.Chrome("./chromedriver.exe", options=opts)


driver.get("https://www.devoto.com.uy/almacen?sc=3")


driver.maximize_window()
time.sleep(10)


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









#Precio_antes = dom.xpath('//div[@class="Product-prices"]/span/text()')

    #print(Precio_antes)
    # album_link = album_title['href']
    # title = album_title.div.span['aria-label']
    # style = album_title.div.span['style']
    # styles = cssutils.parseStyle(style)
    # url = styles['background-image']
    # opacity = styles['opacity']
    # album_date = album.find("div", class_="soundTitle__usernameTitleContainer")
    # date = album_date.find("span", class_="releaseDateCompact sc-type-light sc-font-light").span.text



#productos = driver.find_elements(By.XPATH, '//h3[@class="Product-title"]')

# Por cada review...
# for producto in productos:
#
#   # Obtengo el contenedor del nombre de usuario
#   Nombre_producto = productos.find_element(By.XPATH, './text()"]')
#   print(Nombre_producto)

  # # LOGICA DE MAXIMA PAGINACION CON LAZO WHILE
  # # VECES VOY A PAGINAR HASTA UN MAXIMO DE 10
  # PAGINACION_MAX = 10
  # PAGINACION_ACTUAL = 1
  #
  # # Mientras la pagina en la que me encuentre, sea menor que la maxima pagina que voy a sacar... sigo ejecutando...
  # while PAGINACION_MAX > PAGINACION_ACTUAL:
  #
  #     links_productos = driver.find_elements(By.XPATH, '//a[@class="item__info-title"]')
  #     links_de_la_pagina = []
  #     for a_link in links_productos:
  #         links_de_la_pagina.append(a_link.get_attribute("href"))
  #     # Q: Pero leaonrdo, porque no hiciste for link in link_productos, y simplemente ibas y volvias haciendo click en el contenedor que me lleva a la otra pagina?
  #     # A: Porque al yo irme y volver, pierdo la referencia de links_productos que tuve inicialmente. Y selenium me daria error porque le intentaria dar click a algo que no existe en el DOM actual.
  #     # Es por esto que, la mejor estrategia es obtener todos los links como cadenas de texto y luego iterarlos.
  #
  #     for link in links_de_la_pagina:
  #
  #         try:
  #             # Voy a cada uno de los links de los detalles de los productos
  #             driver.get(link)
  #
  #             # Rara vez da error si no utilizamos una espera por eventos:
  #             # precio_element = WebDriverWait(driver, 10).until(
  #             #   EC.presence_of_element_located((By.XPATH, '//span[includes(@class,"price-tag")]'))
  #             # )
  #             titulo = driver.find_element(By.XPATH, '//h1').text
  #             precio = driver.find_element(By.XPATH, '//span[includes(@class,"price-tag")]').text
  #             print(titulo)
  #             print(precio.replace('\n', '').replace('\t', ''))
  #
  #             # Aplasto el boton de retroceso
  #             driver.back()
  #         except Exception as e:
  #             print(e)
  #             # Si sucede algun error dentro del detalle, no me complico. Regreso a la lista y sigo con otro producto.
  #             driver.back()
  #
  #     # Logica de deteccion de fin de paginacion
  #     try:
  #         # Intento obtener el boton de SIGUIENTE y le intento dar click
  #         puedo_seguir_horizontal = driver.find_element(By.XPATH, '//span[text()="Siguiente"]')
  #         puedo_seguir_horizontal.click()
  #     except:
  #         # Si obtengo un error al intentar darle click al boton, quiere decir que no existe
  #         # Lo cual me indica que ya no puedo seguir paginando, por ende rompo el While
  #         break
  #
  #     PAGINACION_ACTUAL += 1
