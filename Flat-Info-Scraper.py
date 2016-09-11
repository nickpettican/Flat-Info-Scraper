#!/usr/bin/env python
'''                     
        Copyright 2016 Nicolas Pettican

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

                    '''

import os
import csv
import requests
from bs4 import BeautifulSoup

DATADIR = "C:\Users\User\Documents\FindFlat2016"
OUTFILE = "flats.csv"
URLFILE = "urls.csv"
    
def webscraper(urls):
    # scrapes the url you input
    # currently only works with RightMove and Prime Location
    all_flats = [['Address', 'Price', 'Telephone', 'Date available', 'Deposit']]
    for url in urls:
        try:
            website = requests.get(url)
            flat = BeautifulSoup(website.content, 'lxml')
            #print flat.prettify()
            if 'rightmove' in url:
                flat = scrape_rightmove(flat)
            elif 'primelocation' in url:
                flat = scrape_prime_location(flat)
            all_flats.append(flat)
            print 'Flat added\n'
        except:
            print 'Error in pulling information from %s\n' %(url)
            continue
    return all_flats

def scrape_rightmove(flat):
    # scrapes Rightmove.com listings
    # header contains address and price
    header = flat.find_all('div', {'class': 'property-header-bedroom-and-price'})
    address = [item.find_all('address') for item in header][0][0].text
    priceraw = [item.find_all('p', {'id': 'propertyHeaderPrice'}) for item in header][0][0].text
    price = ' '.join(priceraw.split())
    key_info = flat.find_all('div', {'id': 'lettingInformation'})[0]
    extra_information = extra_info(key_info)
    telephone = flat.find_all('a', {'class': 'branch-telephone-number'})[0].text
    # order and sort the data
    flat_info_raw = sort_data(address,price,telephone,extra_information)
    flat_info = [item.encode('latin-1').strip("\n") for item in flat_info_raw]
    return flat_info
    
def scrape_prime_location(flat):
    # scrapes PrimeLocation.com listings
    # under development
    address = flat.find_all('h2', {'class': 'listing-details-h1'})[0].text
    priceraw = flat.find_all('div', {'class': 'listing-details-price text-price'})[0].text
    price = ' '.join(priceraw.split())
    telephone = flat.find_all('meta', {'property': 'og:phone_number'})[0].get('content')
    extra_information = ['N/A']
    # order and sort the data
    flat_info_raw = sort_data(address,price,telephone,extra_information)
    flat_info = [item.encode('latin-1').strip("\n") for item in flat_info_raw]
    return flat_info

def sort_data(address,price,telephone,extra_information):
    # sorts the flat information into one list
    flat_info = []
    flat_info.append(address)
    flat_info.append(price)
    flat_info.append(telephone)
    for item in extra_information:
        if 'available' in item[0]:
            flat_info.append(item[1])
    for item in extra_information:
        if 'Deposit' in item[0]:
            flat_info.append(item[1])
    return flat_info
    
def extra_info(key_info):
    # returns the data within an html table
    extra_information = []
    table = key_info.find('tbody')
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [element.text.strip() for element in cols]
        extra_information.append([element for element in cols if element])
    return extra_information

def outputfile(flatfile, flats):
    # outputs all flat information to a CSV
    writer = csv.writer(flatfile)
    writer.writerows(flats)
    flatfile.close()
    print '\n**Successfully created file**\n'

def main():
    outfile = os.path.join(DATADIR, OUTFILE)
    urlfile = os.path.join(DATADIR, URLFILE)
    flatfile = open(outfile, 'wb')
    urls = [line.strip() for line in open(urlfile, 'r')]
    #flats = [['location', 'here'], ['price', 'thismuch'], ['startday', 'now']]
    flats = webscraper(urls)
    outputfile(flatfile, flats)
    
if __name__ == "__main__":
    print '**A very simple web scrapper**\n    By Nicolas Pettican\n\n'
    main()