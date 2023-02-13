from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.select import Select
# import csv
import queue
import threading
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import unidecode


# Lista os municipios unicos de Minas Gerais contidos na tabela Reg_Ter
"""
with open('Municipios_Unicos.csv', newline='') as f:
    csvread = csv.reader(f)
    lista_municipios = list(csvread)
"""

# Cria uma fila com os nomes dos municipios em maiusculo
fila = queue.Queue()
for i in range(853):
    aux = str(i)
    fila.put(aux)
"""
for m in lista_municipios:
    aux = str(m).upper()
    fila.put(aux)
lista_municipios.clear()
"""


def initialize_browser():
    s = Service('C:/Python311/geckodriver.exe')
    firefoxoptions = Options()
    # firefoxOptions.add_argument('-headless')
    firefoxoptions.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    driver = webdriver.Firefox(service=s, options=firefoxoptions)
    driver.maximize_window()
    driver.set_page_load_timeout(30)
    return driver


def baixa_planilha():
    driver = initialize_browser()
    while not fila.empty():
        driver.get("https://consultafns.saude.gov.br/#/detalhada")
        driver.implicitly_wait(10)
        # municipio = str(fila.get()).replace("['", '').replace("']", '')
        municipio = fila.get()

        # Retirar acentuacao
        municipio = unidecode.unidecode(municipio)

        # Seleciona o ano 2023
        seleciona_ano = driver.find_element(By.XPATH, "//select[@id='ano']")
        seleciona = Select(seleciona_ano)
        seleciona.select_by_visible_text('2023')
        driver.implicitly_wait(30)

        # Seleciona o estado Minas Gerais
        seleciona_estado = driver.find_element(By.XPATH, "//select[@id='estado']")
        seleciona = Select(seleciona_estado)
        seleciona.select_by_visible_text('MINAS GERAIS')
        driver.implicitly_wait(30)

        # Seleciona uma cidade de Minas Gerais
        seleciona_cidade = driver.find_element(By.XPATH, "//select[@id='municipio']")
        seleciona = Select(seleciona_cidade)
        # seleciona.select_by_visible_text(municipio)
        seleciona.select_by_value(municipio)
        wait = WebDriverWait(driver, 50)
        loading_overlay = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "overlayLoading")))
        wait.until(ec.invisibility_of_element(loading_overlay))

        # Clica em consultar e aguarda alguns segundos
        driver.find_element(By.XPATH, "//button[@ng-click='detalhadaCtrl.pesquisar()']").click()
        wait = WebDriverWait(driver, 50)
        loading_overlay = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "overlayLoading")))
        wait.until(ec.invisibility_of_element(loading_overlay))

        # Clica em detalhar e aguarda alguns segundos
        driver.find_element(By.XPATH, "//button[@title='Detalhar']").click()
        wait = WebDriverWait(driver, 50)
        loading_overlay = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "overlayLoading")))
        wait.until(ec.invisibility_of_element(loading_overlay))

        # Clica em Planilha Detalhada e aguarda alguns segundos
        driver.find_element(By.XPATH, "//button[@ng-click='acaoCtrl.gerarPlanilha()']").click()
        driver.implicitly_wait(10)
        time.sleep(10)

    driver.close()


# Multithreading
threads = []
for i in range(4):
    t = threading.Thread(target=baixa_planilha)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
