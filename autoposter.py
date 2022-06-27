## how can i hide my ip address so craigslist doesn"t ban me?
## more-cl-zipcodes.txt is the originial file from https://github.com/coventry/cl-zip-codes
# selenium tutorial: https://towardsdatascience.com/using-python-and-selenium-to-automate-filling-forms-and-mouse-clicks-f87c74ed5c0f


from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
# import re 
import os
import pandas as pd

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

def zipcode_mods():
	#open both files
	with open('more-cl-zipcodes.txt','r') as original, open('working_zipcodes.txt','a') as copy:
	# read content from first file
		for line in original:
		# append content to second file
			copy.write(line)
	
	df_zips = pd.read_csv("working_zipcodes.txt", header = None , sep=" ", names = ['sub_geo', 'zipcode'] )

	df_urls = pd.DataFrame (sub_geo_urls, columns = ['sub_geo_url'])
	url_series = pd.Series(df_urls['sub_geo_url'])
	
	# this pulls the regional name of the substring of for the url
	url_series = url_series.str.split(r"https://|.craigslist.org", expand=True)	
	# and append it to the url dataframe
	df_urls['sub_region_name'] = url_series[1]
	
	# join the two dataframes together

	df_url_zip = pd.merge(left=df_urls, right=df_zips, how='left', left_on='sub_region_name', right_on='sub_geo')
	
	df_url_zip['row_num'] = df_url_zip.sort_values(['zipcode'], ascending=False)\
		.groupby(['sub_geo_url'])\
		.cumcount() + 1
    # kb - are these the best zipcodes for the subregions?
	df_url_zip_unique = df_url_zip[df_url_zip['row_num'] == 1]
	df_final = df_url_zip_unique[['sub_reg_url', 'zipcode']]
	
	return df_url_zip_unique


# def clickity_clicks():

test_url = 'https://northernwi.craigslist.org'

# this brings in details of the post
import post_content 

driver = webdriver.Chrome(ChromeDriverManager().install())
			# driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(test_url)

driver.find_element(By.LINK_TEXT,'create a posting').click()
			# create_post = driver.find_element_by_link_text('create a posting')
			# # perform click
			# create_post.click()
time.sleep(20)

driver.find_element(By.CSS_SELECTOR, "input[type='radio'][value='c']").click()
			# click_community = driver.find_element_by_css_selector("input[type='radio'][value='c']").click()
time.sleep(7)

driver.find_element(By.CSS_SELECTOR, "input[type='radio'][value='3']").click()
			# click_general_community = driver.find_element_by_css_selector("input[type='radio'][value='3']").click()
time.sleep(8)

# xpaths for post input fields
posting_title_input = '//*[@id="PostingTitle"]'
postal_code_input = '//*[@id="postal_code"]'
post_body_input = '//*[@id="PostingBody"]'

# free use free email address 
email_input = '//*[@id="new-edit"]/div/fieldset[1]/div/div/div[1]/label/label/input'

# select privacy radio button
driver.find_element(By.CSS_SELECTOR, "input[type='radio'][value='A']").click()
			# driver.find_element_by_css_selector("input[type='radio'][value='A']").click()
time.sleep(15)

driver.find_element(By.XPATH,posting_title_input).send_keys(post_content.post_title)
			# driver.find_element_by_xpath(posting_title_input).send_keys(post_content.post_title)
time.sleep(20)

driver.find_element(By.XPATH,post_body_input).send_keys(post_content.post_description)
			# driver.find_element_by_xpath(post_body_input).send_keys(post_content.post_description)
time.sleep(60)

			# driver.find_element_by_xpath(login_submit).click()

time.sleep(20)
driver.quit()





reg_url()
class_strings()
sub_reg_url()
zipcode_mods()

