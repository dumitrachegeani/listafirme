import random
import time

import undetected_chromedriver as uc
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from windscribe import windscribe

import const
from const import write_header, Company, write_to_csv, selectCompanyLink

windscribe_locations = windscribe.locations()
# Function to return a random sleep time
def random_sleep():
    return random.randint(1, 2)


# The login function
def login(driver):
    username = const.email
    password = const.password
    try:

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
        try:
            time.sleep(3)
            driver.switch_to.alert.accept()
        except:
            pass
    except:
        pass


# Scrapes one firm page and create the Company object
def process_data(firm_link: str, driver: WebDriver) -> Company:
    driver.get(firm_link)
    random_scroll(driver)

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


def random_scroll(driver):
    randam = random.randint(0, 1080)
    driver.execute_script(f"window.scrollTo(0, {randam})")


def scrape_one_page(driver: WebDriver):
    xpath = '/html/body/div[1]/main/section/div/table/tbody/tr'
    # one page of companies mining
    rows = driver.find_elements(By.XPATH, xpath)
    companies_list = []
    link_list = []

    # get all links from page first
    for row in rows:
        exception_occurred, firm_link = selectCompanyLink(row)
        if exception_occurred:
            continue
        link_list.append(firm_link
                         )
    # go and scrape every link
    for j in range(len(link_list)):
        link = link_list[j]
        if j % 3 == 0:
            changeVPn()
        try:
            company = process_data(link, driver)
        except Exception:
            print(f"Eroare la {link}")
            changeVPn()
            j = j-1
            continue # without incrementing J

        companies_list.append(company)

    write_to_csv(companies_list, 'companies.csv', 'bilant.csv')



def changeVPn():
    global last_location_index
    last_location_index += 1
    if last_location_index < len(windscribe_locations):
        windscribe.connect(windscribe_locations[last_location_index])
    else:
        last_location_index = 0
        windscribe.connect(windscribe_locations[last_location_index])

# Main flow
if __name__ == "__main__":
    windscribe.login('geanyhalav', 'croco2001')

    driver = uc.Chrome(headless=False, use_subprocess=False)
    global last_location_index
    last_location_index = 0
    try:
        write_header()
        for i in range(14, 28157):
            # Go to page, login, get all data of 50 firms, switch IP
            link = f'https://www.listafirme.ro/pagini/p{i}.html'
            print(f"Scrapping page {i}")
            driver.get(link)
            login(driver)
            scrape_one_page(driver)
            windscribe.connect(rand=True)
    finally:
        driver.quit()
