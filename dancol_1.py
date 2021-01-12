
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient


client = MongoClient('localhost:27017')
db = client['dancol']
col = db['todo_selenium']


# Definimos el User Agent en Selenium utilizando la clase Options
opts = Options()
opts.add_argument("user-agent=...")


# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
driver = webdriver.Chrome('./chromedriver.exe') # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER

# Voy a la pagina que requiero
driver.get('https://www.dancol.com.uy/copia-de-colchones-de-resortes')


for i in range(90): # Voy a darle click en cargar mas 3 veces
    try:
        # Esperamos a que el boton se encuentre disponible a traves de una espera por eventos
        # Espero un maximo de 10 segundos, hasta que se encuentre el boton dentro del DOM
        boton = WebDriverWait(driver, 15).until(
          EC.presence_of_element_located((By.XPATH, '//button[@data-hook="load-more-button"]'))
        )
        # le doy click al boton que espere
        boton.click()

        # Espero hasta 10 segundos a que toda la informacion de todos los anuncios se encuentre cargada
        WebDriverWait(driver, 20).until(
          EC.presence_of_all_elements_located((By.XPATH, '//li[@data-hook="product-list-grid-item"]//h3[@data-hook="product-item-name"]'))
        )
        # Luego de que se hallan todos los elementos cargados, seguimos la ejecucion
    except Exception as e:
        print (e)
        # si hay algun error, rompo el lazo. No me complico.
        break

# Encuentro cual es el XPATH de cada elemento donde esta la informacion que quiero extraer
# Esto es una LISTA. Por eso el metodo esta en plural
lista_precios = driver.find_elements_by_xpath('//li[@data-hook="product-list-grid-item"]')

# Recorro cada uno de los anuncios que he encontrado
for precio in lista_precios:
    # Por cada anuncio hallo el precio, que en esta pagina principal, rara vez suele no estar, por eso hacemos esta validacion.
    try:
      nombre_item = precio.find_element_by_xpath('.//h3[@data-hook="product-item-name"]').text
      precio_antes_descuento = precio.find_element_by_xpath('.//span[@data-hook="product-item-price-before-discount"]').text
      precio_item = precio.find_element_by_xpath('.//span[@data-hook="product-item-price-to-pay"]').text
      nombre_item = nombre_item.replace('$U', '')
      precio_antes_descuento = precio_antes_descuento.replace('$U', '')
      precio_item = precio_item.replace('$U', '')
    except:
      nombre_item = 'NO DISPONIBLE'
      precio_antes_descuento = 'NO DISPONIBLE'
      precio_item = 'NO DISPONIBLE'
    print ("Nombre Producto: " + nombre_item)
    print("Precio normal: " + precio_item)
    print("Precio sin descuento: " + precio_antes_descuento)



    col.insert_one({
        'Nombre': nombre_item,
        'Precio': precio_antes_descuento,
        'Precio_con_despuesnto': precio_item
    })

    # Por cada anuncio hallo la descripcion
    #descripcion = auto.find_element_by_xpath('.//span[@data-aut-id="itemTitle"]').text
    #print (descripcion)




