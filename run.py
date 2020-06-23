from secret import data
from automate import createDriver, authenticate, repSearch

for email, password in data.items():

    driver = createDriver(False)
    authenticate(driver, email, password)
    repSearch(driver, 30)
    driver.quit()
