from secret import data
from automate import createDriver, authenticate, repSearch

for email, password in data.items():

    driver = createDriver()
    authenticate(driver, email, password)
    repSearch(driver, email, 30)
    driver.quit()
