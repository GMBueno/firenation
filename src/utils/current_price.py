import json
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_prices(start_date, end_date, onclick_value, file_name):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-fullscreen")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    page_content = driver.get('https://www.agron.com.br/grafico-e-tabela-de-resumo-de-cotacao-agricola-e-pecuaria-para-commodities-como-graos-de-milho-e-soja-arroba-do-boi-e-da-vaca-preco-do-bezerro-do-acucar-algodao-arroz-e-cafe-segundo-o-cepea.html')
    from_input = driver.find_element_by_id('de')
    until_input = driver.find_element_by_id('ate')
    from_input.clear()
    until_input.clear()
    from_input.send_keys(start_date)
    time.sleep(1)
    driver.find_element_by_id('botOK').click()
    until_input.send_keys(end_date)
    time.sleep(1)
    driver.find_element_by_id('pesqi').click()
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    driver.quit()
    
    soup = soup.find('table', class_='tabela_cinza')
    soup = soup.find('tbody')
    soup = soup.find_all('tr')

    data = {}
    for i in soup:
        date = i.findChildren()[0].text
        price = i.find('label', onclick=onclick_value).text
        data[date] = price
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=3)

start_date = 10112020
end_date = 20112020

# Corn data scraping
get_prices(start_date, end_date, 'redirecionarClick("Milho");', 'corn_data.json')

#Soy data scraping
get_prices(start_date, end_date, 'redirecionarClick("Soja");', 'soy_data.json')