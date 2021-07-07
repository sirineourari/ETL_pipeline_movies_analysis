from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import os
import csv 

BASE_DIR = os.path.dirname(__file__)

def parse_and_extract(url,year):
    
    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text
    
    # Parse HTML code for the entire site
    soup = BeautifulSoup(html_content, "lxml")
    gdp = soup.find_all("div", attrs={"class": "a-section imdb-scroll-table-inner"})
    #print(len(gdp))
    
    table1 = gdp[0]
    body = table1.find_all("tr")
    # Head values (Column names) are the first items of the body list
    head = body[0] # 0th item is the header row
    body_rows = body[1:] # All other items becomes the rest of the rows

    




    headings = []
    # loop through all th elements
    for item in head.find_all("th"): 
        # convert the th elements to text and strip "\n"
        item = (item.text).rstrip("\n")
        # append the clean column name to headings
        headings.append(item)
    #print(headings)
    
    all_rows = [] # will be a list for list for all rows
    
    for row_num in range(len(body_rows)): # A row at a time
        row = [] # this will old entries for one row
        for row_item in body_rows[row_num].find_all("td"): #loop through all row entries
            aa = re.sub("(\xa0)|(\n)|,","",row_item.text)
            #append aa to row - note one row entry is being appended
            row.append(aa)
        all_rows.append(row) 
    
    filename= year + ".csv"
    with open(filename, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        # writing the fields 
        csvwriter.writerow(headings) 
        # writing the data rows 
        csvwriter.writerows(all_rows)
    return True

"""url="https://www.boxofficemojo.com/year/world/2020/"
year="2020"
parse_and_extract(url,year)"""


start_year = "2015"
end_year = "2020"
nyears = int(end_year) - int(start_year)
  
for i in range(0, nyears+1):
    year = int(start_year) + i 
    url = f"https://www.boxofficemojo.com/year/world/{year}/"
    finished = parse_and_extract(url,str(year)) 
    if finished:
        print("Finished" + str(year))  
 

