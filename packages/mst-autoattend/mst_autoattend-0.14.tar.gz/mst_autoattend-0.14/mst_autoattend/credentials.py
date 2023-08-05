import json
import pathlib

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from .pretty_printer import print_msg
from .wait_and_find import *

timeOutDelay = 30   # increase if you have a slow internet connection

CREDENTIALS_FILE_PATH = pathlib.Path.home() / '.msteams_class_attender'

def login(data, check=False, browser=None):
    if check:
        print_msg("running login test...", "DEBUG")
        opt = Options()
        opt.add_argument("headless")
        browser = webdriver.Chrome(ChromeDriverManager().install(),options=opt)
        browser.get('https://teams.microsoft.com/_#/calendarv2')
    wait_and_find_ele_by_id(browser, 'i0116', timeOutDelay).send_keys(data['username'])      # enter username
    wait_and_find_ele_by_id(browser, 'idSIButton9', timeOutDelay).click()                    # click next
    print_msg("user name entered", "DEBUG")
    wait_and_find_ele_by_id(browser, 'aadTile', timeOutDelay).click()                        # choose organization account
    print_msg("chose school or organization accoutn", "DEBUG")
    wait_and_find_ele_by_id(browser, 'i0118', timeOutDelay).send_keys(data['password'])      # enter password
    wait_and_find_ele_by_id(browser, 'idSIButton9', timeOutDelay).click()                    # click next
    print_msg("password entered", "DEBUG")
    pass_error = wait_and_find_ele_by_id(browser, 'passwordError', timeOutDelay)
    if pass_error is not None:
        raise Exception(pass_error.get_attribute("innerHTML"))
    print_msg("password correct, clicking remember signin...", "DEBUG")
    if not check:
        wait_and_find_ele_by_id(browser, 'idSIButton9', timeOutDelay).click()                    # click yes to stay signed in
    else:
        browser.quit()

def load_credentials(reset=False):
    modified = False
    data = {}
    if not reset:
        try:
            with open(CREDENTIALS_FILE_PATH) as f:
                data = json.load(f)
            print_msg("saved credentials loaded!", "DEBUG")
            if data.get("username") is None:
                data['username'] = input("Please enter your MS Teams username: ")
                modified = True
            if data.get("password") is None:
                data["password"] = input("Please enter your MS Teams password: ")
                modified = True
        except (FileNotFoundError, json.JSONDecodeError):
            print_msg("Failed to load from credentials file!", "DEBUG")
            reset = True
    if (reset):
        login_success = False
        while not login_success:
            data['username'] = input("Please enter your MS Teams username: ")
            data["password"] = input("Please enter your MS Teams password: ")
            try:
                print_msg("verifying username and password, please wait for a few minutes...", "INFO")
                login(data, True)
                login_success = True
                print_msg("authenticated successfully", "INFO")
            except:
                print_msg("authenticated failed", "ERROR")
                continue
            data["minimumParticipants"] = input("Please enter minimum participants to exit the meeting: ")
            response = input("Do you want to interact in the meeting while it is going on? (y/n): ")
            while response.lower() not in ["y", "n"]:
                print_msg("please enter y or n!", "ERROR")
                response = input("Do you want to interact in the meeting while it is going on? (y/n): ")
            if response.lower() == "y":
                data["joinMeetingInBackground"] = False
            else:
                data["joinMeetingInBackground"] = True
        modified = True

    if modified:
        with open(CREDENTIALS_FILE_PATH, "x") as f:
            json.dump(data, f)
        print_msg("Credentials saved to " + str(CREDENTIALS_FILE_PATH), "DEBUG")
    return data
