"""
LinkedIn Easy Apply — FINAL VERSION (PUNE LOCATION FIX)

Fixes included:
• Prevents background tabs
• Pagination Next button works
• Easy Apply automation
• Numeric fields handled
• Dropdown handled
• Typeahead location handled (Pune)
• Multi-step form handled
• Done button handled
• Already applied skipped
"""

import time
import random
import datetime
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import *


# ======================
# CONFIG
# ======================

PROFILE_PATH = r"C:\selenium-profile"

JOB_URL = "https://www.linkedin.com/jobs/search/?keywords=data%20analyst&location=India"

MAX_APPLY = 50

OUTPUT_APPLIED = "applied_jobs.xlsx"
OUTPUT_FAILED = "failed_jobs.csv"

YEARS_EXPERIENCE = "1"
EXPECTED_SALARY = "500000"
NOTICE_PERIOD = "0"
PHONE_NUMBER = "7645091386"
EMAIL_VALUE = "pk861510@gmail.com"

DEFAULT_CITY = "Pune"   # <<< LOCATION FIX


SHORT = 0.5
MEDIUM = 1.2
LONG = 2.5


# ======================
# DRIVER
# ======================

options = webdriver.ChromeOptions()

options.add_argument(f"--user-data-dir={PROFILE_PATH}")
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 20)


# ======================
# HELPERS
# ======================

def sleep(a=SHORT, b=MEDIUM):
    time.sleep(random.uniform(a, b))


def now():
    return datetime.datetime.now().strftime("%H:%M:%S")


# ======================
# CLOSE EXTRA TABS FIX
# ======================

def close_extra_tabs():

    main = driver.window_handles[0]

    for handle in driver.window_handles:

        if handle != main:

            driver.switch_to.window(handle)

            driver.close()

    driver.switch_to.window(main)


# ======================
# SCROLL JOB LIST
# ======================

def scroll_jobs_panel():

    last = 0

    while True:

        jobs = driver.find_elements(By.CSS_SELECTOR, "a.job-card-container__link")

        if len(jobs) == last:
            break

        last = len(jobs)

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'end'});",
            jobs[-1]
        )

        sleep(1,2)


# ======================
# GET JOB CARDS
# ======================

def get_job_cards():

    wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "a.job-card-container__link")
        )
    )

    return driver.find_elements(
        By.CSS_SELECTOR,
        "a.job-card-container__link"
    )


# ======================
# CLICK JOB CARD
# ======================

def click_job_card(card):

    driver.execute_script(
        "arguments[0].removeAttribute('target');",
        card
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        card
    )

    sleep()

    driver.execute_script(
        "arguments[0].click();",
        card
    )

    sleep(2,3)

    close_extra_tabs()


# ======================
# EASY APPLY CLICK
# ======================

def click_easy_apply():

    try:

        btn = wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//button[contains(@class,'jobs-apply-button')]")
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            btn
        )

        sleep()

        return True

    except:

        print(now(), "Already applied or no Easy Apply")

        return False


# ======================
# GET MODAL
# ======================

def get_modal():

    return wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@role='dialog']")
        )
    )


# ======================
# NORMAL INPUT SET
# ======================

def set_input(inp, value):

    inp.clear()

    inp.send_keys(value)

    sleep(0.5,1)


# ======================
# TYPEAHEAD LOCATION FIX
# ======================

def set_typeahead(inp, value):

    inp.clear()

    inp.send_keys(value)

    sleep(1,2)

    try:

        option = wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//div[contains(@class,'typeahead')]//span")
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            option
        )

        sleep()

    except Exception as e:

        print("Typeahead failed:", e)


# ======================
# FILL INPUTS
# ======================

def fill_inputs(modal):

    inputs = modal.find_elements(By.XPATH, ".//input")

    for inp in inputs:

        try:

            if not inp.is_displayed():
                continue

            if inp.get_attribute("value"):
                continue

            label = inp.get_attribute("aria-label") or ""

            parent = inp.find_element(
                By.XPATH,
                "./ancestor::div[1]"
            ).text

            text = (label + parent).lower()


            if "city" in text or "location" in text:

                set_typeahead(inp, DEFAULT_CITY)


            elif "experience" in text:

                set_input(inp, YEARS_EXPERIENCE)


            elif "salary" in text or "ctc" in text:

                set_input(inp, EXPECTED_SALARY)


            elif "phone" in text:

                set_input(inp, PHONE_NUMBER)


            elif "email" in text:

                set_input(inp, EMAIL_VALUE)


            elif "notice" in text:

                set_input(inp, NOTICE_PERIOD)


            else:

                set_input(inp, "1")


        except:
            pass


# ======================
# DROPDOWN
# ======================

def handle_dropdown(modal):

    selects = modal.find_elements(By.TAG_NAME, "select")

    for sel in selects:

        try:

            s = Select(sel)

            s.select_by_index(1)

        except:
            pass


# ======================
# CLICK NEXT / SUBMIT
# ======================

def click_next(modal):

    buttons = modal.find_elements(By.TAG_NAME, "button")

    for btn in buttons:

        text = btn.text.lower()

        if text in ["next", "review", "submit application", "submit"]:

            driver.execute_script(
                "arguments[0].click();",
                btn
            )

            sleep(2,3)

            return text

    return None


# ======================
# DONE BUTTON
# ======================

def click_done():

    try:

        done = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Done']")
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            done
        )

        sleep()

    except:
        pass


# ======================
# APPLY JOB
# ======================

def apply_job(card):

    click_job_card(card)

    if not click_easy_apply():
        return False

    modal = get_modal()

    for _ in range(10):

        fill_inputs(modal)

        handle_dropdown(modal)

        action = click_next(modal)

        if action and "submit" in action:

            click_done()

            return True

    return False


# ======================
# NEXT PAGE
# ======================

def click_next_page():

    try:

        next_btn = driver.find_element(
            By.XPATH,
            "//button[.//span[text()='Next']]"
        )

        if "disabled" in next_btn.get_attribute("class"):
            return False

        driver.execute_script(
            "arguments[0].click();",
            next_btn
        )

        sleep(3,5)

        return True

    except:

        return False


# ======================
# MAIN
# ======================

def main():

    driver.get(JOB_URL)

    sleep(5,7)

    applied = []
    failed = []

    while len(applied) < MAX_APPLY:

        scroll_jobs_panel()

        cards = get_job_cards()

        print("Jobs on page:", len(cards))

        for card in cards:

            if len(applied) >= MAX_APPLY:
                break

            try:

                success = apply_job(card)

                if success:

                    applied.append("OK")

                    print(now(), "Applied")

                else:

                    failed.append("FAIL")

            except Exception as e:

                print("Error:", e)

                failed.append("ERROR")

            sleep(2,4)

        if not click_next_page():

            print("No more pages.")

            break


    pd.DataFrame(applied).to_excel(OUTPUT_APPLIED,index=False)

    pd.DataFrame(failed).to_csv(OUTPUT_FAILED,index=False)

    driver.quit()


# ======================

if __name__ == "__main__":
    main()
