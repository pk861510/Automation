# indeed_automation_v2_7.py
# FINAL STABLE VERSION

import time, random, re
from pathlib import Path
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


# ================= CONFIG =================

CONFIG = {

    "start_url":
    "https://in.indeed.com/jobs?q=data+analyst&l=Pune",

    # FIXED LOGIN PROFILE
    "chrome_user_data_dir":
    r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data",

    "chrome_profile_directory":
    "Profile 5",

    "resume_path": r"D:\resume.pdf",

    "email": "your_email@example.com",

    "phone": "9999999999",

    "full_name": "Prince Kumar",

    "linkedin": "https://linkedin.com/in/prince",

    "location": "Pune",

    "current_company": "Fresher",

    "salary": "600000",

    "experience_years": "2",

    "notice_period": "30",

    "max_pages": 5,

    "output_dir": "indeed_outputs",
}

Path(CONFIG["output_dir"]).mkdir(exist_ok=True)

APPLIED_XLSX = Path(CONFIG["output_dir"]) / "applied.xlsx"
CAPTCHA_XLSX = Path(CONFIG["output_dir"]) / "captcha.xlsx"
FAILED_XLSX  = Path(CONFIG["output_dir"]) / "failed.xlsx"


# ================= DRIVER =================

def build_driver():

    opts = webdriver.ChromeOptions()

    # USE REAL CHROME PROFILE
    opts.add_argument(
        f"--user-data-dir={CONFIG['chrome_user_data_dir']}"
    )

    opts.add_argument(
        f"--profile-directory={CONFIG['chrome_profile_directory']}"
    )

    opts.add_argument("--start-maximized")

    opts.add_experimental_option(
        "excludeSwitches", ["enable-automation"]
    )

    opts.add_experimental_option(
        "useAutomationExtension", False
    )

    opts.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=opts)

    driver.implicitly_wait(5)

    return driver


# ================= HELPERS =================

def sleep(a=0.8, b=1.6):
    time.sleep(random.uniform(a, b))


def normalize(text):
    return re.sub(r"\s+", " ", (text or "").lower())


# ================= CAPTCHA =================

def detect_captcha(driver):

    try:

        frames = driver.find_elements(By.TAG_NAME, "iframe")

        for f in frames:

            src = (f.get_attribute("src") or "").lower()

            if "recaptcha" in src and f.is_displayed():
                return True

        els = driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'captcha') or contains(@class,'recaptcha')]"
        )

        for e in els:

            if e.is_displayed():
                return True

    except:
        pass

    return False


# ================= CHECKBOX =================

def handle_checkboxes(driver):

    boxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")

    for box in boxes:

        try:

            if not box.is_displayed():
                continue

            if box.is_selected():
                continue

            driver.execute_script(
                "arguments[0].click();",
                box
            )

            sleep(0.3,0.6)

        except:
            pass


# ================= RADIO BUTTONS =================

def handle_radio_buttons(driver):

    radios = driver.find_elements(By.XPATH, "//input[@type='radio']")

    groups = {}

    for r in radios:
        try:
            name = r.get_attribute("name")
            if not name:
                continue
            groups.setdefault(name, []).append(r)
        except:
            pass


    for group_name, group in groups.items():

        try:

            container = group[0].find_element(
                By.XPATH,
                "./ancestor::*[self::div or self::fieldset][1]"
            )

            question = normalize(container.text)


            choose_yes_keywords = [
                "bachelor","degree","experience","excel",
                "python","sql","power bi","work in",
                "eligible","authorized"
            ]

            choose_no_keywords = [
                "criminal","convicted","offence","bond"
            ]


            if any(k in question for k in choose_no_keywords):
                target = "no"

            elif any(k in question for k in choose_yes_keywords):
                target = "yes"

            else:
                target = "yes"


            for r in group:

                label = driver.find_element(
                    By.XPATH,
                    f"//label[@for='{r.get_attribute('id')}']"
                )

                label_text = normalize(label.text)

                if target in label_text:

                    driver.execute_script(
                        "arguments[0].click();",
                        r
                    )

                    sleep(0.3, 0.6)

                    break

        except:
            pass


# ================= INPUT HANDLER =================

