import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

'''Helps login into WealthFront website, read relevant data and successfully logouts using user credentials.'''

#page load timeout
load_timeout=30
#XPaths for elements
#in case window opens full screen as given by params
nav_to_login_page_xpath='/html/body/div[1]/header/div[1]/div/ul[2]/li[1]/a'
#in case window does ot opens full scren
expand_nav_to_login_page_xpath='/html/body/div[1]/header/div[1]/div/ul[3]/li/div'
click_header_nav_to_login_page_xpath='/html/body/div[1]/header/div[2]/a[3]'
#common XPaths
asset_value_xpath='//*[@id="Investments-subgroup"]/div[1]/div/div[2]/div'
deposit_value_xpath='//*[@id="Investments-subgroup"]/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div/div[2]/span'
logout_open_dropdown_xpath='/html/body/header/div/ul[2]/li[3]/a/span'
logout_xpath='/html/body/header/div/ul[2]/li[3]/div/ul/li[3]/a'

#website address
url="https://www.wealthfront.com/"

print(sys.argv)
if len(sys.argv) < 3:
  print("Please provide valid email/password for WealthFront account. For example, wealthfront.py <email> <password>.")
  sys.exit()

email_val=sys.argv[1]
password_val=sys.argv[2]

options = webdriver.ChromeOptions()
options.add_argument("--kiosk")
#full screen, but may fail
driver = webdriver.Chrome(chrome_options=options)
driver.get(url)
try:
  #navigate to login page
  try:
    driver.find_element_by_xpath(nav_to_login_page_xpath).click()
  except:
  	#incase not full screen, do 1 more click (website design)
  	driver.find_element_by_xpath(expand_nav_to_login_page_xpath).click()
  	driver.find_element_by_xpath(click_header_nav_to_login_page_xpath).click()
  #wait till website loads
  try:
    #email=driver.find_element_by_id("web_authentication_email")
    email_elem=WebDriverWait(driver, load_timeout).until(EC.presence_of_element_located((By.ID, "username")))
  except TimeoutException as e:
    print("Failed to get element from page")
    raise
  email_elem.clear()
  email_elem.send_keys(email_val)
  password_elem=driver.find_element_by_id("password")
  password_elem.clear()
  password_elem.send_keys(password_val)
  #submit form : 2 ways possible
  #driver.find_element_by_name("commit").click()
  password_elem.submit() #or email.submit()
  #Can be improved using EC
  driver.implicitly_wait(load_timeout/2)
  #login success
  try:
    print("WEALTHFRONT INVESTMENTS")
    print("Net Assest Value : " + driver.find_element_by_xpath(asset_value_xpath).text)
    print("Net Deposit : " + driver.find_element_by_xpath(deposit_value_xpath).text)
  except:
    print("Failed to extract values from UI.")
    raise
  finally:
    #logout
    driver.find_element_by_xpath(logout_open_dropdown_xpath).click()
    driver.find_element_by_xpath(logout_xpath).click()
    print("Logout Successfull!")
except NoSuchElementException as e:
  print("Failure during execution")
  raise
finally:
  #close browser. For closing tab only : driver.close()
  driver.quit()