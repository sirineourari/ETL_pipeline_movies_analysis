from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import datetime
import os
import sys
import csv 

def parse_and_extract(url):
    
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
    #loop through all row entries
    for row_item in body_rows[row_num].find_all("td"): 
        # row_item.text removes the tags from the entries
        # the following regex is to remove \xa0 and \n and comma from row_item.text
        # xa0 encodes the flag, \n is the newline and comma separates thousands in numbers
        aa = re.sub("(\xa0)|(\n)|,","",row_item.text)
        #append aa to row - note one row entry is being appended
        row.append(aa)
    # append one row to all_rows
    all_rows.append(row)
    #df = pd.DataFrame(data=all_rows,columns=headings)
    #print(df.head())
    
    # name of csv file 
    filename = "year.csv"
    # writing to csv file 
    with open(filename, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        
        # writing the fields 
        csvwriter.writerow(headings) 
        
        # writing the data rows 
        csvwriter.writerows(all_rows)

    
def run(start_year=None, years_ago=0):
    if start_year == None:
        now = datetime.datetime.now()
        start_year = now.year
    assert isinstance(start_year, int)
    assert isinstance(years_ago, int)
    assert len(f"{start_year}") == 4
    for i in range(0, years_ago+1):
        url = f"https://www.boxofficemojo.com/year/world/{start_year}/"
        finished = parse_and_extract(url, name=start_year)
        if finished:
            print(f"Finished {start_year}")
        else:
            print(f"{start_year} not finished")
        start_year -= 1

if __name__ == "__main__":
    try:
        start = int(sys.argv[1])
    except:
        start = None
    try:
        count = int(sys.argv[2])
    except:
        count = 0
    run(start_year=start, years_ago=count)
