import csv

from selenium.webdriver.common.by import By

email='Florinciobanu91@yahoo.com'
password='16Florin!'


def write_header():
    with open("companies.csv", 'a+', newline='') as file:
        writer = csv.writer(file)
        # Writing headers (field names)
        writer.writerow(
            ["Name", "CUI", "Registration Number", "EUID", "Start Date", "Description", "State", "City", "Address",
             "Phones", "Fax", "Email",
             "Website", "CAEN", "Activity", "Description of Activity"])


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


def selectCompanyLink(row):
    exception_occurred = False
    try:
        a_tags = row.find_elements(By.TAG_NAME, 'a')
        a_tag = a_tags[1]  # prima e ceva nota
        if '/nota.asp' in a_tag.text:  # daca e anomalie schimbam
            print("anomaliie!")
            a_tag = a_tags[0]

        firm_link = a_tag.get_property('href')
    except:
        exception_occurred = True
        firm_link = None
    return exception_occurred, firm_link
