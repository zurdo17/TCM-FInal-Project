import csv
import requests
from bs4 import BeautifulSoup

# temp_url = 'https://www.studentdoctor.net/schools/school/emory/survey/26/emory-university-school-of-medicine/1'

root_url = "https://www.studentdoctor.net/schools/schools/2/allopathic-medical-school-rankings/"
root_soup = BeautifulSoup(requests.get(root_url).content, "html.parser")
table = root_soup.select('table', class_='sdn-school-table')
a_tags = table[0].select('a')
base_url_list = []
for anchor in a_tags:
    if anchor.get('href') is not None:
        base_url_list.append(anchor.get('href'))

url_list = []
for base_url in base_url_list:
    base_url_soup = BeautifulSoup(requests.get(base_url).content, 'html.parser')
    anchor = base_url_soup.findAll('a', text = 'View All Questions & Responses', attrs = { 'class': 'sdn-button'})
    url = anchor[0].get('href')
    print('found url: ', url)
    url_list.append(url)

question_list = []
for url in url_list:
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    # Find university
    school_info = soup.find_all('ul', class_='school-details')
    university = "General"
    if len(school_info) > 0:
        university = school_info[0].find('li').text
    print('Looking up questions for ', university)
    for article in soup.find_all('article'):
        for question in article.select("p", class_="quote-format"):
            q = question.get_text(strip=True)
            print('found question: ', q)
            if not q.startswith('"'):
                continue
            q = q[1:].split('"')[0]
            new_question = [university, q]
            print('appending question: ', new_question)
            question_list.append(new_question)

with open('question_data.csv', mode='w') as question_data_file:
    question_writer = csv.writer(question_data_file, delimiter=',')
    for question in question_list:
        question_writer.writerow(question)
