import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

import time, os
from datetime import datetime, timedelta

chromedriver_path = '../chromedriver'
driver = webdriver.Chrome(chromedriver_path)
driver.implicitly_wait(2)

url = 'http://index.krx.co.kr/contents/MKD/03/0304/03040101/MKD03040101.jsp?idxCd=1028&upmidCd=0102#a110dc6b3a1678330158473e0d0ffbf0=3'
driver.get(url)
driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/article/div/div[2]/div/div[1]/fieldset/form/dl[1]/dd/input[2]').click()
time.sleep(1)
total_data = []
cnt = 0
date = 20200101
while date < 20230000:
    date_box = driver.find_element(By.NAME, 'todate')
    date_box.clear()
    date_box.send_keys(date)
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, 'cal-btn-range1y').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/article/div/div[2]/div/div[1]/fieldset/form/div/button').click()
    time.sleep(4)
    date_data = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/article/div/div[2]/div/div[1]/div[4]/div[1]/div[1]/div[2]/div/div/table/tbody')
    date_data = date_data.get_attribute('textContent').strip().replace(' ', '').replace('\t', '').replace('/','').split('\n')
    print(date_data)
    total_data += list(set(date_data[1::9]))
    date += 10000
    cnt += 1
    if cnt % 10 == 0:
        print(date)
driver.quit()
pd.DataFrame(total_data).to_csv('date_data.csv')
