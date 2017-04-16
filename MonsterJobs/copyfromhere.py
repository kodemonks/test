from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import csv

# Delay In Number Of Seconds To Use To Slow Down The Script
time_delay = 6


class carOffer():
    def __init__(self, name, weekPrice, totalPrice):
        self.name = name
        self.weekPrice = weekPrice
        self.totalPrice = totalPrice


# This function removes "\n" at the end of strings. Input must be a list of strings.
def removeNewLine (lines):
    return map(lambda line: line.replace("\n",""), lines)



# Opens front page and inputs form data
def inputDataFrontPage (pickUpLocation, returnLocation, pickUpDate, returnDate, pickUpTime, returnTime):

    # Going to use a loop where it will reload the page and try to reinput the same data until it sucessfully submits in order to skip any pop-ups that get in the way.
    print("Input is - ")
    print(pickUpLocation)
    print(returnLocation)
    print(pickUpDate)
    print(returnDate)
    print(pickUpTime)
    print(returnTime)

    sucessfullySubmitted = False
    while sucessfullySubmitted == False:
        try:
            driver.get("http://nationalcar.com")
            time.sleep(2)

            # Checks If Return Location Is Available, Otherwise Unticks Return To Same Location And Inputs The Location
            try:
                driver.find_element_by_id("_content_nationalcar_com_en_US_car_rental_home_jcr_content_cq_colctrl_lt30_c1_start_dropOffLocation_searchCriteria").clear()
                driver.find_element_by_id("_content_nationalcar_com_en_US_car_rental_home_jcr_content_cq_colctrl_lt30_c1_start_dropOffLocation_searchCriteria").send_keys(returnLocation)
            except:
                driver.find_element_by_class_name("lblReturnToSameLocation").click()
                driver.find_element_by_id("_content_nationalcar_com_en_US_car_rental_home_jcr_content_cq_colctrl_lt30_c1_start_dropOffLocation_searchCriteria").clear()
                driver.find_element_by_id("_content_nationalcar_com_en_US_car_rental_home_jcr_content_cq_colctrl_lt30_c1_start_dropOffLocation_searchCriteria").send_keys(returnLocation)

            # Input Pickup Location
            driver.find_element_by_id("_content_nationalcar_com_en_US_car_rental_home_jcr_content_cq_colctrl_lt30_c1_start_pickUpLocation_searchCriteria").clear()
            driver.find_element_by_id("_content_nationalcar_com_en_US_car_rental_home_jcr_content_cq_colctrl_lt30_c1_start_pickUpLocation_searchCriteria").send_keys(pickUpLocation)


            # Execute Javascript To Remove Read-Only From Pickup/Return Date So We Can Input Dates Of Our Own
            driver.execute_script('document.getElementById("_content_nationalcar_com_en_US_car_rental_home_jcr_content_cq_colctrl_lt30_c1_start_pickUpDateTime_date").removeAttribute("readonly")')
            driver.execute_script('document.getElementById("_content_nationalcar_com_en_US_car_rental_home_jcr_content_cq_colctrl_lt30_c1_start_dropOffDateTime_date").removeAttribute("readonly")')
            # Input PickUp Date
            driver.find_element_by_id("_content_nationalcar_com_en_US_car_rental_home_jcr_content_cq_colctrl_lt30_c1_start_pickUpDateTime_date").clear()
            driver.find_element_by_id("_content_nationalcar_com_en_US_car_rental_home_jcr_content_cq_colctrl_lt30_c1_start_pickUpDateTime_date").send_keys(pickUpDate)
            # Input Return Date
            driver.find_element_by_id("_content_nationalcar_com_en_US_car_rental_home_jcr_content_cq_colctrl_lt30_c1_start_dropOffDateTime_date").clear()
            driver.find_element_by_id("_content_nationalcar_com_en_US_car_rental_home_jcr_content_cq_colctrl_lt30_c1_start_dropOffDateTime_date").send_keys(returnDate)


            # Input Pickup Time
            driver.find_element_by_name("pickUpDateTime.time").send_keys(pickUpTime)
            # Input Return Time
            driver.find_element_by_name("dropOffDateTime.time").send_keys(returnTime)

            # Submits The Form
            try:
                driver.find_element_by_id("_content_nationalcar_com_en_US_car_rental_home_jcr_content_cq_colctrl_lt30_c1_start_submit").click()
                sucessfullySubmitted = True
                print('Form filled and submitted!')
            except:
                print('Form Failed')
                pass

        except:
            pass



