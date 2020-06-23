from secret import *
from automate import *

#Stores Email and Points after every search
accData = []

for email, password in data.items():

    driver = createDriver(False)
    authenticate(driver, email, password)
    accData.append((email, repSearch(driver, 1)))
    sendMail(emailAddress, emailPass, userEmail, accData)
    driver.quit()
