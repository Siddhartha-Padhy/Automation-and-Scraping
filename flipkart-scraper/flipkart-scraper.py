from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

URL = "https://www.flipkart.com/"
PATH = "C:/SeleniumDrivers/chromedriver.exe"
ITEM = 'atomic habits'

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36")

driver = webdriver.Chrome(executable_path=PATH,chrome_options=opts)
driver.get(URL)
driver.implicitly_wait(30)

#cancel the login dialog box
cancel_btn = driver.find_element(By.CSS_SELECTOR,'button[class="_2KpZ6l _2doB4z"]')
cancel_btn.click()
print("\nCancel Button Clicked\n")

#enter query in search box
search_bar = driver.find_element(By.CLASS_NAME,'_3704LK')
search_bar.click()
search_bar.send_keys(ITEM + Keys.ENTER)
print("\nSearched\n")

sleep(10)

results_list = driver.find_elements(By.CSS_SELECTOR,'div[class="_13oc-S"]')
print("Result_list length = ",len(results_list))

num = 1
for quad_set in results_list:
    product_list = quad_set.find_elements(By.CLASS_NAME,'_4ddWXP')
    print("Product list length=",len(product_list))

    for product in product_list:
        print(num)
        num +=1

        title = str(product.find_element(By.CSS_SELECTOR,'a[class="s1Q9rs"]').get_attribute('innerHTML')).strip()
        desc = str(product.find_element(By.CLASS_NAME,'_3Djpdu').get_attribute('innerHTML')).strip()

        try:
            rating = str(product.find_element(By.CLASS_NAME,'_3LWZlK').get_attribute('innerHTML')).strip()
            rating = rating.split('<')[0]
        except:
            rating = 0
        price = str(product.find_element(By.CLASS_NAME,'_30jeq3').get_attribute('innerHTML')).strip()

        print("Name: " + title)
        print("Desc: " + desc)
        print("Rating: " + rating)
        print("Price: " + price)
