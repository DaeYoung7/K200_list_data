import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

import time, os
from datetime import datetime, timedelta

date_data = pd.read_csv('date_data.csv')['0'].sort_values()

chromedriver_path = '../chromedriver'
driver = webdriver.Chrome(chromedriver_path)
driver.implicitly_wait(2)

url = 'http://index.krx.co.kr/contents/MKD/03/0304/03040101/MKD03040101.jsp?idxCd=1028&upmidCd=0102#a110dc6b3a1678330158473e0d0ffbf0=3'
driver.get(url)

yearnow = date_data.values[0] // 10000
ticker_df = pd.DataFrame(index=[i for i in range(205)])
for dateint in date_data.values:
    datestr = str(dateint)
    search_date = datetime(int(datestr[:4]), int(datestr[4:6]), int(datestr[6:]))
    date_box = driver.find_element(By.NAME, 'schdate')
    date_box.clear()
    date_box.send_keys(int(search_date.strftime('%Y%m%d')))
    time.sleep(1)

    button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/article/div/div[2]/div/div[1]/fieldset/form/div/button')
    button.click()
    time.sleep(2)
    ticker_data = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/article/div/div[2]/div/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/table/tbody')
    # ticker_data = driver.find_element(By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div/div[1]/div[1]/div[1]/div[2]/div/div/table/tbody')
    # ticker_data = driver.find_element(By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div/div[1]/div[1]/div[1]')

    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/article/div/div[2]/div/div[1]/fieldset/form/div/span/button[2]').click()
    time.sleep(5)
    data = pd.read_csv('/Users/daeyoung/Downloads/data.csv')
    ticker = pd.Series(['A'+str(x).zfill(6) for x in data['종목코드']], name=search_date)
    ticker_df = pd.concat([ticker_df, ticker], axis=1)

    os.remove('/Users/daeyoung/Downloads/data.csv')
    if yearnow != int(datestr[:4]):
        yearnow +=1
        print(yearnow, int(datestr[:4]))
driver.quit()

ticker_df = ticker_df.dropna(how='all').T
ticker_df.to_csv('k200_ticker.csv')