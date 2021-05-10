from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import re
import os

PREFIX = 'https://www.zillow.com/homes/'

print(os.path.dirname(os.path.realpath(__file__)))
driver = webdriver.Chrome('resources/chromedriver')

#Get an address and return the Zillow url corresponding to this address
def get_address(address):
    address = re.sub('\W+',' ', address )
    url = address.replace(' ','-')
    return PREFIX + url+'_rb'

#Return Number of bedrooms, bathrooms and size of the appartment
def get_bd_ba_size(driver):
    element = driver.find_element_by_class_name("ds-bed-bath-living-area-container")
    infos = element.text.split()
    #print(infos)
    bd = to_decimal(infos[0])
    ba = to_decimal(infos[1][2:])
    size = int(infos[2][2:]+infos[3])
    return bd, ba, size

#Return sold date if the appartment is sold, else None
def get_sold_date(driver):
    try : 
        element =  driver.find_element_by_xpath("//*[contains(text(),'Sold on ')]")
        return element.text[-8:]
    except : 
        return None
#Return Zestimate if the appartment is sold, else None
def get_Zestimate(driver):
    element =  driver.find_element_by_xpath(".//p[@class = 'Text-c11n-8-33-0__aiai24-0 StyledParagraph-c11n-8-33-0__sc-18ze78a-0 jfHfpE']")
    res = element.text.split()[-1] 
    return res if '$' in res else None

def get_walk_Score(driver):
    return int(driver.find_element_by_xpath(".//div[@class= 'zsg-content-component']//a").text)
        
def get_transit_Score(driver):
    return int(driver.find_element_by_xpath(".//div[@class= 'zsg-content-component']//li[position()=2]//a").text)

#Return the average of GrateSchools rating
def get_GreateSchools(driver):
    i, grades =1, []
    while True:
        try :
            element = driver.find_element_by_xpath(".//div[@class= 'Spacer-c11n-8-33-0__sc-17suqs2-0 hHqwWf']//li[position()="+str(i)+"]")
            grades.append(int(element.text[0]))
        except:
            break
        i+=1
    return round(np.average(grades),2)

def get_info(address):
    url = get_address(address)
    
    driver.get(url)
    #time.sleep(15)
    #bt_submit = driver.find_element_by_css_selector("[type=submit]")

# wait for the user to click the submit button (check every 1s with a 1000s timeout)
    #WebDriverWait(driver, timeout=15, poll_frequency=1).until(EC.staleness_of(bt_submit))

    lst = []
    lst += get_bd_ba_size(driver)
    lst.append(get_sold_date(driver))
    lst.append(get_Zestimate(driver))
    lst.append(get_walk_Score(driver))
    lst.append(get_transit_Score(driver))
    lst.append(get_GreateSchools(driver))
    return lst

#Convert a float written with a , to a regular float
def to_decimal(x):
    num = x.split(',')
    return int(x) if len(num) <= 1 else float(num[0]+'.'+num[1])

#print(get_info('2517 E 13th St, Indianapolis, IN 46201'))
#print(get_info('5689 Versailles Ave, Ann Arbor, MI 48103'))
#print(get_info('1500 N Lake Shore Dr #4B, Chicago, IL 60610'))
