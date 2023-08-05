from time import sleep

sleepDelay = 4      # increase if you have a slow internet connection

def wait_and_find_ele_by_id(browser, id, timeout):
    sleep(sleepDelay)
    for i in range(timeout):
        try:
            ele = browser.find_element_by_id(id)
        except:
            sleep(sleepDelay)
        else:
            return ele

def wait_and_find_ele_by_link_text(browser, text, timeout):
    sleep(sleepDelay)
    for i in range(timeout):
        try:
            ele = browser.find_element_by_link_text(text)
        except:
            sleep(sleepDelay)
        else:
            return ele

def wait_and_find_element_by_xpath(browser, xpath, timeout):
    sleep(sleepDelay)
    for i in range(timeout):
        try:
            ele = browser.find_element_by_xpath(xpath)
        except:
            sleep(sleepDelay)
        else:
            return ele

def wait_and_find_elements_by_xpath(browser, xpath, timeout):
    sleep(sleepDelay)
    for i in range(timeout):
        try:
            ele = browser.find_elements_by_xpath(xpath)
        except:
            sleep(sleepDelay)
        else:
            return ele