# Property Information Scraper
To gather general information from real-estate sites RightMove and PrimeLocation

## Motivation

While I was looking for flats to move to I wanted an easy way to write down the address, telephone number, price and other info. At the same time I was eager to try out the python libraries **Requests** and **BeautifulSoup**, and so I created this script!

## Functionality

The functionality is quite limited, being currently tailored for rightmove.com and primelocation.com. 

- It pulls the source code and looks for key elements, returning the information
- It requires an input file ```urls.csv``` for the urls
- It outputs a CSV file with all the information
