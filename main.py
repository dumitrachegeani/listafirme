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

import const


def write_to_csv(companies, filename, bilant_filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        # Writing headers (field names)
        writer.writerow(
            ["Name", "CUI", "Registration Number", "EUID", "Start Date", "Description", "State", "City", "Address", "Phones", "Fax", "Email",
             "Website", "CAEN", "Activity", "Description of Activity"])
        # Writing data rows
        for company in companies:
            writer.writerow(
                [company.name, company.cui, company.nr_inmatriculare, company.euid, company.start_date, company.company_description, company.state,
                 company.city, company.address, company.phones, company.fax, company.email, company.website, company.caen, company.activity,
                 company.description_of_activity])

    with open(bilant_filename, 'w', newline='') as bilant_file:
        bilant_writer = csv.writer(bilant_file)
        # Writing headers (field names)
        bilant_writer.writerow(["Company Name", "Bilant"])
        # Writing data rows
        for company in companies:
            bilant_writer.writerow([company.name, company.bilant])


# Function to change the IP address
def change_ip():
    pass
    # Your code to change the IP


# Function to return a random sleep time
def random_sleep():
    return random.randint(3, 10)


# The login function
def login(driver, username, password):
    driver.get("https://www.listafirme.ro/")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rememlg"]'))).click()

    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/header/div[1]/div/div[3]/div/ul/li/div/form/input[1]')))
    username_field.send_keys(username)

    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/header/div[1]/div/div[3]/div/ul/li/div/form/input[2]')))
    password_field.send_keys(password)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/header/div[1]/div/div[3]/div/ul/li/div/form/input[3]'))).click()


class Company:
    def __init__(self, name, cui, nr_inmatriculare, euid, start_date, company_description, state, city, address, phones, fax, email, website, caen, activity, description_of_activity, bilant):
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

def process_data1(firm_link):
    with requests.Session() as s:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537'}
        response = s.get(firm_link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize all fields to an empty string
    name = cui = nr_inmatriculare = euid = start_date = company_description = state = city = address = phones = fax = email = website = caen = activity = description_of_activity = bilant = ""

    info_table = soup.find(id="date-de-identificare")
    trs = info_table.find_all('tr')
    for i in range(len(trs)):
        if 'Nume firmă' in trs[i].text:
            name = trs[i].text.split('\r\n')[2].strip()
        if 'Cod Unic de Înregistrare' in trs[i].text:
            cui = trs[i].text.split('\r\n')[2].strip()
        if 'Nr. Înmatriculare' in trs[i].text:
            nr_inmatriculare = trs[i].text.split('\r\n')[2].strip()
        if 'EUID' in trs[i].text:
            euid = trs[i].text.split('\r\n')[2].strip()
        if 'Data înfiinţării' in trs[i].text:
            start_date = trs[i].text.split('\r\n')[2].strip()

    # print(soup.find(id='marci-inregistrate').text) useless
    try:
        company_description = soup.find(id='descriere-firma').text.strip()
    except:
        company_description = ""

    contact_table = soup.find(id="contact")
    trs = contact_table.find_all('tr')
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

    activity_table = soup.find(id="domeniu-de-activitate")
    trs = activity_table.find_all('tr')
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
    bilant = soup.find(id='bilant')
    try:
        bilant = bilant.text
    except:
        bilant = ""


    company = Company(name, cui, nr_inmatriculare, euid, start_date, company_description, state, city, address, phones, fax, email, website, caen, activity, description_of_activity, bilant)

    return company


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
    bilant = driver.find_element(By.ID, 'bilant')
    try:
        bilant = bilant.text
    except:
        bilant = ""


    company = Company(name, cui, nr_inmatriculare, euid, start_date, company_description, state, city, address, phones, fax, email, website, caen, activity, description_of_activity, bilant)

    return company


def parse_firms_page(driver: WebDriver):
    xpath = '/html/body/div[1]/main/section/div/table/tbody/tr'
    # one page of companies mining
    rows = driver.find_elements(By.XPATH, xpath)
    companies_list = []
    for row in rows:
        try:
            a_tags = row.find_element(By.TAG_NAME, 'a')
            firm_link = a_tags.get_property('href')
        except:
            continue
        print(f'Mining {firm_link}')
        company = process_data(firm_link, driver)
        companies_list.append(company)
    write_to_csv(companies_list, 'companies.csv', 'bilant.csv')


# Main flow
if __name__ == "__main__":
    username = const.email
    password = const.password

    ua = UserAgent()
    user_agent = ua.random

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(chrome_options)

    try:
        login(driver, username, password)
        try:
            driver.switch_to.alert.accept()
        except:
            pass
        for i in range(1, 28157):
            # Implement the logic to go to next page
            link = f'https://www.listafirme.ro/pagini/p{i}.html'
            driver.get(link)

            parse_firms_page(driver)
            time.sleep(random_sleep())

    finally:
        driver.quit()

