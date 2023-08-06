import os
import sys
from random import randint
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from .credentials import load_credentials, login
from .pretty_printer import print_msg, print_help
from .wait_and_find import *

minRandomJoinLeaveWait = 10
maxRandomJoinLeaveWait = 180

timeOutDelay = 30   # increase if you have a slow internet connection
RETRY_WAITOUT = 30
data = None

maxParticipants = curParticipants = 0
minParticipants = 2

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.notifications": 1 
})

browser = None

def checkAndJoinMeeting():
    global maxParticipants, curParticipants
    joins = wait_and_find_elements_by_xpath(browser, '//button[.="Join"]', 3)
    if len(joins) == 0: # no meeting scheduled
        print_msg("no meeting to join", "INFO")
        return
    print_msg("meeting found, joining the latest meeting...", "INFO")
    sleep(randint(minRandomJoinLeaveWait, maxRandomJoinLeaveWait))
    joins[-1].click()   # join the latest meeting scheduled i.e if join buttons for 9 A.M and 10 A.M available, will join 10 A.M
    elem = wait_and_find_element_by_xpath(browser, '//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button', timeOutDelay)
    print_msg("turning off camera...", "DEBUG")
    if elem.get_attribute('aria-pressed') == 'true': # turn off camera
        elem.click()
    print_msg("turning off microphone...", "DEBUG")
    elem = wait_and_find_element_by_xpath(browser, '//*[@id="preJoinAudioButton"]/div/button', timeOutDelay)
    if elem.get_attribute('aria-pressed') == 'true': # turn off microphone
        elem.click()
    wait_and_find_element_by_xpath(browser, '//button[.="Join now"]', timeOutDelay).click() # join meeting
    print_msg("meeting joined", "INFO")
    sleep(60*5)
    actions = ActionChains(browser)
    rosterBtn = wait_and_find_element_by_xpath(browser, '//button[@id="roster-button"]', timeOutDelay)
    actions.move_to_element(rosterBtn).click().perform()
    numStr = wait_and_find_elements_by_xpath(browser, '//span[@class="toggle-number"][@ng-if="::ctrl.enableRosterParticipantsLimit"]', timeOutDelay)
    if len(numStr) >= 2:
        if numStr[1].text[1:-1] != '':
            maxParticipants = curParticipants = int(numStr[1].text[1:-1])

def checkAndEndOrLeaveOrJoinMeeting():
    global maxParticipants, curParticipants
    hangupBtn = wait_and_find_element_by_xpath(browser, '//button[@id="hangup-button"]', 2)
    if hangupBtn != None: # currently in meeting
        print_msg("in a meeting", "DEBUG")
        numStr = wait_and_find_elements_by_xpath(browser, '//span[@class="toggle-number"][@ng-if="::ctrl.enableRosterParticipantsLimit"]', timeOutDelay)
        if len(numStr) >= 2:
            if numStr[1].text[1:-1] != '':
                curParticipants = int(numStr[1].text[1:-1])
            else :
                actions = ActionChains(browser)
                actions.move_to_element(wait_and_find_element_by_xpath(browser, '//button[@id="roster-button"]', timeOutDelay)).click().perform()
        maxParticipants = max(maxParticipants, curParticipants)
        print_msg("found {} participants in the meeting".format(curParticipants), "DEBUG")
        if curParticipants <= minParticipants and curParticipants != 0:   # leaves the meeting automatically for given condition
            print_msg("leaving meeting as number of participants ({}) is less than minimum set to leave ({})".format(curParticipants, minParticipants), "INFO")
            sleep(randint(minRandomJoinLeaveWait, maxRandomJoinLeaveWait))
            hangupBtn = wait_and_find_element_by_xpath(browser, '//button[@id="hangup-button"]', 3)
            actions = ActionChains(browser)
            actions.move_to_element(hangupBtn).click().perform()
            print_msg("meeting left", "WARNING")
            browser.get('https://teams.microsoft.com/_#/calendarv2')    # open calendar tab
        else :
            return
    else:
        print_msg("not in a meeting, looking for a meeting to join...", "DEBUG")
        maxParticipants = curParticipants = 0
        browser.get('https://teams.microsoft.com/_#/calendarv2')
        try:
            checkAndJoinMeeting()
        except Exception as e:
            print_msg(e, "DEBUG")
            browser.get('https://teams.microsoft.com/_#/calendarv2')

def init(step=0):
    global minParticipants
    print_msg("opening ms teams calendar page...", "DEBUG")
    browser.get('https://teams.microsoft.com/_#/calendarv2')    # open calendar tab in teams
    minParticipants = int(data.get('minimumParticipants', minParticipants))
    success_step = 0
    # login step
    if step <= 0:
        print_msg("attempting login...", "DEBUG")
        login(data, check=False, browser=browser)
        success_step = 1
    # calendar access step
    if step <= 1:
        print_msg("opening calendar...", "DEBUG")
        wait_and_find_element_by_xpath(browser, '//button[@title="Switch your calendar view"]', timeOutDelay)
        while wait_and_find_element_by_xpath(browser, '//button[@title="Switch your calendar view"]', timeOutDelay).get_attribute('name') != "Week": # change calender work-week view to week view
            switch_button = wait_and_find_element_by_xpath(browser, '//button[@title="Switch your calendar view"]', timeOutDelay)
            if switch_button:
                switch_button.click()
            else:
                continue
            to_week = wait_and_find_element_by_xpath(browser, '//button[@name="Week"]', timeOutDelay)
            if to_week:
                to_week.click()
            else:
                continue
            print_msg("week view set in calendar", "DEBUG")
        success_step = 2
    return success_step

def main():
    global browser, data
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_help()
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        print_msg("config reset requested by user...", "WARNING")
        data = load_credentials(reset=True)    
    else:
        print_msg("loading credentials from saved file...", "DEBUG")
        data = load_credentials()
    if data.get("joinMeetingInBackground"):
        print_msg("starting in headless mode as per setting...", "INFO")
        opt.add_argument("headless")

    browser = webdriver.Chrome(ChromeDriverManager().install(),options=opt)
 
    step = 0
    while step != 2:
        print_msg("initializing session, please wait a few minutes...", "INFO")
        step = init(step)
    else:
        print_msg("initialized successfully!", "INFO")
        while True:
            try:
                print_msg("checking for meeting activity...", "INFO")
                checkAndEndOrLeaveOrJoinMeeting()
            except Exception as e:
                print_msg(e, "DEBUG")
                print_msg("failed to check meeting activity", "WARNING")
            finally:
                print_msg("checking teams activity again in {} seconds".format(RETRY_WAITOUT), "INFO")
                sleep(RETRY_WAITOUT)

if __name__ == "__main__":
    main()