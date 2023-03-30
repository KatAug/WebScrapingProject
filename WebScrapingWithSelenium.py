from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import csv 

# Set Up CSV 

file = open("laptops.csv", "w", newline="")
writer = csv.writer(file)
writer.writerow(["id","name", "price", "specifications", "number of reviews"])

# Create Chrome Service and WebDriver Instance

browser_driver = Service("./chromedriver.exe")
scraper = webdriver.Chrome(service=browser_driver)

# GET page for scraping 

scraper.get("https://webscraper.io/test-sites/e-commerce/static/computers/laptops")


cookies = WebDriverWait(scraper, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "acceptCookies")))
cookies.click()
data = []

# Grab all the Laptop names, prices, specifications, number of reviews and add ID 

unique_id = 1
while True:
    laptops = scraper.find_elements(By.CLASS_NAME,"thumbnail")
    for laptop in laptops:
        laptop_name = laptop.find_element(By.CLASS_NAME, "title").get_attribute("title")
        price = laptop.find_element(By.CLASS_NAME, "pull-right.price").text
        specifications = laptop.find_element(By.CLASS_NAME, "description").text
        num_of_reviews = laptop.find_element(By.CLASS_NAME, "ratings").text.split(" ")[0]
        data.append([laptop_name, price, specifications, num_of_reviews])
        # writer.writerow(
        #     [laptop_name.text, price.text, specifications.text])
        unique_id +=1
    try:
        element = scraper.find_element(By.PARTIAL_LINK_TEXT,"›")
        element.click()
    except NoSuchElementException:
        break

print(data)

sorted_data = sorted(data, key= lambda row: row[1])

for i, row in enumerate(sorted_data):
    writer.writerow([i+1]+ row)

# Quit the browser

#file.close()
#scraper.quit()