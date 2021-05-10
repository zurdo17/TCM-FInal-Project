import csv
import requests
from bs4 import BeautifulSoup

# temp_url = 'https://www.studentdoctor.net/schools/school/emory/survey/26/emory-university-school-of-medicine/1'

#this file will output a csv file called question_data.csv. 
#This csv file will be necessary to run the main program, as it contains all interview questions for all medical schools.

#First part extract all medical schools in the SDN Database
root_url = "https://www.studentdoctor.net/schools/schools/2/allopathic-medical-school-rankings/"
root_soup = BeautifulSoup(requests.get(root_url).content, "html.parser")
table = root_soup.select('table', class_='sdn-school-table')
a_tags = table[0].select('a')
base_url_list = []
for anchor in a_tags:
    if anchor.get('href') is not None:
        base_url_list.append(anchor.get('href'))

#Then, it obtains the URL's from all the medical schools where all interview questions are located.    
url_list = []
for base_url in base_url_list:
    base_url_soup = BeautifulSoup(requests.get(base_url).content, 'html.parser')
    anchor = base_url_soup.findAll('a', text = 'View All Questions & Responses', attrs = { 'class': 'sdn-button'})
    url = anchor[0].get('href')
    print('found url: ', url)
    url_list.append(url)

#Then, obtains all questions from all the URLs found in the previous scrape.    
question_list = []
for url in url_list:
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
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

#Writes the csv file from which the main program extracts the questions from.
#It is able to write since all Schools and all questions have been stored in lists.
with open('question_data.csv', mode='w') as question_data_file:
    question_writer = csv.writer(question_data_file, delimiter=',')
    for question in question_list:
        question_writer.writerow(question)
