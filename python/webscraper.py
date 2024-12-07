import requests
import pandas as pd
from bs4 import BeautifulSoup



# Scape Main Page
def scrape_main_page(page_num):
    data = []
    base_url = "https://researchops.web.illinois.edu"
    url = base_url + "/?page=" + str(page_num)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table_rows = soup.find_all('tr')
        for row in table_rows:
            first_td = row.find('td', headers="view-title-table-column")
            if first_td:
                title_element = first_td.find('a')
                title = title_element.text.strip() if title_element else None
                description = first_td.text.strip().replace(title, "").strip() if title else None
                detail_url = base_url + title_element['href'] if title_element else None 
                description = first_td.text.strip().replace(title, "").strip() if title else None
                columns = row.find_all('td')[1:]
                other_data = [column.text.strip() for column in columns]
                
                row_data = [title, description, detail_url] + other_data
                data.append(row_data)
    return data



# sraping webpage
def scrape_detail_page(row):
    full_data = []
    detail_url = row['Detail URL']
    detail_response = requests.get(detail_url)
    if detail_response.status_code == 200:
        detail_soup = BeautifulSoup(detail_response.content, 'html.parser')

        # extract details like sponsoring_institution, location, etc.
        def extract_field(label):
            label_div = detail_soup.find('div', class_="field__label", string=label)
            if label_div:
                value_div = label_div.find_next_sibling('div', class_="field__item")
                return value_div.text.strip() if value_div else None
            return None

        location = extract_field("Location")
        # Combine details of research opportunities
        full_data.append({
            "Topic": row["Topic"],
            "Description": row["Description"],
            "Research Area": row["Research Area"],
            "Opportunity Timing": row["Opportunity Timing"],
            "Deadline Date": row["Deadline Date"],
            "Location": location
        })
    return full_data