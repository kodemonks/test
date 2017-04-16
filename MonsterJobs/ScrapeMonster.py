from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys

# Delay In Number Of Seconds To Use To Slow Down The Script
time_delay = 6
implicit_wait_time = 10

# Opens Login page and fills user details and Login
def inputDataFrontPage (username, password):

# Going to use a loop where it will reload the page and try to reinput the same data until it successfully submits in order to skip any pop-ups that get in the way.
    print("Login data entered is - ")
    print(username)
    print(password)

    sucessfullySubmitted = False
    while sucessfullySubmitted == False:
        try:
            driver.get("https://hiring.monster.ca/login.aspx?redirect=http%3a%2f%2fhiring.monster.ca%2fdefault.aspx%3fre%3dswoop%26intcid%3dskr_navigation_swoop_hiring%26HasUserAccount%3d2%22")
            time.sleep(2)

# Checks If Return Location Is Available, Otherwise Unticks Return To Same Location And Inputs The Location
            try:
                driver.find_element_by_xpath("//input[contains(@title,'User')]").clear()
                driver.find_element_by_xpath("//input[contains(@title,'User')]").send_keys(username)
                driver.find_element_by_xpath("//input[contains(@title,'Password')]").clear()
                driver.find_element_by_xpath("//input[contains(@title,'Password')]").send_keys(password)

                print('Form Filled trying submit.')
            except:
                print('Error entering username + password!!')

# Submits The Form
            try:
                driver.save_screenshot('form_filled.png')
                driver.find_element_by_xpath("//button[contains(@title,'Sign')]").click()
                sucessfullySubmitted = True
            except:
                print('Form Failed!! Reattempt.')
                pass
        except:
            pass



# def fetchFinalData():
#     dataSetOne = driver.find_element_by_id("candidateData")
#     title = dataSetOne.find_element_by_xpath("//div[contains(@class,'candidateRecentTitle')]/span").text
#
#
#     dataSetOneA = dataSetOne.find_element_by_xpath("//div[contains(@class,'headerSubColumn')]")
#     address = dataSetOneA[1].find_element_by_xpath("//div[2]/span").text
#
#     mobile = dataSetOneA[2].find_element_by_xpath("/div[2]/span").text
#     email = dataSetOneA[2].find_element_by_xpath("//div[4]/a").text
#
#
#     resumeData = driver.find_element_by_class_name('resumeLinen')
#
#
#     print("Done here too")
#     print(title)
#     print(address)
#     print(mobile)
#     print(email)
#     print('\n\n==-------==\n\n')
#


# Scrape offers section  - All sections
def searchResume():
    print('Started scraping homepage!!')
#    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #check if it's a real login page or an error page.
    try:
        name = driver.find_element_by_id("ctl00_ctl00_ContentPlaceHolderBase_cphHomeBody_lblName").text
        print("Hello "+name)

    except:
        err = driver.find_element_by_xpath("//div[contains(@class,'validation-summary')][1]/ul/li").text
        print('An error occoured!!')
        print(err)
        pass


# #Home Page
#     try:
#         resumeLink = driver.find_element_by_xpath("//div[contains(@class,'search-resumes-btn')]/a")
#
#         print('Page-1 loaded...  Saving as Image... :D')
#         driver.save_screenshot('Homepage.png')
#
#         print(resumeLink.isDisplayed())
#         print(resumeLink.isEnabled())
#
#         print(resumeLink)
#         resumeLink.click()
#         print('I think I clicked already :D')
#         print('Waiting for ' + str(time_delay) + '  sec. for page load')
#         time.sleep(time_delay)
#     except:
#         e = sys.exc_info()[0]
#         link = driver.find_element_by_xpath("//a[contains(@title,'Sign Out')]")
#         print(link)
#         link.click()
#
#         driver.save_screenshot('ResumeList.png')
#
#         print('Error so Sign Out!!')
#         pass
#

#Search Resume Page
    try:
        driver.get('http://hiring.monster.ca//jcm/resumesearch/resumesearch.aspx')
        print('Loaded Search page!!')
        print('Page-2 loaded...  Saving as Image... :D')
        driver.save_screenshot('search-page.png')

        driver.find_element_by_xpath("//input[contains(@title,'Keyword')]").clear()
        driver.find_element_by_xpath("//input[contains(@title,'Keyword')]").send_keys('java')

        driver.find_element_by_xpath("//div[contains(@class,'topButtonContainer')]/button").click()

        print('Waiting for ' + str(time_delay) + '  sec. for page load')
        time.sleep(time_delay)

        print('Page-3 loaded...  Saving as Image... :D')
        driver.save_screenshot('search-result.png')



    except Exception as e:
        print("Error is"+ str(e))
        link = driver.find_element_by_xpath("//a[contains(@title,'Sign Out')]")
        print(link)
        link.click()
        driver.save_screenshot('signout.png')

        print('Error so Sign Out!!')
        sys.exit(1)
        pass



#Iterate User + Resume
    try:
        resumeList =  driver.find_element_by_xpath("//td[contains(@class,'geResults')]")
        print('Here list of resumes')
        print(resumeList)
        driver.save_screenshot('ResumeList.png')

        print('Page-3 loaded...  Saving as Image... :D')
        driver.save_screenshot('ResumeList.png')

        for resume in resumeList:
            print('in loop')
            compData = resume.find_element_by_id('linkResumeTitle').text
            name = compData.split('-')[0]
            print('Got complete title and fetching data now')
            title =resume.find_element_by_xpath("//div[contains(@class ,'expRecentJobTitle')]")

            print(name)
            print(title)
            print('\n-----\n')
    except Exception as e:
        print("Error is"+ str(e))
        print('Error so Sign Out!!')
        link = driver.find_element_by_xpath("//a[contains(@title,'Sign Out')]")
        print(link)
        link.click()
        driver.save_screenshot('AfterSignOut.png')
        pass

    print('Clicked search button..  Saving as Image.. :D')
    driver.save_screenshot('Search_result.png')






# Main function
if __name__ == "__main__":
    # Opens PhantomJS Web Driver with changed user agent
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 ""(KHTML, like Gecko) Chrome/15.0.87")
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver.implicitly_wait(implicit_wait_time)

    print('Phantomjs started')
    inputDataFrontPage('xnara1x11','Familyfirst5')
    print('Form filled sleeping for '+str(time_delay)+" sec. to slow down the script.")
    time.sleep(time_delay)
    searchResume()
    print('Done scraping here!!')
    driver.quit()




    # resumeLinen