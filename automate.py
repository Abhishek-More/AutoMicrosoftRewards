from bs4 import BeautifulSoup
import datetime
import random
from random_word import RandomWords
from secrets import path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
import time
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def createDriver(headless=True):
    #Returns Firefox Webdriver
    try:
        os.environ['PATH'] += os.pathsep + path
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
    driver.find_element_by_id
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

    try:
        back = driver.find_element_by_id('idBtn_Back')
        back.click()
    except:
        pass
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
        time.sleep(random.randint(30,50))

    print("***Completed Searches***")

    points = scrapeInfo(driver)
    return points


def scrapeInfo(driver):
    #Scrapes page and returns total user points

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    scores = soup.find_all(id='id_rc')
    for score in scores:
        return score.text

def sendMail(email, password, userEmail, accData):
    #Sends Email containing emails and points

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(email, password)

        date = datetime.date.today()
        subject = f"AutoMicrosoftRewards: {date}"

        body = ''
        for data in accData:
            body += f"{data[0]}: {data[1]} points\n"

        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(email, userEmail, msg)
        print("***Sent Email***")

def writeData(email, points):
    if "@gmail.com" in email:
        email = email.replace("@gmail.com", "")
    print(email)
    cred = credentials.Certificate('autorewards.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://autorewards-92ae1.firebaseio.com/'
    })
    ref = db.reference()
    users_ref = ref.child('accounts')

    users_ref.update({email: str(points)})
