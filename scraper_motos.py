#Scraper motos.net

#libraries
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
from tools import remove_accents as ra

#BeautifulSoup object
motor_url = 'http://motos.coches.net/ocasion/?pg=1&or=-1&fi=SortDate'
motos_req = requests.get(motor_url)
motos_soup = BeautifulSoup(motos_req.text, "html.parser")

ads_number_text = motos_soup.find_all("h1", {"class": "floatleft"})
num_ads = int(re.findall(r'[^ ]*\.[^ ]*', ads_number_text[0].contents[0])[0].replace('.',''))

#There are usually thirty ads per page
ads_per_page = 30
first_page = 1
last_page = num_ads / ads_per_page

#Lets go to scrape the urls
matrioska_tb = []
matrioska_header = ['city', 'brand', 'model', 'type', 'cc', 'color', 'km', 'year', 'price']

for i in range(first_page, 5):
	sub_url = 'http://motos.coches.net/ocasion/?pg=%d&or=-1&fi=SortDate' %i
	sub_req = requests.get(sub_url, allow_redirects = False)
	print 'sub_url'
	print sub_url
	if sub_req.status_code == 200:
		sub_soup = BeautifulSoup(sub_req.text, "html.parser")
		links_list = sub_soup.find_all("a", {"class": "lnkad"}, href = True)
		print "ok link_list"
		for link in links_list:
			link_req = requests.get("http://motos.net" + link['href'])
			link_soup = BeautifulSoup(link_req.text, "html.parser")
			
			#If the ad exists, there is a h1 tag with class 'mgbottom10 floatleft'
			if len(link_soup.find_all("h1", class_= 'mgbottom10 floatleft')) != 0:
				
				title = link_soup.find_all("span", itemprop = "title")
				if len(title) == 4:
					bike_city, bike_brand, bike_model = ra(title[1].get_text()), ra(title[2].get_text()),ra(title[3].get_text())
					print bike_city, bike_brand, bike_model

					#price
					try:
						bike_price = int(''.join(re.findall(r'\b\d+\b', link_soup.find(class_='pvp').contents[0])))
					except:
						print "price error in http://motos.coches.net" + link['href']

					print bike_price

