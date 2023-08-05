from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait


def get_clear_browsing_button(driver):
    """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page."""
    return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')


def clear_cache(driver, timeout=60):
    """Clear the cookies and cache for the ChromeDriver instance."""
    # navigate to the settings page
    driver.get('chrome://settings/clearBrowserData')

    # wait for the button to appear
    wait = WebDriverWait(driver, timeout)
    wait.until(get_clear_browsing_button)

    # click the button to clear the cache
    get_clear_browsing_button(driver).click()

    # wait for the button to be gone before returning
    wait.until_not(get_clear_browsing_button)



caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"
# noinspection SpellCheckingInspection

options = webdriver.ChromeOptions()

chrome_preferences = {'profile.managed_default_content_settings.images': 2}
options.add_argument("headless")
# noinspection SpellCheckingInspection
options.add_experimental_option("prefs", chrome_preferences)
driver = webdriver.Chrome()
clear_cache(driver)
browser = webdriver.Chrome(options=options, service_args=['--silent'], desired_capabilities=caps)