from selenium import webdriver
import time
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By



@pytest.fixture(scope='session')
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.mark.run(order=1)
def test_privacy_page(browser):
    browser.get("https://www.shaberi.com/tw")
    
    # privacy page test
    qa_bt = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/ul/li[2]/a')
    qa_bt.click()
    wait = WebDriverWait(browser, 10)
    wait.until(EC.url_contains("/qa"))
    time.sleep(1)

    # Add assertion
    assert "/qa" in browser.current_url

@pytest.mark.run(order=2)
def test_language_switch(browser):

    languages = [
        ('简体中文', '/cn/qa'),
        ('English', '/en/qa'),
        ('日本語', '/jp/qa'),
        ('繁體中文', '/tw/qa')
    ]

    for lang, expected_url_part in languages:
        language_dropdown = browser.find_element(By.CLASS_NAME, 'flex.cursor-pointer')
        language_dropdown.click()
        language_option = browser.find_element(By.XPATH, f'//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li/a[contains(text(), "{lang}")]')
        language_option.click()
        wait = WebDriverWait(browser, 10)
        wait.until(EC.url_contains(expected_url_part))
        time.sleep(1)

        # Add assertion
        assert expected_url_part in browser.current_url

@pytest.mark.run(order=3)
def test_search_login(browser):
    question_input = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[1]/div[1]/div[2]/div/input')
    question_input.send_keys('登入')
    time.sleep(1)
    search_result = browser.find_element(By.CLASS_NAME, 'question-collapse.open')
    time.sleep(1)
    assert search_result.is_displayed(), "Search results is not displayed"

@pytest.mark.run(order=4)
def test_clean_answer(browser):
    clean_bt = browser.find_element(By.CLASS_NAME, 'btn-clean')
    clean_bt.click()
    time.sleep(1)
    problem_category = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[3]')
    assert problem_category.is_displayed(), "Problem Category is not displayed"

@pytest.mark.run(order=5)
def test_search_wallet(browser):
    question_input = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[1]/div[1]/div[2]/div/input')
    question_input.send_keys('錢包')
    time.sleep(1)
    search_result = browser.find_element(By.CLASS_NAME, 'question-collapse.open')
    time.sleep(1)
    assert search_result.is_displayed(), "Search results is not displayed"
