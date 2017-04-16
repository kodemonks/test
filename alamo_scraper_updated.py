from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time

# Delay In Number Of Seconds To Use To Slow Down The Script
time_delay = 6


class carOffer():
    def __init__(self, name, price, wprice, snprice, snwprice):
        self.name = name
        self.price = price
        self.wprice = wprice
        self.snprice = snprice
        self.snwprice = snwprice


# This function removes "\n" at the end of strings. Input must be a list of strings + removes empty lines
def removenewline (lines):
    lines = map(lambda line: line.replace("\n",""), lines)
    return filter(None, lines)

def cleanLine(line):
    return line.replace('\n', ' ').replace('\r', '')


# Opens front page and inputs data
def inputDataFrontPage (pickUpLocation, returnLocation, pickUpDate, returnDate, pickUpTime, returnTime):
    
    print "- - Input data - -"
    print pickUpLocation
    print returnLocation
    print pickUpDate
    print returnDate
    print pickUpTime
    print returnTime
    print '\n---\n'
    

    # Going to use a loop where it will reload the page and try to reinput the same data until it sucessfully submits in order to skip any pop-ups that get in the way.
    sucessfullySubmitted = False
    while sucessfullySubmitted == False:
        # Opens the front page
        driver.get("http://alamo.com")
        driver.set_window_size(2000, 2000)
        time.sleep(1)

        # Checks If Return Location Is Available, Otherwise Unticks Return To Same Location And Inputs The Location
        try:
            driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffLocation_searchCriteria").clear()
            driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffLocation_searchCriteria").send_keys(returnLocation)
        except:
            driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_returnToSameLocation").click()
            driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffLocation_searchCriteria").clear()
            driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffLocation_searchCriteria").send_keys(returnLocation)

        # Input the data into all of the fields
        driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_pickUpLocation_searchCriteria").clear()
        driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_pickUpLocation_searchCriteria").send_keys(pickUpLocation)
        driver.execute_script('document.getElementById("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_pickUpDateTime_date").removeAttribute("readonly")')
        driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_pickUpDateTime_date").clear()
        driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_pickUpDateTime_date").send_keys(pickUpDate)
        driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_pickUpDateTime_time").send_keys(pickUpTime)
        driver.execute_script('document.getElementById("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffDateTime_date").removeAttribute("readonly")')
        driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffDateTime_date").clear()
        driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffDateTime_date").send_keys(returnDate)
        driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffDateTime_time").send_keys(returnTime)

        # Submits The Form
        try:
            driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_insidersMember").send_keys(Keys.TAB)
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            sucessfullySubmitted = True
            print "---"
            print "Form submitted!"
        except:
            print "---"
            print "Form Failed!"
            pass


# Scrapes
def scrapeOffers():
    soup = BeautifulSoup(driver.page_source,'html.parser')
    offers = []
    # Gets All The HTML Of Each Of The Cars Into A List
    cars = soup.findAll(attrs={'class': 'cars'})
    suvs = soup.findAll(attrs={'class': 'suvs'})
    vans = soup.findAll(attrs={'class': 'vans'})
    trucks = soup.findAll(attrs={'class': 'trucks'})
    for each in suvs:
        cars.append(each)
    for each in vans:
        cars.append(each)
    for each in trucks:
        cars.append(each)

#Check if any error
    if (len(cars) == 0):
        print('Length is - ')
        print(len(cars))
        try:
            a = soup.findAll(attrs={'class': 'error'})
            print('Error is - ')
            print(a[0].text)
        except:
            pass

#Fetching data
    for car in cars:
        try:
            # print('insode loop')
            #Fetching Vehicle Name
            name = car.find(attrs={'class': 'car-description'}).text.split("Auto")[0]
            name=cleanLine(name)
            # print('Name passed')

            #Fetching Vehicle Price
            try:
                wprices = car.findAll(attrs={'class': 'amount'})
                wprice1 = wprices[0].text
                dayOrWeek = wprices[0].findNext('span').contents[0]
                wprice1 = wprice1 +" "+dayOrWeek
            except:
                try:
                    #Incase we have single section
                    wprices = car.findAll(attrs={'class': 'amt'})
                    wprice1 = wprices[0].text
                    wprice1=cleanLine(wprice1)
                except:
                    print('')
            #Fetching total price
            prices = car.findAll(attrs={'class': 'total modal'})
            price1 = prices[0].text.split("Total:")[1].split("IE7")[0]
            new_price1 = price1.split('\n', 1)[0]
            try:
                price2 = prices[1].text.split("Total:")[1].split("IE7")[0]
                new_price2 = price2.split('\n', 1)[0]
                wprice2 = wprices[1].text
                new_wprice2= wprice2.split('\n', 1)[0]

            except:
                new_price2 = "None"
                new_wprice2 = "None"

            print 'Success SCraping \n Name - ' + name
            print 'TPrice - ' + new_price1
            print 'Price - ' + wprice1
            print 'PNS total - ' + new_price2
            print 'PNS price - ' + new_wprice2 + '\n----'
            offers.append(carOffer(name, new_price1, wprice1, new_price2, new_wprice2))
        except:
            print('')
            pass


    return offers




if __name__ == "__main__":
    with open("input.csv", "rb") as f:
        reader = csv.reader(f)
        wfile = open("results.csv", "w")
        writer = csv.writer(wfile)
        writer.writerow(["Name", "Total Price", "Price", "Pay Now & Save Total Price", "Pay Now & Save Price", "Pick Up Location", "Return Location", "Pick Up Date", "Return Date", "Pick Up Time", "Return Time"])
        wfile.close()
        
        
        # Storing Our Input Data From The Input Files
        pickUpLocations = []
        returnLocations = []
        pickUpDates = []
        returnDates = []
        pickUpTimes = []
        returnTimes = []
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
                                except:
                                    print('Form error')
                                    continue                                   
                                wfile = open("results.csv", "a")
                                writer = csv.writer(wfile)
                                print "Pausing For " + str(time_delay) + " Seconds To Slow Down The Script! Write one "
                                time.sleep(time_delay)
                                pageOffers = scrapeOffers()

                                #Retry once in case of a failure
                                if(len(pageOffers)==0):
                                    print('No data!! Retrying same input!!')
                                    inputDataFrontPage(pul, rl, pud, rd, put, rt)
                                    print "Pausing For " + str(time_delay) + " Seconds To Slow Down The Script! Write one "
                                    time.sleep(time_delay)
                                    pageOffers = scrapeOffers()

                                for each in pageOffers:
                                    # Add each offer to spreadsheet
                                    writer.writerow([each.name, each.price, each.wprice, each.snprice, each.snwprice, pul, rl, pud, rd, put, rt])
                                wfile.close()
                                print('Done here!!\n')
        wfile.close()
        driver.quit()