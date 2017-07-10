# -*- coding: utf-8 -*-
# auto operator for weibo.

import os,time,random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import weibo_opt as opt

def _new_status(content):
    driver.get("https://m.weibo.cn/compose")
    transinput = driver.find_element_by_xpath('//div[@id="app"]/div[1]/div/main/div[1]/div/span/textarea[1]')
    #clear input box first... weibo will save last input in cookie.
    transinput.clear()
    transinput.send_keys(content)
    time.sleep(0.5)
    sendbtn = driver.find_element_by_xpath('//div[@id="app"]/div[1]/div/header/div[3]/a')
    driver.execute_script("arguments[0].click();", sendbtn) #force to click
    #sendbtn.click()

def _get_first_at_info():
    driver.get("https://m.weibo.cn/msg/atme?subtype=allWB")
    first_card = driver.find_element_by_xpath('//div[@id="box"]/section[1]/div[1]/div[1]/section[1]/p[1]')
    return first_card.text
    
def __read_file_into_list(filename, needstrip = True, myEncoding = "utf-8", prefix = '', suffix = ''):
    readlist = []
    if(not os.path.exists(filename)):
        return None
    with open(filename, 'r', encoding=myEncoding) as myfile:
        for line in myfile:
            if(needstrip):
                readlist.append(prefix + line.replace('\n', '') + suffix)
            else:
                readlist.append(prefix + line + suffix)
    return readlist
    
def _make_atlist(atlist):
    returnstr = ''
    for atname in atlist:
        returnstr = returnstr + '@' + str(atname) + ' '
    return returnstr
    
def reforward_first_call():
    driver.get("https://m.weibo.cn/msg/atme?subtype=allWB")
    reforward_btn = driver.find_element_by_xpath('//div[@id="box"]/section[1]/div[1]/div[1]/footer/a[1]')
    reforward_btn.click()
    time.sleep(0.5)
    #sendbtn = driver.find_element_by_xpath('//div[@id="app"]/div[1]/div/header/div[3]/a')
    sendbtn = driver.find_element_by_xpath('//div[@id="box"]/header[1]/a[2]')
    driver.execute_script("arguments[0].click();", sendbtn) #force to click
    
    
#get random from txt.
def act_rand_call(filepath, atlist = []):
    wordlist = __read_file_into_list(filepath)
    respon = random.choice(wordlist)
    #print (respon)
    _new_status(respon + _make_atlist(atlist))
    
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
        driver.set_page_load_timeout(15)
        print ("let's try to send get command...")
        time.sleep(1)
        #rs = _get_first_at_info()
        #print (rs) 
        reforward_first_call()
        driver.close()
    
    print ("all task done~")
    