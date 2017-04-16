from bs4 import BeautifulSoup
from selenium import webdriver
import random
import logging
import sys
import uuid
from random import randint


#
# Handle encoding issues by using utf-8 encoding
#
reload(sys)
sys.setdefaultencoding('utf-8')



#
#Saving all error/warning logs to given file
#Change here for change in log filename or Log LEVEL
#
logging.basicConfig(filename='MonsterJobs.log',level=logging.DEBUG)


#Change here for number of records to scrape in a go
RECORDS_TO_SCRAPE=3

# Delay In Number Of Seconds To Use To Slow Down The Script
time_delay = 2

#Implicit wait if JS is still rendering the HTML DOM
implicit_wait_time = 6

#All scraped data will be stored in this variable till
#verified and parsed properly
jobDetailList=[]

HOMEPAGE = 'https://www.youtube.com'

#
# Clean some strings - remove encodings - filter spl char
# remove few encoding and as parsed data is single line so -
# make it more readable
#
def cleanLine(inputLine):
    if inputLine is not None:
        inputLine = inputLine.replace(".",". \n")
        inputLine = inputLine.replace(".",". \r")
        return inputLine.encode('ascii', 'ignore').decode('ascii','ignore')



#
#Function creates a new driver or returns an existing driver if any
#using custom header and User Agent
#
def getOrCreateDriver():
        driver = webdriver.PhantomJS()
        driver.set_window_size(1120, 550)
        driver.implicitly_wait(implicit_wait_time)
        driver.set_page_load_timeout(120)#Incase something goes wrong timeout driver
        return driver




# URL mpdifier/fetcher methids

#
#  Function to create search URL for given
#  parameters as - Search Keyword + Date modified
#
#
# Fetch absolute link
# Helpful in fetching next page link
#
def getAbsoluteNextPageLink(keyword,relativeLink):
    keyword.replace(" ", "-")
    return "https://www.monster.ca/jobs/search/" + keyword + "_5"+relativeLink




#
# Function to save Job data to a text file with given name
# clean text file data, remove errors, format and save to folder
#
def saveToTextFile(jobDescription,fileName):
    jobDescription=cleanLine(jobDescription)
    f = open("outputJobs/"+fileName, "w")
    f.write(jobDescription + '\n')
    f.close()





#
# Scrape until RECORDS_TO_SCRAPE criteria is fulfilled
#
def searchForEnoughJobs(driver,url,recordsScraped):
    print('(Waiting for DOM to build) Got Search page - '+str(url))
    try:
        driver.get(url)
    except Exception as e:
        print(e)
        driver=getOrCreateDriver()
        driver.get(url)
    try:
    # Creating Soup element as it will be faster to parse / Phantomjs has rendered complete DOM
            soup = BeautifulSoup(driver.page_source, "html.parser")
            channelSpan = soup.find("span", {"class": "qualified-channel-title-text"})
            channelLink  = channelSpan.find("a")['href']

            channelLink = HOMEPAGE + channelLink
            print(channelLink)

            channelName = channelSpan.find('a').text
            print(channelName)

        #     Moving to Next page as Requirement not satisfied
            next_page_link = soup.find("ul",{"class":'branded-page-related-channels-list'})
            # print(next_page_link)
            next_page_link= next_page_link.find_all('li')
            # print(next_page_link)
            for channel in next_page_link:
               title = channel.span
               linker = title.find("a")['href']
               titler = title.find("a").text
               print(linker)
               print(titler)

            driver.save_screenshot('images/Next_click'+str(randint(1,9))+'.png')
        #    End of while loop
    except Exception as e:
        logging.error('There is an Exception here!! Next page and DB_schema.sql page..')
        pass
    driver.save_screenshot('images/last-listing.png')
    return recordsScraped





#
# Main function
#
if __name__ == "__main__":
#   Check if number of argument are two and exit if they are not
#     length = len(sys.argv)
#     if(length!=3):
#         print('Error!!\n INVALID argument count| Required - 2, Got - '+str(length-1))
#         sys.exit(-1)
#     keyword = sys.argv[1]
#     timeline = sys.argv[2]
#     print('Arguments are - '+keyword+" - "+timeline)



# Opens PhantomJS Web Driver with changed user agent
    driver  =getOrCreateDriver()

    recordsScraped=0
    url=HOMEPAGE+"/channel/UCdxi8d8qRsRyUi2ERYjYb-w"

    #Searching for jobs in given page until number of Jobs required are fulfilled
    recordsScraped=searchForEnoughJobs(driver,url,recordsScraped)

        #insert all new records to DB

    print("All scraping done total records scraped  ")
    print("Closing Phantomjs Driver")
    driver.quit()

