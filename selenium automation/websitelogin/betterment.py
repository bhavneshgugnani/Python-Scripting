import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

'''Helps login into Betterment website, read relevant data and successfully logouts using user credentials.'''

#page load timeout
load_timeout=30
#XPaths for elements
asset_value_xpath='//*[@id="summary"]/div[1]/div/div[2]/div[1]/div[2]/span[1]'
earnings_xpath='//*[@id="summary"]/div[1]/div/div[2]/div[2]/div[2]/span'
logout_open_dropdown_xpath='/html/body/header[1]/nav[2]/ul/li[2]/a'
logout_xpath='/html/body/header[1]/nav[2]/ul/li[2]/ul/li[4]/form/button'

#website address
url='https://wwws.betterment.com'

def waitTillXPathClickableThenClick(xpath):
  try:
    element = WebDriverWait(driver, load_timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)));
    element.click();
  except:
    print("Faield to click XPath.")
    raise

print(sys.argv)
if len(sys.argv) < 3:
  print("Please provide valid email/password for Betterment account. For example, betterment.py <email> <password>.")
  sys.exit()

email_val=sys.argv[1]
password_val=sys.argv[2]


options = webdriver.ChromeOptions()
options.add_argument("--kiosk")
driver=webdriver.Chrome(chrome_options=options)
driver.get(url)
try:
  assert "Betterment" in driver.title
  #wait till website loads
  try:
    #email=driver.find_element_by_id("web_authentication_email")
    email_elem=WebDriverWait(driver, load_timeout).until(EC.presence_of_element_located((By.ID, "web_authentication_email")))
  except TimeoutException as e:
    print("Failed to get element from page")
    raise
  email_elem.clear()
  email_elem.send_keys(email_val)
  password_elem=driver.find_element_by_id("web_authentication_password")
  password_elem.clear()
  password_elem.send_keys(password_val)
  #submit form : 2 ways possible
  #driver.find_element_by_name("commit").click()
  password_elem.submit() #or email.submit()
  #TODO : improve using EC
  driver.implicitly_wait(load_timeout/2)
  #login maybe success/failure. Only way to find is try extacting values.
  try:
    print("BETTERMENT INVESTMENTS")
    print("Net Assest Value : " + driver.find_element_by_xpath(asset_value_xpath).text)
    print("Net Earnings : " + driver.find_element_by_xpath(earnings_xpath).text)
  except:
    print("Failed to extract values from UI attributes. Login failure or XPaths changed.")
    raise
  finally:
    #logout
    waitTillXPathClickableThenClick(logout_open_dropdown_xpath)
    waitTillXPathClickableThenClick(logout_xpath)
    print("Logout Successfull!")
except NoSuchElementException as e:
  print("Failure during execution")
  raise
finally:
  #close browser. For closing tab only : driver.close()
  driver.quit()