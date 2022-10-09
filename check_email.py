from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
import re 
import os
import pandas as pd
import post_content 
import secret_file
from selenium.common.exceptions import NoSuchElementException


#x_path for checking email
	
web_address = "https://account.proton.me/login"

driver = webdriver.Chrome(ChromeDriverManager().install())

# ----- sign-in section ----- #

driver.get(str(web_address))

time.sleep(19)

## username x path: 
username_input = '//*[@id="username"]'

# ## password x path: 
password_input = '//*[@id="password"]'

## signin button xpath: 

login_submit = '/html/body/div[1]/div[3]/div[1]/div/main/div[2]/form/button'

driver.find_element_by_xpath(username_input).send_keys(secret_file.email)

time.sleep(20)

driver.find_element_by_xpath(password_input).send_keys(secret_file.password)

time.sleep(20)

driver.find_element_by_xpath(login_submit).click()

time.sleep(120)

# ----- get email section ----- #

# all caught up xpath
no_messages_found = '/html/body/div[1]/div[3]/div/div[3]/div/div[2]/div/main/div/div/div/div[2]/figure/figcaption/h3'

def check_for_messages(xpath):
	try: 
		driver.find_element_by_xpath(xpath)
	except NoSuchElementException:
		return True
	return False

# print(check_for_messages(no_messages_found))


#get first email in list by xpath

while not check_for_messages(no_messages_found):

	get_top_email = '/html/body/div[1]/div[3]/div/div[3]/div/div[2]/div/main/div/div[1]/div/div[2]/div/div'

	driver.findElement(By.xpath,get_top_email).click()

	time.sleep(20)

	# # button in craigslist post
	driver.findElement(By.linkText("complete your posting")).click()

	time.sleep(20)

	# archive email

	archive_button = '/html/body/div[1]/div[3]/div/div[3]/div/div[2]/div/main/section/div/div[3]/div/div/div/article/div[1]/div[4]/div[1]/div/button[3]'

	driver.findElement(By.xpath,archive_button).click()

	time.sleep(20)

print("no such elemnt found")

# # ---- no emails found ---- # 

