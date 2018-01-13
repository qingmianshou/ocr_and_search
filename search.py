#-*- coding：utf-8 -*-
import requests


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import open_browser

global driver
global wait
global keyword_input
global submit 

#浏览器初始化
def init_browser():
	if open_browser:
		global driver
		global wait
		global keyword_input
		global submit 
		driver = webdriver.Chrome("D:\\chromedriver.exe",service_args=['--disk-cache=true','--load-images=false']);
		driver.maximize_window()  
		wait = WebDriverWait(driver, 10)
		driver.get("http://www.baidu.com");
		keyword_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#kw')))
		submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#su')))

def search_BaiDu(keywords):
	if open_browser:
		keyword_input.clear()
		keyword_input.send_keys(keywords)
		submit.click()
		return ""
	else:
	    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"}
	    res = requests.get("http://www.baidu.com/s?tn=ichuner&lm=-1&word="+keywords+"&rn=1",headers=headers)
	    return res.text
	    
def close_browser():
	driver.close()