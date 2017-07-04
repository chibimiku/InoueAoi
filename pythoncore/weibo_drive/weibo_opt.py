# -*- coding: utf-8 -*-
# auto operator for weibo.

# provides some api.

from selenium import webdriver

def __inner_gettext(driver, elementid):
    el = driver.find_element_by_id(elementid)
    content1 = el.get_attribute("Value")
    if(not content1):
        content1 = el.text
    return content1

def __inner_input(driver, elementid, content, clean_first = False):
    time.sleep(0.3)
    transinput = driver.find_element_by_id(elementid)
    if(clean_first):
        transinput.clear()
        time.sleep(0.2)
    transinput.send_keys(content)
    
def __inner_check(driver, elementid):
    checkbtn = driver.find_element_by_id(elementid)
    checkbtn.click()
    time.sleep(0.5)

def __inner_select(driver, elementid, labels):
    el = driver.find_element_by_id(elementid)
    for option in el.find_elements_by_tag_name('option'):
        if option.text == labels:
            option.click()
            break
    time.sleep(0.5)
	
