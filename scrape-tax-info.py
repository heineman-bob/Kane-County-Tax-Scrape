import requests
from bs4 import BeautifulSoup
import os
import json
import sys
import pandas as pd
import numpy as np

start_link = "http://kaneapplications.countyofkane.org/taxassessor/Treasurer.aspx?parcelnumber={parcel}"
info = {}

def run_application():
    with open('parcel-numbers.txt', 'r') as f:
      for line in f:
        info[f.readline().replace('-','').replace('\n','')] =''
    for key in info:
      print("attempting parcel number {number}".format(number=key))
      soup = get_soup(start_link.format(parcel=key))
      if soup:
        content = {}
        for thing in soup.find_all('span'):
            content[thing['id'][3:]] = thing.get_text()
        info[key] = content
    df = pd.DataFrame(info)
    print(df)
    df.T.to_excel('path_to_file.xlsx', sheet_name='Sheet1')
    
def get_soup(url):
    page = requests.get(url)
    if page.status_code == 200:
        return BeautifulSoup(page.content, 'html.parser')
    else:
        return False


if __name__ == '__main__':
    run_application()
