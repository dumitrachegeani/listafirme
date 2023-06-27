import csv
import random
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from windscribe import windscribe
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

import const


def write_to_csv(companies, filename, bilant_filename):
    with open(filename, 'a+', newline='') as file:
        writer = csv.writer(file)
        # Writing data rows
        for company in companies:
            writer.writerow(
                [company.name, company.cui, company.nr_inmatriculare, company.euid, company.start_date,
                 company.company_description, company.state,
                 company.city, company.address, company.phones, company.fax, company.email, company.website,
                 company.caen, company.activity,
                 company.description_of_activity])

        file.flush()
    with open(bilant_filename, 'a+', newline='') as bilant_file:
        bilant_writer = csv.writer(bilant_file)
        # Writing headers (field names)
        bilant_writer.writerow(["Company Name", "Bilant"])
        # Writing data rows
        for company in companies:
            bilant_writer.writerow([company.name, company.bilant])
            bilant_file.flush()


# Function to return a random sleep time
def random_sleep():
    # windscribe.connect(rand=True)
    return random.randint(1, 3)


# The login function
def login(driver, username, password):
    driver.get("https://www.listafirme.ro/")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rememlg"]'))).click()

    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/header/div[1]/div/div[3]/div/ul/li/div/form/input[1]')))
    username_field.send_keys(username)

    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/header/div[1]/div/div[3]/div/ul/li/div/form/input[2]')))
    password_field.send_keys(password)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/header/div[1]/div/div[3]/div/ul/li/div/form/input[3]'))).click()


class Company:
    def __init__(self, name, cui, nr_inmatriculare, euid, start_date, company_description, state, city, address, phones,
                 fax, email, website, caen, activity, description_of_activity, bilant):
        self.name = name
        self.cui = cui
        self.nr_inmatriculare = nr_inmatriculare
        self.euid = euid
        self.start_date = start_date
        self.company_description = company_description
        self.state = state
        self.city = city
        self.address = address
        self.phones = phones
        self.fax = fax
        self.email = email
        self.website = website
        self.caen = caen
        self.activity = activity
        self.description_of_activity = description_of_activity
        self.bilant = bilant

    def __str__(self):
        return f"Company Name: {self.name}, CUI: {self.cui}, Registration Number: {self.nr_inmatriculare}, EUID: {self.euid}, Start Date: {self.start_date}, Description: {self.company_description}, State: {self.state}, City: {self.city}, Address: {self.address}, Phones: {self.phones}, Fax: {self.fax}, Email: {self.email}, Website: {self.website}, CAEN: {self.caen}, Activity: {self.activity}, Description of Activity: {self.description_of_activity}, Bilant: {self.bilant}"


