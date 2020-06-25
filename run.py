from secret import *
from automate import *

#Stores Email and Points after every search
accData = []

for email, password in data.items():

    driver = createDriver()
    authenticate(driver, email, password)
    accData.append((email, repSearch(driver, 30)))
    driver.quit()

sendMail(emailAddress, emailPass, userEmail, accData)