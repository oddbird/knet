from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from . import page



class BasePage(page.Page):
    """Base class for all PYO Pages."""
    user_name_locator = (By.CSS_SELECTOR, 'header .user-nav .user-name > a')
    logout_locator = (By.CSS_SELECTOR, 'header .user-nav .logout-form > button')


    @property
    def is_user_logged_in(self):
        return self.is_element_visible(*self.user_name_locator)


    @property
    def username_text(self):
        return self.selenium.find_element(*self.user_name_locator).text


    def click_logout(self):
        logout = self.selenium.find_element(*self.logout_locator)
        logout.click()
        from . import landing
        return landing.LandingPage(self.selenium)
