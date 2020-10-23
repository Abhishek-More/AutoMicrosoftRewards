from secrets import *
from automate import *

#Stores Email and Points after every search
accData = []

for email, password in data.items():

    driver = createDriver(False)
    authenticate(driver, email, password)
    #accData.append((email, repSearch(driver, 30)))
    writeData(email, repSearch(driver, 30))
    driver.quit()

#sendMail(emailAddress, emailPass, userEmail, accData)