# Nombre Producto: Quality 2.0 (2 plazas)
# Precio normal: $U19.958,64
# Precio sin descuento: $U38.382,00
# Nombre Producto: Grand Master (2 Plazas)
# Precio normal: $U22.157,00
# Precio sin descuento: $U41.805,66
# Nombre Producto: Elegance Comfort (2 plaza)
# Precio normal: $U24.787,02
# Precio sin descuento: $U48.602,00
# Nombre Producto: Premium Comfort 33 /Pillow (2 plazas)
# Precio normal: $U19.913,04
# Precio sin descuento: $U36.876,00
# Nombre Producto: Super Comfort 33 (2 plazas)
# Precio normal: $U18.640,16
# Precio sin descuento: $U33.286,00
# Nombre Producto: Super Density 28 (2 plazas)
# Precio normal: $U14.925,06
# Precio sin descuento: $U27.639,00
# Nombre Producto: Magno Vitta (Queen)
# Precio normal: $U31.846,06
# Precio sin descuento: $U54.907,00
# Nombre Producto: Elegance Comfort (Queen)
# Precio normal: $U28.587,04
# Precio sin descuento: $U49.288,00
# Nombre Producto: Quality 2.0 (Queen)
# Precio normal: $U24.237,04
# Precio sin descuento: $U41.788,00
# Nombre Producto: Max Density 45 (Queen)
# Precio normal: $U28.934,46
# Precio sin descuento: $U49.887,00
# Nombre Producto: Super Density 28 (Queen)
# Precio normal: $U17.707,98
# Precio sin descuento: $U30.531,00
# Nombre Producto: Procoluna 33 (Queen)
# Precio normal: $U31.489,94
# Precio sin descuento: $U54.293,00
# Nombre Producto: Super Density 28 (1 plaza)
# Precio normal: $U9.661,25
# Precio sin descuento: $U16.375,00
# Nombre Producto: Premium Comfort 33 /Pillow (1 Plaza)
# Precio normal: $U13.208,92
# Precio sin descuento: $U22.388,00
# Nombre Producto: Super Comfort 33 (1 Plaza)
# Precio normal: $U11.350,42
# Precio sin descuento: $U19.238,00
# Nombre Producto: e-pocket (1 Plaza)
# Precio normal: $U12.601,22
# Precio sin descuento: $U21.358,00
# Nombre Producto: Magno Vitta (1 plaza)
# Precio normal: $U17.652,80
# Precio sin descuento: $U29.920,00
# Nombre Producto: Quality 2.0 (1 plaza)
# Precio normal: $U13.672,66
# Precio sin descuento: $U23.174,00
# Nombre Producto: Eucalyptus Pocket (1 plaza)
# Precio normal: $U24.479,36
# Precio sin descuento: $U38.249,00
# Nombre Producto: Resiste Pocket (1 plaza)
# Precio normal: $U17.542,28
# Precio sin descuento: $U28.294,00
# Nombre Producto: Resiste Pocket "Plus" (1 Plaza)
# Precio normal: $U26.094,60
# Precio sin descuento: $U41.420,00
# Nombre Producto: Eucalyptus Pocket (2 plazas)
# Precio normal: $U29.657,02
# Precio sin descuento: $U46.339,10
# Nombre Producto: Magno Vitta (2 plazas)
# Precio normal: $U28.349,20
# Precio sin descuento: $U51.544,00
# Nombre Producto: Excelsus Pocket (2 plazas)
# Precio normal: $U25.918,10
# Precio sin descuento: $U39.874,00
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: Procoluna 33 Doble Pillow (Queen)
# Precio normal: $U33.583,16
# Precio sin descuento: $U57.902,00
# Nombre Producto: Procoluna 45 Doble Pillow (Queen)
# Precio normal: $U35.653,76
# Precio sin descuento: $U61.472,00
# Nombre Producto: Premium Comfort 33 /Pillow (Queen)
# Precio normal: $U26.543,70
# Precio sin descuento: $U45.765,00
# Nombre Producto: Grand Master (Queen Size)
# Precio normal: $U26.110,00
# Precio sin descuento: $U49.264,15
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: Excelsus Pocket (Queen)
# Precio normal: $U36.543,65
# Precio sin descuento: $U56.221,00
# Nombre Producto: Resiste Pocket (Extra King)
# Precio normal: $U37.940,90
# Precio sin descuento: $U61.195,00
# Nombre Producto: Excelsus Pocket (Extra King)
# Precio normal: $U43.755,40
# Precio sin descuento: $U67.316,00
# Nombre Producto: Sublime Pocket (Extra King)
# Precio normal: $U41.256,60
# Precio sin descuento: $U68.761,00
# Nombre Producto: Eucalyptus Pocket (1 plaza)
# Precio normal: $U24.479,36
# Precio sin descuento: $U38.249,00
# Nombre Producto: Resiste Pocket (1 plaza)
# Precio normal: $U17.542,28
# Precio sin descuento: $U28.294,00
# Nombre Producto: Resiste Pocket "Plus" (1 Plaza)
# Precio normal: $U26.094,60
# Precio sin descuento: $U41.420,00
# Nombre Producto: Eucalyptus Pocket (2 plazas)
# Precio normal: $U29.657,02
# Precio sin descuento: $U46.339,10
# Nombre Producto: Magno Vitta (2 plazas)
# Precio normal: $U28.349,20
# Precio sin descuento: $U51.544,00
# Nombre Producto: Excelsus Pocket (2 plazas)
# Precio normal: $U25.918,10
# Precio sin descuento: $U39.874,00
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: Procoluna 33 Doble Pillow (Queen)
# Precio normal: $U33.583,16
# Precio sin descuento: $U57.902,00
# Nombre Producto: Procoluna 45 Doble Pillow (Queen)
# Precio normal: $U35.653,76
# Precio sin descuento: $U61.472,00
# Nombre Producto: Premium Comfort 33 /Pillow (Queen)
# Precio normal: $U26.543,70
# Precio sin descuento: $U45.765,00
# Nombre Producto: Grand Master (Queen Size)
# Precio normal: $U26.110,00
# Precio sin descuento: $U49.264,15
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: Excelsus Pocket (Queen)
# Precio normal: $U36.543,65
# Precio sin descuento: $U56.221,00
# Nombre Producto: Resiste Pocket (Extra King)
# Precio normal: $U37.940,90
# Precio sin descuento: $U61.195,00
# Nombre Producto: Excelsus Pocket (Extra King)
# Precio normal: $U43.755,40
# Precio sin descuento: $U67.316,00
# Nombre Producto: Sublime Pocket (Extra King)
# Precio normal: $U41.256,60
# Precio sin descuento: $U68.761,00
# Nombre Producto: Eucalyptus Pocket (1 plaza)
# Precio normal: $U24.479,36
# Precio sin descuento: $U38.249,00
# Nombre Producto: Resiste Pocket (1 plaza)
# Precio normal: $U17.542,28
# Precio sin descuento: $U28.294,00
# Nombre Producto: Resiste Pocket "Plus" (1 Plaza)
# Precio normal: $U26.094,60
# Precio sin descuento: $U41.420,00
# Nombre Producto: Eucalyptus Pocket (2 plazas)
# Precio normal: $U29.657,02
# Precio sin descuento: $U46.339,10
# Nombre Producto: Magno Vitta (2 plazas)
# Precio normal: $U28.349,20
# Precio sin descuento: $U51.544,00
# Nombre Producto: Excelsus Pocket (2 plazas)
# Precio normal: $U25.918,10
# Precio sin descuento: $U39.874,00
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: Procoluna 33 Doble Pillow (Queen)
# Precio normal: $U33.583,16
# Precio sin descuento: $U57.902,00
# Nombre Producto: Procoluna 45 Doble Pillow (Queen)
# Precio normal: $U35.653,76
# Precio sin descuento: $U61.472,00
# Nombre Producto: Premium Comfort 33 /Pillow (Queen)
# Precio normal: $U26.543,70
# Precio sin descuento: $U45.765,00
# Nombre Producto: Grand Master (Queen Size)
# Precio normal: $U26.110,00
# Precio sin descuento: $U49.264,15
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: Excelsus Pocket (Queen)
# Precio normal: $U36.543,65
# Precio sin descuento: $U56.221,00
# Nombre Producto: Resiste Pocket (Extra King)
# Precio normal: $U37.940,90
# Precio sin descuento: $U61.195,00
# Nombre Producto: Excelsus Pocket (Extra King)
# Precio normal: $U43.755,40
# Precio sin descuento: $U67.316,00
# Nombre Producto: Sublime Pocket (Extra King)
# Precio normal: $U41.256,60
# Precio sin descuento: $U68.761,00
# Nombre Producto: Eucalyptus Pocket (1 plaza)
# Precio normal: $U24.479,36
# Precio sin descuento: $U38.249,00
# Nombre Producto: Resiste Pocket (1 plaza)
# Precio normal: $U17.542,28
# Precio sin descuento: $U28.294,00
# Nombre Producto: Resiste Pocket "Plus" (1 Plaza)
# Precio normal: $U26.094,60
# Precio sin descuento: $U41.420,00
# Nombre Producto: Eucalyptus Pocket (2 plazas)
# Precio normal: $U29.657,02
# Precio sin descuento: $U46.339,10
# Nombre Producto: Magno Vitta (2 plazas)
# Precio normal: $U28.349,20
# Precio sin descuento: $U51.544,00
# Nombre Producto: Excelsus Pocket (2 plazas)
# Precio normal: $U25.918,10
# Precio sin descuento: $U39.874,00
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: Procoluna 33 Doble Pillow (Queen)
# Precio normal: $U33.583,16
# Precio sin descuento: $U57.902,00
# Nombre Producto: Procoluna 45 Doble Pillow (Queen)
# Precio normal: $U35.653,76
# Precio sin descuento: $U61.472,00
# Nombre Producto: Premium Comfort 33 /Pillow (Queen)
# Precio normal: $U26.543,70
# Precio sin descuento: $U45.765,00
# Nombre Producto: Grand Master (Queen Size)
# Precio normal: $U26.110,00
# Precio sin descuento: $U49.264,15
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: Excelsus Pocket (Queen)
# Precio normal: $U36.543,65
# Precio sin descuento: $U56.221,00
# Nombre Producto: Resiste Pocket (Extra King)
# Precio normal: $U37.940,90
# Precio sin descuento: $U61.195,00
# Nombre Producto: Excelsus Pocket (Extra King)
# Precio normal: $U43.755,40
# Precio sin descuento: $U67.316,00
# Nombre Producto: Sublime Pocket (Extra King)
# Precio normal: $U41.256,60
# Precio sin descuento: $U68.761,00
# Nombre Producto: Eucalyptus Pocket (1 plaza)
# Precio normal: $U24.479,36
# Precio sin descuento: $U38.249,00
# Nombre Producto: Resiste Pocket (1 plaza)
# Precio normal: $U17.542,28
# Precio sin descuento: $U28.294,00
# Nombre Producto: Resiste Pocket "Plus" (1 Plaza)
# Precio normal: $U26.094,60
# Precio sin descuento: $U41.420,00
# Nombre Producto: Eucalyptus Pocket (2 plazas)
# Precio normal: $U29.657,02
# Precio sin descuento: $U46.339,10
# Nombre Producto: Magno Vitta (2 plazas)
# Precio normal: $U28.349,20
# Precio sin descuento: $U51.544,00
# Nombre Producto: Excelsus Pocket (2 plazas)
# Precio normal: $U25.918,10
# Precio sin descuento: $U39.874,00
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: Procoluna 33 Doble Pillow (Queen)
# Precio normal: $U33.583,16
# Precio sin descuento: $U57.902,00
# Nombre Producto: Procoluna 45 Doble Pillow (Queen)
# Precio normal: $U35.653,76
# Precio sin descuento: $U61.472,00
# Nombre Producto: Premium Comfort 33 /Pillow (Queen)
# Precio normal: $U26.543,70
# Precio sin descuento: $U45.765,00
# Nombre Producto: Grand Master (Queen Size)
# Precio normal: $U26.110,00
# Precio sin descuento: $U49.264,15
# Nombre Producto: NO DISPONIBLE
# Precio normal: NO DISPONIBLE
# Precio sin descuento: NO DISPONIBLE
# Nombre Producto: Excelsus Pocket (Queen)
# Precio normal: $U36.543,65
# Precio sin descuento: $U56.221,00
# Nombre Producto: Resiste Pocket (Extra King)
# Precio normal: $U37.940,90
# Precio sin descuento: $U61.195,00
# Nombre Producto: Excelsus Pocket (Extra King)
# Precio normal: $U43.755,40
# Precio sin descuento: $U67.316,00
# Nombre Producto: Sublime Pocket (Extra King)
# Precio normal: $U41.256,60
# Precio sin descuento: $U68.761,00
#
# Process finished with exit code 0
