# -*- coding: utf-8 -*-
# auto operator for weibo.

import os,time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import weibo_opt as opt

def _new_status(content):
    driver.get("https://m.weibo.cn/compose")
    transinput = driver.find_element_by_xpath('//div[@id="app"]/div[1]/div/main/div[1]/div/span/textarea[1]')
    transinput.send_keys(content)
    time.sleep(0.5)
    sendbtn = driver.find_element_by_xpath('//div[@id="app"]/div[1]/div/header/div[3]/a')
    sendbtn.click()

def _get_first_at_info():
    '''
    driver.get("https://m.weibo.cn/")
    clickel = driver.find_element_by_xpath('//div[@id="box"]/div[1]/div[1]/div[2]/a[2]')
    clickel.click()
    '''
    driver.get("https://m.weibo.cn/msg/atme?subtype=allWB")
    first_card = driver.find_element_by_xpath('//div[@id="box"]/section[1]/div[1]/div[1]/section[1]/p[1]')
    return first_card.text
    
if __name__=='__main__':
    installize_driver = True
    if(installize_driver):
        chromedriverPath='lib/chromedriver_230.exe'
        chromeprofilePath = 'C:\\Users\\chibimiku\\AppData\\Local\\Google\\Chrome\\User Data'
        os.environ["webdriver.chrome.driver"] = chromedriverPath
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=" + chromeprofilePath) #Path to your chrome profile
        #options.add_argument("remote-debugging-port=12288")
        driver = webdriver.Chrome(chromedriverPath, chrome_options=options)
        #driver = webdriver.Chrome(chromedriverPath)
        driver.set_page_load_timeout(15)
        print ("let's try to send get command...")
        time.sleep(1)
        #rs = _get_first_at_info()
        #print (rs)
        _new_status("第三版又来啦，这次换了python控制台，我们看看在接入tensorflow之后会怎么样吧；）")
        print ("all task done~")