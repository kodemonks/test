from bs4 import BeautifulSoup
from selenium import webdriver
import random
from MySqlDB import  MySqlDBFetcher
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
RECORDS_TO_SCRAPE=5

# Delay In Number Of Seconds To Use To Slow Down The Script
time_delay = 2

#Implicit wait if JS is still rendering the HTML DOM
implicit_wait_time = 6

#PhantomJS driver used globally across all functions
driver = None
db=None
urlHistory=None

#All scraped data will be stored in this variable till
#verified and parsed properly
jobDetailList=[]


#
#Custom header used for PhantomJS driver |
#Bot detection system will find it hard to differ from normal user
#
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Connection': 'keep-alive'
           }

#
# List of User Agent's, each time driver is being instantiated
# we randomly choose one user agent for scraping
# same reason as above
#
uaList=[
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Ubuntu/10.10 Chromium/8.0.552.237 Chrome/8.0.552.237 Safari/534.10',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36',
'Mozilla/5.0 (compatible; Origyn Web Browser; AmigaOS 4.0; U; en) AppleWebKit/531.0+ (KHTML, like Gecko, Safari/531.0+)',
'Mozilla/5.0 (compatible; Origyn Web Browser; AmigaOS 4.1; ppc; U; en) AppleWebKit/530.0+ (KHTML, like Gecko, Safari/530.0+)'
]



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
    global driver
    for key, value in headers.iteritems():
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
    webdriver.DesiredCapabilities.PHANTOMJS[
        'phantomjs.page.settings.userAgent'] = random.choice(uaList)
    if driver is not None:
        return driver
    else:
        driver = webdriver.PhantomJS()
        print(driver.capabilities)
        driver.set_window_size(1120, 550)
        driver.implicitly_wait(implicit_wait_time)
        driver.set_page_load_timeout(120)#Incase something goes wrong timeout driver
        return driver




# URL mpdifier/fetcher methids

#
#  Function to create search URL for given
#  parameters as - Search Keyword + Date modified
#
def fetchUrl(keyword,days):
    keyword.replace(" ", "-")
    return "https://www.monster.ca/jobs/search/"+keyword+"_5?tm="+days


#
# Fetch absolute link
# Helpful in fetching next page link
#
def getAbsoluteNextPageLink(keyword,relativeLink):
    keyword.replace(" ", "-")
    return "https://www.monster.ca/jobs/search/" + keyword + "_5"+relativeLink

#
#Fetch Link for next page from history URL
#
def getNextAbsoluteUrl(oldUrl):
    urlFormer=oldUrl.split('=')
    try:
        urlFormer = [str(x) for x in urlFormer]
        page=urlFormer[len(urlFormer)-1]
        urlFormer.pop(len(urlFormer)-1)
        page=int(page)+1
        next_page=""
        for url in urlFormer:
            next_page=next_page+url+"="
        return next_page+str(page)
    except Exception as e:
        return urlHistory



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
# Filter scraped data and removed bad packets
# any future unhandled DOM's will be treated as bad
#
def filterInputData(inputDataList):
    length = len(inputDataList)
    i=0
    while(i<=length-1):
        if(len(inputDataList[i])!=6):
            inputDataList.pop(i)
            length=length-1
        else:
            i=i+1
    return  inputDataList




#
# Check DB_schema.sql for given details using MySQLDb class
# details for given Timestamp
#

def checkDbforDetails(title,company,location,timestamp):
    try:
        location=location.replace('\n','')
        sql = "SELECT * FROM jobs_raw where JOB_TITLE = '"+title+"' AND COMPANY_NAME = '"+company+"' AND LOCATION = '"+location+"'"
        cur = db.fetchDBdetailsforTimeStamp(sql)
        numrows = int(cur.rowcount)
        if (numrows > 0):
            return True
        else:
            return False
    except Exception as e:
        print(e)


#
# Scrape until RECORDS_TO_SCRAPE criteria is fulfilled
#
def searchForEnoughJobs(url,recordsScraped):
    global driver,jobDetailList,RECORDS_TO_SCRAPE,urlHistory

    print('(Waiting for DOM to build) Got Search page - '+str(url))
    try:
        driver.get(url)
    except Exception as e:
        print(e)
        driver=getOrCreateDriver()
        driver.get(url)
    try:
        while recordsScraped<RECORDS_TO_SCRAPE:
