from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import csv

URL = "https://www.flipkart.com/"
PATH = "C:/SeleniumDrivers/chromedriver.exe"

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36")

heads = ['Title','Desc','Rating','Price']
data = []

def create_file(data, item):
    file = item.lower().replace(' ','_')
    file = f'Auto-Scraping/flipkart-scraper/{file}.csv'
    with open(file,'w', newline='') as f:
        w=csv.DictWriter(f,heads)
        w.writeheader()
        for value in data:
            w.writerow(value)
    print("Task Complete!")

def driver_func(driver,item, min_lim, max_lim):
    #cancel the login dialog box
    cancel_btn = driver.find_element(By.CSS_SELECTOR,'button[class="_2KpZ6l _2doB4z"]')
    cancel_btn.click()

    #enter query in search box
    search_bar = driver.find_element(By.CLASS_NAME,'_3704LK')
    search_bar.click()
    search_bar.send_keys(item + Keys.ENTER)

    # filter price
    filter_box = driver.find_elements(By.CLASS_NAME,'_2YxCDZ')
    val1 = Select(filter_box[0])
    val1.select_by_value(min_lim)
    
    val2 = Select(filter_box[1])
    val2.select_by_value(max_lim)

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[class="_13oc-S"]')))

    results_list = driver.find_elements(By.CSS_SELECTOR,'div[class="_13oc-S"]')

    num = 1
    try:
        for quad_set in results_list:
            product_list = quad_set.find_elements(By.CLASS_NAME,'_4ddWXP')

            for product in product_list:
                print(num)
                num +=1
                info = {}

                info['Title'] = str(product.find_element(By.CSS_SELECTOR,'a[class="s1Q9rs"]').get_attribute('innerHTML')).strip()

                try:
                    info['Desc'] = str(product.find_element(By.CLASS_NAME,'_3Djpdu').get_attribute('innerHTML')).strip()
                except:
                    info['Desc'] = 'Unavailable'

                try:
                    info['Rating'] = str(product.find_element(By.CLASS_NAME,'_3LWZlK').get_attribute('innerHTML')).strip()
                    info['Rating'] = info['Rating'].split('<')[0]
                except:
                    info['Rating'] = 'Unavailable'

                try:
                    info['Price'] = str(product.find_element(By.CLASS_NAME,'_30jeq3').get_attribute('innerHTML')).strip()
                    info['Price'] = info['Price'][1:len(info['Price'])]
                except:
                    info['Price'] = 'Unavailable'

            print(info)
            data.append(info)
    except:
        pass

    create_file(data, item)

def main():
    item = str(input("Enter item: "))
    max_lim = str(input('Enter upper limit: '))
    min_lim = str(input('Enter lower limit: '))
    driver = webdriver.Chrome(executable_path=PATH,chrome_options=opts)
    driver.implicitly_wait(30)
    driver.get(URL)
    driver_func(driver,item, min_lim=min_lim, max_lim=max_lim)

if __name__=="__main__":
    main()
