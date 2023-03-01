import time
import pandas as pd
import re
import os
from os import listdir
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def find_bounces(current_rounds):
    driver = webdriver.Chrome()
    driver.get("")
    time.sleep(10)
    elem = driver.find_element(By.NAME, "loginfmt")
    elem.send_keys(os.environ.get('EMAIL_ADDRESS'))
    elem.send_keys(Keys.RETURN)
    time.sleep(5)
    elem = driver.find_element(By.NAME, "passwd")
    elem.send_keys(os.environ.get('EMAIL_PASSWORD'))
    elem.send_keys(Keys.RETURN)
    time.sleep(5)
    elem = driver.find_element(By.ID, "idSIButton9")
    elem.click()
    time.sleep(10)
    elem = driver.find_element(By.ID, "topSearchInput")
    elem.send_keys("undeliverable")
    elem.send_keys(Keys.RETURN)
    time.sleep(5)
    elem = driver.find_element(By.ID, "groupHeaderAll results")
    elem.click()

    all_emails = []
    for i in range(50):
        time.sleep(2)
        actions = ActionChains(driver)
        actions.send_keys(Keys.ARROW_DOWN)
        actions.perform()
        time.sleep(5)
        elem = driver.find_element(By.CLASS_NAME, "L72vd")
        text = elem.text
        emails = re.findall(r'\S+@\S*\.\w+', text)
        emails = list(set(emails))
        for email in emails:
            all_emails.append(email)
    all_emails = list(set(all_emails))
    driver.close()

    df = pd.DataFrame(all_emails, columns=['email'])
    file_name = f'all_emails_{time.strftime("%Y%m%d-%H%M%S")}.csv'
    df.to_csv(file_name, index=False)
    print(f'Emails saved to {file_name}')
