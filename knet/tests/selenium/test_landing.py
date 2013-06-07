"""Selenium tests for landing page."""
from selenium.webdriver.common.by import By

from .pages import landing



def test_user_can_submit_email_address(selenium):
    landing_pg = landing.LandingPage(selenium)

    landing_pg.go_to_landing_page()
    landing_pg.signup()

    assert landing_pg.is_element_present(By.CSS_SELECTOR, '#messages .success')
