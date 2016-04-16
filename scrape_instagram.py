from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Firefox()  # can be webdriver.PhantomJS()
browser.get('https://www.instagram.com/p/BD6CBkGjyzp/')

# wait for the select element to become visible
element  = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div/article/div[2]/ul/li[1]/h1/span/span[2]')))
print element.text
browser.quit()