def fill_inputs(driver):

    elements = driver.find_elements(
        By.XPATH,
        "//input | //textarea | //select"
    )

    for el in elements:

        try:

            if not el.is_displayed():
                continue

            tag = el.tag_name
            value = (el.get_attribute("value") or "").strip()

            label_text = ""

            label_text += el.get_attribute("aria-label") or ""
            label_text += " " + (el.get_attribute("placeholder") or "")

            field_id = el.get_attribute("id")

            if field_id:
                try:
                    label = driver.find_element(
                        By.XPATH,
                        f"//label[@for='{field_id}']"
                    )
                    label_text += " " + label.text
                except:
                    pass

            label = normalize(label_text)

            if tag == "input":

                typ = el.get_attribute("type")

                if typ in ["radio", "checkbox", "hidden"]:
                    continue

                if typ == "file":
                    if not value:
                        el.send_keys(CONFIG["resume_path"])
                    continue


                if typ in ["text","email","tel","number"]:

                    if value:
                        continue

                    if "email" in label:
                        el.send_keys(CONFIG["email"])

                    elif "phone" in label or "mobile" in label:
                        el.send_keys(CONFIG["phone"])

                    elif "linkedin" in label:
                        el.send_keys(CONFIG["linkedin"])

                    elif "company" in label:
                        el.send_keys(CONFIG["current_company"])

                    elif "location" in label or "city" in label:
                        el.send_keys(CONFIG["location"])

                    elif "qualification" in label:
                        el.send_keys("Bachelor's")

                    elif "name" in label:
                        el.send_keys(CONFIG["full_name"])

                    elif "salary" in label or "ctc" in label:
                        el.send_keys(CONFIG["salary"])

                    elif "experience" in label:
                        el.send_keys(CONFIG["experience_years"])

                    elif "notice" in label:
                        el.send_keys(CONFIG["notice_period"])

                    else:
                        el.send_keys("NA")


            elif tag == "textarea":

                if not value:
                    el.send_keys(
                        "I am interested in this role and available to join immediately."
                    )


            elif tag == "select":

                try:
                    Select(el).select_by_index(1)
                except:
                    pass

        except:
            pass


# ================= BUTTON =================

def click_continue(driver):

    buttons = driver.find_elements(
        By.XPATH,
        "//button | //input[@type='submit']"
    )

    keywords = ["continue","next","review","submit","apply"]

    for b in buttons:

        try:

            txt = normalize(
                b.text or b.get_attribute("value")
            )

            if any(k in txt for k in keywords):

                driver.execute_script(
                    "arguments[0].click();", b
                )

                sleep()

                return True

        except:
            pass

    return False


# ================= FIND APPLY BUTTON =================

def find_apply_button(driver):

    xpaths = [

        "//button[contains(.,'Apply')]",
        "//button[contains(.,'Apply Now')]",
        "//button[contains(.,'Apply on Indeed')]"

    ]

    for xp in xpaths:

        try:

            btn = driver.find_element(By.XPATH, xp)

            if btn.is_displayed():
                return btn

        except:
            pass

    return None


# ================= APPLY =================

def apply_to_job(driver, url, title):

    result = {"title": title, "url": url}

    main_tab = driver.current_window_handle

    driver.execute_script(
        "window.open(arguments[0]);", url
    )

    driver.switch_to.window(
        driver.window_handles[-1]
    )

    sleep()


    if detect_captcha(driver):

        result["status"] = "captcha"

        print(" -> captcha tab kept open")

        driver.switch_to.window(main_tab)

        return result


    if "apply on company site" in driver.page_source.lower():

        result["status"] = "external"

        driver.close()

        driver.switch_to.window(main_tab)

        return result


    btn = find_apply_button(driver)

    if not btn:

        result["status"] = "no_apply_button"

        driver.close()

        driver.switch_to.window(main_tab)

        return result


    btn.click()

    sleep()


    for _ in range(20):

        if detect_captcha(driver):

            result["status"] = "captcha"

            print(" -> captcha tab kept open")

            driver.switch_to.window(main_tab)

            return result


        fill_inputs(driver)
        handle_radio_buttons(driver)
        handle_checkboxes(driver)

        click_continue(driver)

        sleep()


        if "application submitted" in driver.page_source.lower():

            result["status"] = "submitted"

            driver.close()

            driver.switch_to.window(main_tab)

            return result


    result["status"] = "failed"

    driver.close()

    driver.switch_to.window(main_tab)

    return result


# ================= COLLECT JOBS =================

def collect_jobs(driver):

    jobs = []

    seen = set()

    anchors = driver.find_elements(
        By.XPATH,
        "//a[contains(@href,'/rc/clk')]"
    )

    for a in anchors:

        url = a.get_attribute("href")

        title = a.text

        if url and url not in seen:

            seen.add(url)

            jobs.append((url,title))

    return jobs


# ================= MAIN =================

def run():

    driver = build_driver()

    applied, captcha, failed = [], [], []

    driver.get(CONFIG["start_url"])

    sleep()


    for page in range(CONFIG["max_pages"]):

        jobs = collect_jobs(driver)

        print(f"\nPage {page+1}: {len(jobs)} jobs")


        for url,title in jobs:

            print("Applying:", title)

            res = apply_to_job(driver,url,title)

            st = res["status"]

            print(" ->", st)


            if st == "submitted":
                applied.append(res)

            elif st == "captcha":
                captcha.append(res)

            else:
                failed.append(res)


            sleep()


        try:

            nxt = driver.find_element(
                By.XPATH,
                "//a[@aria-label='Next']"
            )

            nxt.click()

            sleep()

        except:

            break


    pd.DataFrame(applied).to_excel(APPLIED_XLSX,index=False)
    pd.DataFrame(captcha).to_excel(CAPTCHA_XLSX,index=False)
    pd.DataFrame(failed).to_excel(FAILED_XLSX,index=False)


    print("\nDone")
    print("Applied:", len(applied))
    print("Captcha tabs open:", len(captcha))
    print("Failed:", len(failed))


if __name__ == "__main__":
    run()