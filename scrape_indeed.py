import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd

# Function to extract data from website
def extract(page):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
    base_url = f'https://in.indeed.com/jobs?q=Analyst&start={page}'
    r = requests.get(base_url,headers)
    soup = BeautifulSoup(r.content,'lxml')
    return soup

# Function to transform extracted data
def transform(soup):
    divs = soup.find_all('div',class_ = 'job_seen_beacon')
    for item in divs:
        title = item.find('a').text
        company = item.find('span',class_ = 'companyName').text
        location = item.find('div', class_ = 'companyLocation').text
        try:
            salary = item.find('div',class_ = 'metadata salary-snippet-container').text.strip()
        except:
            salary= ''
        summary = item.find('div', {'class' : 'job-snippet'}).text.strip().replace('\n','')
        job = {
            'title' : title,
            'company': company,
            'salary' : salary,
            'summary': summary,
            'location' : location
            }
        jobslist.append(job)
    return

# Extracting data from many pages
jobslist = []
for i in range(0,5640,10):

    c = extract(i)
    transform(c)

# Loading data into dataframe    
JobData = pd.DataFrame(jobslist)

joblocale = JobData['location']


Keys = ['Chennai, Tamil Nadu', 'Bangalore, Karnataka' ,'Gurgaon, Haryana', 'Hyderabad, Telangana', 'Pune, Maharashtra', 'Mumbai, Maharashta', 'Remote']


for i in range(0,len(joblocale)):
    for x in range(0,len(Keys)):
        if Keys[x] in joblocale[i] or Keys[x] in joblocale[i]:
            joblocale[i] = Keys[x]
            break
        
JobData['location'] = joblocale

JobData.to_csv('Job_Data.csv', index = False)

len(JobData)














