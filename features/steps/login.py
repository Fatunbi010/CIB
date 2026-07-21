from behave import given, when, then
from selenium import webdriver
from selenium.common.exceptions import (TimeoutException, NoSuchElementException,ElementClickInterceptedException, StaleElementReferenceException)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import pyotp

# Setup: Initialize driver and maximize window
options = webdriver.ChromeOptions()

# Required for GitHub Actions
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

@given('the user visits the website "{url}"')
def step_impl(context, url):
    driver.get(url)
    time.sleep(3)

@when('the user enters username')
def step_impl(context):
    wait = WebDriverWait(driver, 15)
    input_field = wait.until(EC.presence_of_element_located((By.ID, "Username")))
    wait.until(EC.element_to_be_clickable((By.ID, "Username")))
    input_field.clear()
    input_field.send_keys("ofatunbi_11")

@when('the user enters password')
def step_impl(context):
    wait = WebDriverWait(driver, 15)
    input_field = wait.until(EC.presence_of_element_located((By.ID, "Password")))
    wait.until(EC.element_to_be_clickable((By.ID, "Password")))
    input_field.clear()
    input_field.send_keys("Ofatunbi@2026!")

@when('the user clicks the eye icon in the password field')
def step_impl(context):
    wait = WebDriverWait(driver, 15)
    # Click the button wrapping the eye icon rather than the SVG itself
    eye_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='password'], button[aria-label*='eye'], button[aria-label*='show'], button[aria-label*='toggle']")))
    eye_btn.click()
    time.sleep(1)

@when('the user enters wrong password')
def step_impl(context):
    wait = WebDriverWait(driver, 15)
    input_field = wait.until(EC.presence_of_element_located((By.ID, "Password")))
    wait.until(EC.element_to_be_clickable((By.ID, "Password")))
    input_field.clear()
    input_field.send_keys("Ofatunbi@2029!")

@when('the user clicks Next')
def step_impl(context):
    wait = WebDriverWait(driver, 15)
    next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiButton-contained[type='submit']")))
    next_btn.click()
    time.sleep(3)

@when('the user enters OTP & clicks login')
def step_impl(context):
    wait = WebDriverWait(driver, 30)
    otp_secret = os.environ.get("OTP_SECRET", "")
    if not otp_secret:
        raise AssertionError("OTP_SECRET environment variable is not set. Add it as a GitHub Actions secret.")
    totp = pyotp.TOTP(otp_secret)
    otp_code = totp.now()
    otp_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
        "input[type='text'], input[type='number'], input[name*='otp'], "
        "input[name*='code'], input[placeholder*='OTP'], input[placeholder*='code']")))
    wait.until(EC.element_to_be_clickable(otp_field))
    otp_field.clear()
    otp_field.send_keys(otp_code)
    login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiButton-contained[type='submit']")))
    login_btn.click()

@when('the user enters invalid OTP')
def step_impl(context):
    wait = WebDriverWait(driver, 30)
    otp_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
        "input[type='text'], input[type='number'], input[name*='otp'], "
        "input[name*='code'], input[placeholder*='OTP'], input[placeholder*='code']")))
    wait.until(EC.element_to_be_clickable(otp_field))
    otp_field.clear()
    otp_field.send_keys("000000")
    login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiButton-contained[type='submit']")))
    login_btn.click()

@when('the user clicks login')
def step_impl(context):
    wait = WebDriverWait(driver, 15)
    login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiButton-contained[type='submit']")))
    login_btn.click()

@then('the user sees "{message}"')
def step_impl(context, message):
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{message}')]")))
    except TimeoutException:
        raise AssertionError(f"Expected message '{message}' was not found on the page.")

@then('the user should see "{message}"')
def step_impl(context, message):
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{message}')]")))
    except TimeoutException:
        raise AssertionError(f"Expected message '{message}' was not found on the page.")

@then('the username field displays an inline message "Username is required"')
def step_impl(context):
    wait = WebDriverWait(driver, 15)
    try:
        error_msg = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Username is required')]")))
        assert error_msg.is_displayed(), "Inline message 'Username is required' found but not visible."
        assert "Username is required" in error_msg.text, f"Expected 'Username is required' but got '{error_msg.text}'."
    except TimeoutException:
        raise AssertionError("Expected inline message 'Username is required' was not displayed on the username field.")

@then('the user should a message "Incorrect username or password."')
def step_impl(context):
    wait = WebDriverWait(driver, 30)
    try:
        error_msg = wait.until(EC.presence_of_element_located((By.XPATH,
            "//*[contains(text(), 'Incorrect username or password.') or "
            "contains(text(), 'Invalid username or password') or "
            "contains(text(), 'Login failed') or "
            "contains(text(), 'account is locked') or "
            "contains(text(), 'too many')]")))
        assert error_msg.is_displayed(), "Error message element found but not visible."
    except TimeoutException:
        page_text = driver.find_element(By.TAG_NAME, "body").text
        raise AssertionError(
            f"Expected error message 'Incorrect username or password.' was not displayed.\n"
            f"Page content: {page_text[:500]}"
        )

@then('the user should be directed to My Account')
def step_impl(context):
    wait = WebDriverWait(driver, 30)
    try:
        wait.until(EC.url_contains("my-account"))
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='My Account']")))
    except TimeoutException:
        raise AssertionError("My Account page not found — login may have failed or redirect did not occur.")
    time.sleep(20)

@then('the password field displays an inline message "Password is required"')
def step_impl(context):
    wait = WebDriverWait(driver, 15)
    try:
        inline_msg = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Password is required')]")))
        assert inline_msg.is_displayed(), "Inline message found but not visible."
    except TimeoutException:
        raise AssertionError("Expected inline message 'Password is required' was not displayed in the password field.")

@then('both the username field displays "Username is required" and the password field displays "Password is required"')
def step_impl(context):
    wait = WebDriverWait(driver, 15)
    errors = []

    try:
        username_msg = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Username is required')]")))
        assert username_msg.is_displayed(), "Username inline message found but not visible."
    except (TimeoutException, AssertionError):
        errors.append("Expected inline message 'Username is required' was not displayed for the username field.")

    try:
        password_msg = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Password is required')]")))
        assert password_msg.is_displayed(), "Password inline message found but not visible."
    except (TimeoutException, AssertionError):
        errors.append("Expected inline message 'Password is required' was not displayed for the password field.")

    if errors:
        raise AssertionError("\n".join(errors))