# Creating Soup element as it will be faster to parse / Phantomjs has rendered complete DOM
            soup = BeautifulSoup(driver.page_source, "html.parser")
            jobList = soup.find_all("div", {"class": "js_result_details-left"})
            postTime = soup.find_all('time')


            for i in range(len(jobList)):
                try:
                    singleJobDetail=[]
                    job_data = jobList[i].find_all('a')
                    title = job_data[0].span.text.strip()
                    company = job_data[1].span.text.strip()
                    location = job_data[2].span.text.strip()
                    link = job_data[0].get('href').strip()
                    timestamp = "n/a"

                    if postTime[i] is not  None:
                        if postTime[i].has_attr('datetime'):
                            timestamp=postTime[i]['datetime']
                    else:
                        print('Null :(')
                        print(postTime[i])

                    flag = checkDbforDetails(title,company,location,timestamp)
                    if(flag):
                        print('Ignoring as already in DB -  '+title)
                        continue

                    singleJobDetail.append(link)
                    singleJobDetail.append(title)
                    singleJobDetail.append(company)
                    singleJobDetail.append(location)
                    singleJobDetail.append(timestamp)

                    #Check if given detail is in our List of data
                    jobDetailList.append(singleJobDetail)
                    recordsScraped = recordsScraped+1
                    if(recordsScraped>=RECORDS_TO_SCRAPE):
                        break;

                    # print("records scraped " + str(recordsScraped))
                    print("Scraped -  "+title)
                    # print(company)
                    #print(link)
                    # print (location)
                    # print(timestamp)
                    print('----------------\n')

                except Exception as e:
                    logging.warning('There is an Exception here!! TOP job section..')
                    print(e)
                    pass

                    # Got all jobs in given page lets check DB_schema.sql if we got some duplicate
            if(recordsScraped < RECORDS_TO_SCRAPE):
                # Moving to Next page as Requirement not satisfied
                next_page_link = soup.find('a', href=True, text='Next')['href']
                urlHistory=getAbsoluteNextPageLink(keyword,next_page_link)
                print('Got Next Page link - ' + str(urlHistory))
                driver.get(urlHistory)
                driver.save_screenshot('images/Next_click'+str(randint(1,9))+'.png')
            #End of while loop
    except Exception as e:
        logging.warning('There is an Exception here!! Next page and DB_schema.sql page..')
        pass
    driver.save_screenshot('images/last-listing.png')
    return recordsScraped






#
#  Function to fetch for Job Description
#  for Given number of link selected after DB_schema.sql check
#
def fetchJobData():
    global driver
    totalPopped=0
    totalData = len(jobDetailList)
    index=0
    while(index<totalData):
        try:
            retryCounter = 0
            driver.get(jobDetailList[index][0])
            soup = BeautifulSoup(driver.page_source, "html.parser")
            jobData =  soup.find("div", {"id": "JobDescription"})
            if jobData is None:
                jobData = soup.find("div", {"id": "CJT-leftpanel"})
                if jobData is None:
                    jobData = soup.find("td", {"class": "jobdesc"})
                    if jobData is None:
                        jobData = soup.find("div", {"id": "CJT-jobdescp"})
                        if jobData is None:
                            jobData = soup.find("div", {"id": "CJT_jobBodyContent"})
                            if jobData is None:
                                jobData = soup.find("div", {"id": "jobcopy"})
                                if jobData is None:
                                    print(jobDetailList.pop(index))
                                    totalPopped=totalPopped+1
                                    totalData=totalData-1
                                    continue
            fileName = str(uuid.uuid4())+".txt"
            jobDetailList[index].append(fileName)
            if jobData is not None:
                saveToTextFile(jobData.text,fileName)
                print('Saved to file - '+fileName)
            else:
                pass
            index = index + 1
        except Exception as e:
            logging.warning('Error parsing Job Description!!')
            if(retryCounter<3):
                retryCounter=retryCounter+1
                driver=getOrCreateDriver()

            else:
                jobDetailList.pop(index)
                totalPopped=totalPopped+1
                continue

    return totalPopped



#
# Main function
#
if __name__ == "__main__":

    #Check if number of argument are two and exit if they are not
    # len = len(sys.argv)
    # if(len!=3):
    #     print('Error!!\n INVALID argument count| Required - 2, Got - '+str(len-1))
    #     sys.exit(-1)
    # keyword = sys.argv[1]
    # timeline = sys.argv[2]
    # print('Arguments are - '+keyword+" - "+timeline)

    keyword='Python'
    timeline='7'

    # Opens PhantomJS Web Driver with changed user agent
    driver  =getOrCreateDriver()
    db = MySqlDBFetcher()
    print('Phantomjs started')

    recordsScraped=0
    urlHistory=fetchUrl(keyword,timeline)
    #Searching for jobs in given page until number of Jobs required are fulfilled
    while(recordsScraped<RECORDS_TO_SCRAPE):
        recordsScraped=recordsScraped+searchForEnoughJobs(urlHistory,recordsScraped)

    #Goto each job and fetch more details from each Job + check if some of them fails coz of DOM change
        recordsSkipped=fetchJobData()
        recordsScraped=recordsScraped-recordsSkipped
        urlHistory=getNextAbsoluteUrl(urlHistory)

        #insert all new records to DB

    db.fillDBwithDetails(jobDetailList)

    print("Closing Phantomjs Driver")
    del urlHistory
    driver.quit()