def process_data(firm_link, driver: WebDriver):
    random_sleep()
    driver.get(firm_link)
    randam = random.randint(100, 1000)
    driver.execute_script(f"window.scrollTo(0, {randam})")
    # Initialize all fields to an empty string
    name = cui = nr_inmatriculare = euid = start_date = company_description = state = city = address = phones = fax = email = website = caen = activity = description_of_activity = bilant = ""

    info_table = driver.find_element(By.ID, "date-de-identificare")
    trs = info_table.find_elements(By.TAG_NAME, 'tr')

    for i in range(len(trs)):
        if 'Nume firmă' in trs[i].text:
            start = len('Nume firmă')
            name = trs[i].text[start:].strip()
        if 'Cod Unic de Înregistrare' in trs[i].text:
            start = len('Cod Unic de Înregistrare')
            cui = trs[i].text[start:].strip()
        if 'Nr. Înmatriculare' in trs[i].text:
            start = len('Nr. Înmatriculare')
            nr_inmatriculare = trs[i].text[start:].strip()
        if 'EUID' in trs[i].text:
            start = len('EUID')
            euid = trs[i].text[start:].strip()
        if 'Data înfiinţării' in trs[i].text:
            start = len('Data înfiinţării')
            start_date = trs[i].text[start:].strip()

    # print(soup.find(id='marci-inregistrate').text) useless
    try:
        company_description = driver.find_element(By.ID, 'descriere-firma').text.strip()
    except:
        company_description = ""

    contact_table = driver.find_element(By.ID, "contact")
    trs = contact_table.find_elements(By.TAG_NAME, 'tr')
    for i in range(len(trs)):
        row = trs[i]
        if 'Judeţ' in row.text:
            start = len('Judeţ')
            state = row.text[start:].strip()
        if 'Localitate/Sector' in row.text:
            start = len('Localitate/Sector')
            city = row.text[start:].strip()
        if 'Adresă' in row.text:
            start = len('Adresă')
            address = row.text[start:].strip()
        if 'Mobil' in row.text:
            start = len('Mobil')
            phones = row.text[start:].strip()
        if 'Fax' in row.text:
            start = len('Fax')
            fax = row.text[start:].strip()
        if 'Email' in row.text:
            start = len('Email')
            email = row.text[start:].strip()
        if 'Adresă web' in row.text:
            start = len('Adresă web   ')
            website = row.text[start:].strip()

    activity_table = driver.find_element(By.ID, "domeniu-de-activitate")
    trs = activity_table.find_elements(By.TAG_NAME, 'tr')
    for i in range(len(trs)):
        row = trs[i]
        if 'Cod CAEN' in row.text:
            start = len('Cod CAEN')
            caen = row.text[start:].strip()
        if 'Obiect Activitate' in row.text:
            start = len('Obiect Activitate')
            activity = row.text[start:].strip()
        if 'Descriere Activitate' in row.text:
            start = len('Descriere Activitate')
            description_of_activity = row.text[start:].strip()
    try:
        bilant = driver.find_element(By.ID, 'bilant')
        bilant = bilant.text
    except:
        bilant = ""

    company = Company(name, cui, nr_inmatriculare, euid, start_date, company_description, state, city, address, phones,
                      fax, email, website, caen, activity, description_of_activity, bilant)

    return company


def parse_firms_page(driver: WebDriver):
    xpath = '/html/body/div[1]/main/section/div/table/tbody/tr'
    # one page of companies mining
    rows = driver.find_elements(By.XPATH, xpath)
    companies_list = []
    link_list = []
    for row in rows:
        try:
            a_tags = row.find_element(By.TAG_NAME, 'a')
            firm_link = a_tags.get_property('href')
        except:
            continue
        link_list.append(firm_link)

    i = 0
    for link in link_list:
        print(f'Mining {link}')

        try:
            company = process_data(link, driver)
        except Exception:
            print(f"Eroare la {link}")
            continue
        companies_list.append(company)
        i += 1
        print(f"A minat {i}/50 de pe aceasta pagina")
    write_to_csv(companies_list, 'companies.csv', 'bilant.csv')


def write_header():
    with open("companies.csv", 'a+', newline='') as file:
        writer = csv.writer(file)
        # Writing headers (field names)
        writer.writerow(
            ["Name", "CUI", "Registration Number", "EUID", "Start Date", "Description", "State", "City", "Address",
             "Phones", "Fax", "Email",
             "Website", "CAEN", "Activity", "Description of Activity"])


# Main flow
if __name__ == "__main__":
    # windscribe.login('geanyhalav', 'croco2001')

    username = const.email
    password = const.password

    ua = UserAgent()
    user_agent = ua.random

    options = Options()
    options.add_argument("start-maximized")
    options.add_argument(f'user-agent={user_agent}')

    driver = uc.Chrome(headless=False, use_subprocess=False)

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        login(driver, username, password)
        try:
            driver.switch_to.alert.accept()
        except:
            pass
        write_header()
        for i in range(1, 28157):
            # Implement the logic to go to next page
            link = f'https://www.listafirme.ro/pagini/p{i}.html'
            print(f"Scrapping page {i}")
            driver.get(link)
            parse_firms_page(driver)
            time.sleep(random_sleep())

    finally:
        driver.quit()
