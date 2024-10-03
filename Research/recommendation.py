import json
import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
data = []
for i in range(0, 9):
    url = "https://researchops.web.illinois.edu/?page=" + str(i)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')  # Parse HTML content of the page

        table_rows = soup.find_all('tr')  # Find all table rows if the data is in a table

        for row in table_rows:
            columns = row.find_all('td')
            row_data = [column.text.strip() for column in columns]
            if row_data:  # Avoid appending empty rows
                data.append(row_data)

df = pd.DataFrame(data, columns=["Description", "Research Area", "Opportunity Timing", "Deadline Date"])
print(df.head)