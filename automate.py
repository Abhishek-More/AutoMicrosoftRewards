from random_word import RandomWords
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

def createDriver(headless=True):
    #Returns Firefox Webdriver
    #Change path to geckodriver below
    try:
        os.environ['PATH'] += os.pathsep + "/usr/local/bin/"
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('--headless')  #Uncomment to run headless
        driver = webdriver.Firefox(options=options)

        base = 'https://www.bing.com/search?q=search'
        driver.get(base)
        print("***Created Driver***")
        return driver
    except Exception as error:
        print("Error:", error)
        quit()

def authenticate(driver, email, password):
    #Signs into Bing with email and password
    base = driver.current_url
    login = driver.find_element_by_class_name('id_button')
    while driver.current_url == base:
        login.click()

    usernameField = driver.find_element_by_class_name('form-control')
    usernameField.send_keys(email)
    usernameField.send_keys(Keys.ENTER)

    time.sleep(1)

    passwordField = driver.find_element_by_class_name('form-control')
    passwordField.send_keys(password)
    passwordField.send_keys(Keys.ENTER)

    time.sleep(1)

def getRandomWord():
    #Returns a random word in the English language
    while True:
        try:
            random = RandomWords()
            word = random.get_random_word()
            return word
        except:
            pass

def searchWord(driver):
    #Inserts word into search box and searches
    tryCount = 3
    while tryCount > 0:
        try:
            search = driver.find_element_by_class_name('b_searchbox')
            break
        except:
            print("Could not find search bar, try:", abs(4 - tryCount))
            time.sleep(5)
            tryCount -= 1
        if tryCount:
            return 1

    word = getRandomWord()

    search.clear()
    search.send_keys(word)
    search.send_keys(Keys.ENTER)

def repSearch(driver, count):
    #Searches repeatedly for specified count with one minute rest
    #Adds/Updates user points in database
    for i in range(count):
        print("Search", i)
        searchWord(driver)
        time.sleep(10)
    print("***Completed Searches***")
