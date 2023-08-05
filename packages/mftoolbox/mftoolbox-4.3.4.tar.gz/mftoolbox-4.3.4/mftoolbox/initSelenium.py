from selenium import webdriver as __webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities as __DesiredCapabilities
from selenium.webdriver.support.ui import Select as __select
from selenium.common import exceptions as __exceptions
from mftoolbox.constants import Header as __header

"""

Creates and instace of the wedbriver as borwser and clears browsing data:
    - browsing history;
    - cookies and other site data; 
    - cached images and files.

This prevents the browser having cached old pages like the ones whe the destination server is down

Inspiration for this module:

    - answer starting as "Selenium provides a convenient Select class to work with select -> option constructs...".
        this presented to me the Select class. Link: 
        https://stackoverflow.com/questions/7867537/how-to-select-a-drop-down-menu-value-with-selenium-using-python
    - article "How to interact with the elements within #shadow-root (open) while Clearing Browsing Data 
        of Chrome Browser using cssSelector". Link:
        https://www.thetopsites.net/article/59404504.shtml
    - article that defined the function "__expand_shadow_element" by injecting a script inside python. Link:
        https://stackoverflow.com/questions/36141681/does-anybody-know-how-to-identify-shadow-dom-web-elements-using-selenium-webdriv
    - article "How to Use Selenium WebDriver Waits using Python" so the driver can wait until cache is cleared. Link:
        https://www.techbeamers.com/selenium-webdriver-waits-python/

"""


def __expand_shadow_element(__browser, element):
    __shadow_root = __browser.execute_script('return arguments[0].shadowRoot', element)
    return __shadow_root

# setting up the browser
__caps = __DesiredCapabilities().CHROME
__caps["pageLoadStrategy"] = "eager"
# noinspection SpellCheckingInspection
__options = __webdriver.ChromeOptions()
__chrome_preferences = {'profile.managed_default_content_settings.images': 2}
 options.add_argument("headless")
# noinspection SpellCheckingInspection
__options.add_experimental_option("prefs", __chrome_preferences)
browser = __webdriver.Chrome(options=__options, service_args=['--silent'], desired_capabilities=__caps)
browser.header_overrides = __header
# opening cleadr browse data page
browser.get('chrome://settings/clearBrowserData')
# find time range dropdown. Full xpath:
# /html/body/# settings-ui//div[2]/settings-main//settings-basic-page//div[1]/settings-section[4]/settings-privacy-page
# //# settings-clear-browsing-data-dialog//cr-dialog[1]/div[3]/iron-pages/div[2]/div/settings-dropdown-menu//select'
__root1 = browser.find_element_by_tag_name("settings-ui")
__shadow_root1 = __expand_shadow_element(browser, __root1)
__root2 = __shadow_root1.find_element_by_css_selector("settings-main#main")
__shadow_root2 = __expand_shadow_element(browser, __root2)
__root3 = __shadow_root2.find_element_by_css_selector("settings-basic-page[role='main']")
__shadow_root3 = __expand_shadow_element(browser, __root3)
__webelement1 = __shadow_root3.find_element_by_css_selector("settings-section[page-title='Privacy and security']")
__root4 = __webelement1.find_element_by_css_selector('settings-privacy-page')
__shadow_root4 = __expand_shadow_element(browser, __root4)
__root5 = __shadow_root4.find_element_by_css_selector('settings-clear-browsing-data-dialog')
__shadow_root5 = __expand_shadow_element(browser, __root5)
__root6 = __shadow_root5.find_element_by_id('clearBrowsingDataDialog')
__webelement2 = __root6.find_element_by_id('clearFromBasic')
__shadow_root6 = __expand_shadow_element(browser, __webelement2)
__dropdown = __select(__shadow_root6.find_element_by_id('dropdownMenu'))
#select option all time
__dropdown.select_by_visible_text('All time')
#find Clear Data Button and click
__button = __root6.find_element_by_id('clearBrowsingDataConfirm')
__button.click()
# wait until button disapears
try:
    while __button.is_displayed():
        pass
except __exceptions.StaleElementReferenceException:
    pass
