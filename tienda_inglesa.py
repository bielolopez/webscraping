from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time
from pymongo import MongoClient


client = MongoClient('localhost')
db = client['tienda_inglesa']
col = db['alimentos']


# Definimos el User Agent en Selenium utilizando la clase Options
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
driver = webdriver.Chrome('./chromedriver.exe', options=opts) # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER

#URL SEMILLA
driver.get('https://www.tiendainglesa.com.uy/Categoria/Almac%C3%A9n/busqueda?0,0,*:*,0,0,0,rel,%5B%5D,false,%5B%5D,%5B%5D,983')


# LOGICA DE MAXIMA PAGINACION CON LAZO WHILE
# VECES VOY A PAGINAR HASTA UN MAXIMO DE 10
PAGINACION_MAX = 200
PAGINACION_ACTUAL = 0

# Mientras la pagina en la que me encuentre, sea menor que la maxima pagina que voy a sacar... sigo ejecutando...
while PAGINACION_MAX > PAGINACION_ACTUAL:

  body = driver.execute_script("return document.body")
  source = body.get_attribute('innerHTML')

  soup = BeautifulSoup(source, "html.parser")


  # ids =[]
  # for i in range(1, 9):
  #   ids.append("GridresultsContainerRow_000" + str(i))
  # for i in range(10, 20):
  #   ids.append("GridresultsContainerRow_00" + str(i))
  #"GridresultsContainerRow_" + "\d+"





  for producto in soup.find_all(class_="ProductCompBack"):
      Nombre_producto = producto.find(class_ = "wCartProductName")
      Nombre = Nombre_producto.find('a').text
      Precio_producto = producto.find(class_ = "tblSearchPrice")
      Precio = Precio_producto.find(class_ = "ProductPrice").text
      Precio = Precio.replace("$", "").strip()

      print(Nombre)
      print(Precio)


      col.insert_one({
        'Nombre': Nombre,
        'Precio': Precio,
     })

      time.sleep(1)



  # Logica de deteccion de fin de paginacion
  try:
    # Intento obtener el boton de SIGUIENTE y le intento dar click
    puedo_seguir_horizontal = driver.find_element(By.XPATH, '//a[text()=">"]')
    puedo_seguir_horizontal.click()
  except:
    # Si obtengo un error al intentar darle click al boton, quiere decir que no existe
    # Lo cual me indica que ya no puedo seguir paginando, por ende rompo el While
    break

    PAGINACION_ACTUAL += 1
