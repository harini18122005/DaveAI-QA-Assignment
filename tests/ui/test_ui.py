from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import UI_BASE_URL


CONTACT_URL = f"{UI_BASE_URL}/contact-us/"
WAIT_SECONDS = 15

NAME_FIELD = (By.ID, "form-field-name")
CONTACT_FIELD_LOCATORS = {
    "Name": NAME_FIELD,
    "Email": (By.ID, "form-field-email"),
    "Company name": (By.CSS_SELECTOR, 'input[placeholder="Company name"]'),
    "Phone number": (By.CSS_SELECTOR, 'input[placeholder="Phone number"]'),
}


def test_ui_01_homepage_loads_with_expected_title_and_heading(driver):
    driver.get(UI_BASE_URL)
    wait = WebDriverWait(driver, WAIT_SECONDS)

    wait.until(lambda browser: browser.title != "")
    assert driver.title == "AI-Native Automotive Intelligence Platform | DaveAI"

    main_heading = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "h1"))
    )
    assert main_heading.text == "Automotive Intelligence Across Every Function"


def test_ui_02_contact_navigation_opens_contact_page(driver):
    driver.get(UI_BASE_URL)
    wait = WebDriverWait(driver, WAIT_SECONDS)

    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
    contact_locator = (
        By.CSS_SELECTOR,
        f'a.elementor-item[href="{CONTACT_URL}"]',
    )
    contact_link = wait.until(EC.presence_of_element_located(contact_locator))
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
        contact_link,
    )
    wait.until(
        lambda browser: browser.execute_script(
            "const rect = arguments[0].getBoundingClientRect(); "
            "return rect.top >= 0 && rect.bottom <= window.innerHeight;",
            contact_link,
        )
    )
    wait.until(EC.element_to_be_clickable(contact_locator)).click()

    wait.until(EC.url_to_be(CONTACT_URL))
    assert driver.current_url == CONTACT_URL


def test_ui_03_contact_form_fields_are_visible_and_enabled(driver):
    driver.get(CONTACT_URL)
    wait = WebDriverWait(driver, WAIT_SECONDS)

    for field_name, locator in CONTACT_FIELD_LOCATORS.items():
        field = wait.until(EC.visibility_of_element_located(locator))
        assert field.is_displayed(), f"{field_name} field should be visible"
        assert field.is_enabled(), f"{field_name} field should be enabled"


def test_ui_04_name_field_accepts_and_clears_sample_text(driver):
    driver.get(CONTACT_URL)
    wait = WebDriverWait(driver, WAIT_SECONDS)
    name_field = wait.until(EC.element_to_be_clickable(NAME_FIELD))

    name_field.send_keys("Harini QA Test")
    assert name_field.get_attribute("value") == "Harini QA Test"

    name_field.clear()
    assert name_field.get_attribute("value") == ""