# Scrape offers section
def scrapeOffers():
    soup = BeautifulSoup(driver.page_source,'html.parser')
    offers = []

    # Gets All The HTML Of Each Of The Cars Into A List
    cars = soup.findAll(attrs={'class': 'vehicleWrapper'})
    # Scrapes The Data From Each Car's HTML

    if(len(cars)==0):
        a= soup.findAll(attrs={'class': 'error'})
        print('Error is - ')
        print(a[0].text)


    for car in cars:
        try:
            name = str(car.find(attrs={'class': 'close'})).split('name">')[1].split("</h3>")[0]
            prices = car.find(attrs={'class': 'priceInfo'}).text.split("IE7")[0]
            new_wprice = car.find(attrs={'class': 'priceInfo'}).text.split('\n')[1]
            regexedPrices = re.findall("\$\d\d\d?\d?\d?\.\d\d?", prices)
            wprice = regexedPrices[0]
            tprice = regexedPrices[1]

            print "Name - "+name
            print "WPrice - "+new_wprice
            print "TPrice - "+tprice

            offers.append(carOffer(name, new_wprice.encode('utf-8'), tprice))
        except:
            pass

    return offers






#Main function

if __name__ == "__main__":
    with open("input.csv", "rb") as f:
        reader = csv.reader(f)
        wfile = open("results.csv", "w")
        writer = csv.writer(wfile)
        writer.writerow(
            ["Name", "Total Price", "Price", "Pick Up Location", "Return Location", "Pick Up Date", "Return Date",
             "Pick Up Time", "Return Time"])

        # Storing Our Input Data From The Input Files
        pickUpLocations = []
        returnLocations = []
        pickUpDates = []
        returnDates = []
        pickUpTimes = []
        returnTimes = []

    #Prepare Output file
        for row in reader:
            if row[0] == "Pickup Location":
                continue
            try:
                pickupLocation = row[0]
                if pickupLocation != "":
                    pickUpLocations.append(pickupLocation)
            except:
                pass
            try:
                pickupDate = row[1]
                if pickupDate != "":
                    pickUpDates.append(pickupDate)
            except:
                pass
            try:
                pickupTime = row[2]
                if pickupTime != "":
                    pickUpTimes.append(pickupTime)
            except:
                pass
            try:
                dropOffLocation = row[3]
                if dropOffLocation != "":
                    returnLocations.append(dropOffLocation)
            except:
                pass
            try:
                dropOffDate = row[4]
                if dropOffDate != "":
                    returnDates.append(dropOffDate)
            except:
                pass
            try:
                dropOffTime = row[5]
                if dropOffTime != "":
                    returnTimes.append(dropOffTime)
            except:
                pass

            # Opens PhantomJS Web Driver
        driver = webdriver.PhantomJS()

        for pul in pickUpLocations:
            for rl in returnLocations:
                for pud in pickUpDates:
                    for rd in returnDates:
                        for put in pickUpTimes:
                            for rt in returnTimes:
                                try:
                                    inputDataFrontPage(pul, rl, pud, rd, put, rt)
                                    print('Slowing down for ' + str(time_delay) + " sec.")
                                    time.sleep(time_delay)
                                except:
                                    print('Form Failed!!')
                                pageOffers = scrapeOffers()

                                #One Rertry incase of a fail
                                if(len(pageOffers)==0):
                                    print("No data!! Retrying same input again!!")
                                    inputDataFrontPage(pul, rl, pud, rd, put, rt)
                                    print('Slowing down for ' + str(time_delay) + " sec.")
                                    time.sleep(time_delay)
                                    pageOffers = scrapeOffers()

                                for each in pageOffers:
                                   writer.writerow([each.name, each.totalPrice, each.weekPrice, pul, rl, pud, rd, put, rt])
        print(' Finished Scraping National!! ')
        wfile.close()
        driver.quit()