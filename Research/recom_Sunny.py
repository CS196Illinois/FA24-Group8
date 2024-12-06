import json
import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

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
# print(df.head)

df1 = df.drop_duplicates()
#tfidf = TfidfVectorizer()
#research_areas = df1['Research Area']
#tfidf_matrix_ra = tfidf.fit_transform(research_areas)
#cosine_similarity_ra = cosine_similarity(tfidf_matrix_ra)
#print(cosine_similarity)
#similarity_df_ra = pd.DataFrame(cosine_similarity_ra, index=df1['Description'], columns=df1['Description'])
# print(similarity_df.head)

#stu = input('Enter the research area you are interested in: ')
#research_area_index = similarity_df_ra.index.get_loc(stu)
#top_10 = similarity_df_ra.iloc[research_area_index].sort_values(ascending=False)[1:11]


tfidf = TfidfVectorizer()
description = df1['Description']
tfidf_matrix_d = tfidf.fit_transform(description)
cosine_similarity_d = cosine_similarity(tfidf_matrix_d)
# print(cosine_similarity)
similarity_df_d = pd.DataFrame(cosine_similarity_d, index=df1['Description'], columns=df1['Description'])
# print(similarity_df.head)

stu_d = input('Enter a research you are interested in: ')
research_description_index = similarity_df_d.index.get_loc(stu_d)
top_10_d = similarity_df_d.iloc[research_description_index].sort_values(ascending=False)[1:11]
print(f'Top 10 similar research to {stu_d}:')
print(top_10_d)