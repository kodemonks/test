from bs4 import BeautifulSoup
from selenium import webdriver
import random
from MySqlDB import  MySqlDBFetcher
import logging
import sys
import uuid
from random import randint
import os
import time



# Opens Login page and fills user details and Login
def inputDataFrontPage (username, password):

# Going to use a loop where it will reload the page and try to reinput the same data until it successfully submits in order to skip any pop-ups that get in the way.
    print("Login data entered is - ")
    print(username)
    print(password)

    sucessfullySubmitted = False
    while sucessfullySubmitted == False:

# Checks If Return Location Is Available, Otherwise Unticks Return To Same Location And Inputs The Location
            try:
                driver.get("www.gmail.com")

                time.sleep(10)
                driver.find_element_by_xpath("//input[contains(@id,'Email')]").clear()
                driver.find_element_by_xpath("//input[contains(@title,'Email')]").send_keys(username)
                driver.save_screenshot('Email.png')


                driver.find_element_by_xpath("//input[contains(@id,'next')]").click()



                driver.find_element_by_xpath("//input[contains(@id,'Passwd')]").clear()
                driver.find_element_by_xpath("//input[contains(@title,'Password')]").send_keys(password)
                driver.save_screenshot('password.png')

                driver.find_element_by_xpath("//input[contains(@title,'signIn')]").click()
                driver.save_screenshot('login.png')
                sucessfullySubmitted=True
                print('All done!!')
            except Exception as e:
                print(e)
                print('Error entering username + password!!')








os.path.join(os.getcwd(), 'cookie.txt')
driver = webdriver.PhantomJS(service_args=['--cookies-file=cookies.txt'])
driver.implicitly_wait(30)
webdriver.DesiredCapabilities.PHANTOMJS[
    'phantomjs.page.settings.userAgent'] = random.choice('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246')

username="adam.ajax123@gmail.com"
password="microhacker"
inputDataFrontPage(username=username,password=password)
