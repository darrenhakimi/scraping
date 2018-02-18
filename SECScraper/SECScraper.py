#!/usr/bin/env python3
#################################
# script to scrape faculty names and link to profile of selected areas of expertise in CBS directory
# use selenium to simulate a browser to navigate the website 
# writes a simple txt file with a name and link per line
# go to developer console on the site and inspect html elements, look for a way of finding them: xpath,
# css selector, or by some characteristic of the element: 
#find_element_by_id
#find_element_by_name
#find_element_by_xpath
#find_element_by_link_text
#find_element_by_partial_link_text
#find_element_by_tag_name
#find_element_by_class_name
#find_element_by_css_selector
# note: use the time library to force the browser to wait between steps (if you like to see a bot browser doing stuff,
# but also, for big requests, to not make the server angry!)
################################

# %%
#import libraries
from selenium import webdriver 
from selenium.webdriver.support.ui import Select
import time
import html2text
import urllib
import pandas

from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        #self.strict = False
        #self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


with open('input.csv', 'r') as csv_file:
    df = pandas.read_csv(csv_file)
    ticker_list = df['ticker']
    ticker_list.tolist()

    for ticker in ticker_list:

        print(ticker)
        # %%
        #get a driver and go to website
        # if you would like to make it without a browser you can use "driver = webdriver.PhantomJS()"
        driver = webdriver.Safari()
        driver.get('https://www.sec.gov/cgi-bin/browse-edgar?CIK=%s' %(ticker))

        time.sleep(3)

        td_list = driver.find_elements_by_tag_name('td')
        searching_for_10K = True
        i = 0
        while searching_for_10K and (i < len(td_list)):
            if (td_list[i].text == '10-K'):
                found_10K = False
                href = td_list[i+1].find_elements_by_tag_name('a')[0]
                url_filing_detail = href.get_attribute('href')
            i = i + 1
        if not searching_for_10K:
            driver.get(url_filing_detail)
            url_10K = driver.find_element_by_xpath('//*[@id="formDiv"]/div/table/tbody/tr[2]/td[3]/a').get_attribute('href')
            driver.close()
            driver.quit()

            with urllib.request.urlopen(url_10K) as response:
                html_response = response.read()
                encoding = response.headers.get_content_charset('utf-8')
                decoded_html = html_response.decode(encoding)
            data = strip_tags(decoded_html)
            print("test")
            print(data)
        else:
            driver.close()
            driver.quit()
            print(ticker + ' did not have a 10-K.')

'''
data10Kstring = data10K.read().lower()
#data10Kstring = data10Kstring.decode('utf-8')
data10Kstring = html2text.html2text(data10Kstring)#.encode('ascii', 'ignore') 
print(data10Kstring)
'''


'''
from bs4 import *
import urllib

url = "https://www.sec.gov/Archives/edgar/full-index/2017/QTR4/company.idx"
htmlfile = urllib.request.urlopen(url)

soup = BeautifulSoup(htmlfile, 'html.parser')
'''


'''
url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=AAPL"
htmlfile = urllib.request.urlopen(url)

#htmltext = htmlfile.read()

soup = BeautifulSoup(htmlfile, 'html.parser')

rows = soup.find("table").find("tbody").find_all("tr")

for row in rows:
    cells = row.find_all("td")
    if cells[0].get_text().strip() == '10-K':
        current_10K = cells[1]['href']
        print(current_10K)
'''


