from selenium.webdriver.common.by import By

from . import base



class LandingPage(base.BasePage):

    page_title = 'K Network'

    email_locator = (By.ID, 'id_email')
    submit_locator = (By.CSS_SELECTOR, '.landing .signup > button')


    def go_to_landing_page(self):
        self.get_relative_path('/')


    def signup(self, email='test@example.com'):
        self.type_in_element(self.email_locator, email)
        self.selenium.find_element(*self.submit_locator).click()

        self.wait_for_ajax()
