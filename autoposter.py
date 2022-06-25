## how can i hide my ip address so craigslist doesn"t ban me?
## need associated zip codes : https://github.com/coventry/cl-zip-codes

## .yml file
## pip install selenium
## pip install webdriver-manager
## pip install bs4
## pip install requests
## pip install regex

from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
import re 

# all states that ban abortions
## kb - figure out how to handle WY
states = ["al","az","ak","ga","id","ky","la","mi","ms","mo","nd","oh","ok","sc","sd","tn","tx","ut","wv","wi"]

# list of regional craigslist domains
url_prefix = "https://geo.craigslist.org/iso/us/"
geo_urls = []

def reg_url():
	for s in states:
		temp = url_prefix + s
		geo_urls.append(temp)
	return geo_urls



class_list = []

def class_strings():
	# this function creates a list that will be used to create necessary 
	# classes for pulling the urls in function sub_reg_url
	for num in range(10):
		temp_string = 'height' + str(num) + (' geo-site-list')
		class_list.append(temp_string)
	return class_list


sub_geo_urls = []

def sub_reg_url():
	# this function pulls the city-specific urls
	# kb - check to make sure that this function is pulling all of the cities from the states variable
	for g in geo_urls:
		page = requests.get(g)
		soup = BeautifulSoup(page.content, features="lxml")
		for item in class_list:
			for link in soup.find_all(class_= item):
				for l in link.find_all('a', href = True):
					sub_geo_urls.append(l['href'])

	return sub_geo_urls

test_url = 'https://northernwi.craigslist.org'

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(test_url)
create_post = driver.find_element_by_link_text('create a posting')
# perform click
create_post.click()
time.sleep(5)

click_community = driver.find_element_by_css_selector("input[type='radio'][value='c']").click()
time.sleep(5)

click_general_community = driver.find_element_by_css_selector("input[type='radio'][value='3']").click()
time.sleep(5)

driver.quit()







reg_url()
class_strings()
sub_reg_url()


