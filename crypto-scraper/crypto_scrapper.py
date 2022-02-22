from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

values = []
#headers for the csv file
heads = ['Date','Open','High','Low','Close','Volume','MarketCap']

#write to csv file
def record(values):
    with open(file,'w', newline='') as f:
        w=csv.DictWriter(f,heads)
        w.writeheader()
        for value in values:
            w.writerow(value)
    print("Task Complete!")

#getting table rows
def get_data():
    #wait till table loads
    table = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//table/tbody/tr')))
    rows = driver.find_elements(By.XPATH,'//table/tbody/tr')

    #if no. of rows less than required then click load more button
    if len(rows)<count:
        load_more = driver.find_element(By.CSS_SELECTOR,'button[class="x0o17e-0 DChGS"]')
        driver.execute_script("arguments[0].click();", load_more)
        get_data()
    
    else:
        for i in range(count):
            value = {}
            for ind,data in list(enumerate(rows[i].find_elements(By.TAG_NAME,'td'))):
                value[heads[ind]] = str(data.get_attribute('innerHTML')).strip()
            values.append(value)
    
        record(values)

if __name__=="__main__":
    count = int(input("Enter number of days: "))
    stock = str(input("Enter stock name: ")).lower()

    PATH = "C:/SeleniumDrivers/chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    driver.implicitly_wait(25)
    driver.get(f"https://coinmarketcap.com/currencies/{stock}/historical-data/")
    file = f'{stock}_crypto.csv'
    try:
        get_data()

    except Exception as e:
        print(f"Exception: {e}")