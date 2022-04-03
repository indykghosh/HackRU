import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://scheduling.rutgers.edu/scheduling/academic-calendar'
requests.get(url)

pages = requests.get(url)
pages.text

soup = BeautifulSoup(pages.text, 'lxml')

table1 = soup.find('table')

headers=[]
for i in table1.find_all('th'):
  title = i.text
  headers.append(title)

mydata = pd.DataFrame(columns = headers)
prevFirst = ""
firstMonths = ['september','october','november','december']
hold = []
for j in table1.find_all('tr')[1:]:
  row_data = j.find_all('td')
  row = [i.text for i in row_data]
  if len(row) == 3:
    row.insert(0,prevFirst)
  counter = 0
  for data in row:
    data = data.lower()
    data = data.strip()
    if '-' in data:
      data = data[0:data.index('-')+1]
    if '–' in data:
      data = data[0:data.index('–')+1]
    if '(' in data:
      data = data[0:data.index('(')+1]
    data = repr(data).replace(r'\n',' ')
    data = data.replace(r'\t\t\t','')
    if counter != 0 :
      check = True
      yearOne = headers[counter][0:4]
      yearTwo = headers[counter][5:9]
      for m in firstMonths:
        if m in data:
          check = False
          data = data+yearOne
      if check:
        data = data + yearTwo
    row[counter] = data
    counter += 1
  length = len(mydata)
  mydata.loc[length] = row
  prevFirst = row[0]

mydata = mydata.drop(3)
mydata = mydata.drop(2)
mydata = mydata.drop(6)
mydata = mydata.drop(15)

end = ['\'thanksgiving recess end\'','\'sunday, november 28\'2021','\'sunday, november 27\'2022','\'sunday, november 26\'2023']
mydata.loc[length]=end

mydata.to_csv('calendar.csv', index=False)
mydata2 = pd.read_csv('calendar.csv')
print (mydata2)
