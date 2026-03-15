# naukri_apply_final.py
# Naukri automation: only apply to jobs with in-site "Apply" (not "Apply on company site").
# Handles popups, multi-step forms, iframes, resume upload, and closes extra tabs.
#
# Requirements:
#   pip install selenium webdriver-manager pandas openpyxl
#
# Usage:
#   python naukri_apply_final.py


# & "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\Users\Dell\AppData\Local\Google\Chrome\User Data" --profile-directory="Profile 5"


import os
import time
import random
import pandas as pd
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException

# ================= CONFIG =================
PROFILE_PATH = r"C:\selenium-profile"   # change to your chrome profile
JOB_URL = "https://www.naukri.com/data-analyst-sql-power-bi-jobs?k=data%20analyst%2C%20sql%2C%20power%20bi&nignbevent_src=jobsearchDeskGNB&experience=0&jobAge=1"
# JOB_URL = "https://www.naukri.com/data-analyst-associate-analyst-mis-executive-jobs?k=data%20analyst%2C%20associate%20analyst%2C%20mis%20executive&nignbevent_src=jobsearchDeskGNB&experience=0&jobAge=1"
MAX_APPLY = 100

OUTPUT_FILE = "applied_jobs.xlsx"
FAILED_FILE = "failed_jobs.csv"
SKIPPED_FILE = "skipped_jobs.csv"

# Optional: resume file path to auto-upload (set to None to skip)
RESUME_PATH = None  # e.g. r"C:\Users\Prince\Documents\Resume.pdf"

# ================= DELAYS =================
def human_sleep_short():
    time.sleep(random.uniform(0.4, 0.9))

def human_sleep_med():
    time.sleep(random.uniform(1.2, 2.0))

def human_sleep_long():
    time.sleep(random.uniform(2.5, 4.0))

# ================= DRIVER =================
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={PROFILE_PATH}")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)
MAIN_TAB = None

print("Chrome opened successfully")

# ================= HELPERS =================
def now():
    return datetime.datetime.now().strftime("%H:%M:%S")

def safe_click(el):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        human_sleep_short()
        el.click()
        human_sleep_short()
        return True
    except ElementClickInterceptedException:
        try:
            driver.execute_script("arguments[0].click();", el)
            human_sleep_short()
            return True
        except Exception:
            return False
    except Exception:
        return False

def close_extra_tabs():
    """Close ALL tabs except MAIN_TAB and switch back to MAIN_TAB"""
    global MAIN_TAB
    handles = driver.window_handles
    for h in handles:
        if h != MAIN_TAB:
            try:
                driver.switch_to.window(h)
                time.sleep(0.6)
                driver.close()
            except Exception:
                pass
    driver.switch_to.window(MAIN_TAB)

def wait_for_new_tab(old_handles, timeout=10):
    end = time.time() + timeout
    while time.time() < end:
        handles = driver.window_handles
        if len(handles) > len(old_handles):
            new = [h for h in handles if h not in old_handles]
            if new:
                return new[-1]
        time.sleep(0.2)
    return None

# =============== APPLY BUTTON FINDERS ===============
def find_apply_button_in_doc(timeout=4):
    """
    Return the first clickable element whose text or attributes indicate an 'apply' action.
    """
    xpaths = [
        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'apply')]",
        "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'apply')]",
        "//button[contains(@class,'apply') or contains(@id,'apply')]",
        "//a[contains(@href,'apply') or contains(@href,'apply-now') or contains(@href,'applyonline')]",
    ]
    for xp in xpaths:
        try:
            el = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xp)))
            if el and el.is_displayed():
                return el
        except TimeoutException:
            continue
    return None

def find_iframe_with_apply():
    frames = driver.find_elements(By.TAG_NAME, "iframe")
    for f in frames:
        try:
            driver.switch_to.frame(f)
            el = find_apply_button_in_doc(timeout=2)
            driver.switch_to.default_content()
            if el:
                return f
        except Exception:
            driver.switch_to.default_content()
    return None

# =============== MODAL / FORM HANDLING ===============
def find_modal_container():
    queries = [
        "//div[@role='dialog' and not(contains(@style,'display:none'))]",
        "//div[contains(@class,'modal') and not(contains(@style,'display:none'))]",
        "//div[contains(@class,'popup') and not(contains(@style,'display:none'))]",
        "//form[contains(@class,'apply') or contains(@class,'application')]",
    ]
    for q in queries:
        try:
            el = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, q)))
            if el:
                return el
        except TimeoutException:
            continue
    return None

def fill_modal_fields(modal_element):
    try:
        # inputs
        inputs = modal_element.find_elements(By.XPATH, ".//input[not(@type='hidden')]")
        for inp in inputs:
            try:
                if not inp.is_displayed():
                    continue
                t = (inp.get_attribute("type") or "").lower()
                val = (inp.get_attribute("value") or "").strip()
                if val:
                    continue
                name = (inp.get_attribute("name") or "").lower()
                aria = (inp.get_attribute("aria-label") or "").lower()
                placeholder = (inp.get_attribute("placeholder") or "").lower()
                meta = " ".join([name, aria, placeholder])

                if t in ("radio", "checkbox"):
                    try:
                        if not inp.is_selected():
                            safe_click(inp)
                    except:
                        pass
                elif t == "file":
                    if RESUME_PATH and os.path.isfile(RESUME_PATH):
                        try:
                            inp.send_keys(RESUME_PATH)
                            human_sleep_short()
                        except Exception:
                            pass
                else:
                    if "phone" in meta or "mobile" in meta:
                        inp.send_keys("9999999999")
                    elif "email" in meta:
                        inp.send_keys("youremail@example.com")
                    elif "exp" in meta or "experience" in meta:
                        inp.send_keys("1")
                    elif "notice" in meta:
                        inp.send_keys("0")
                    elif "ctc" in meta or "salary" in meta:
                        inp.send_keys("300000")
                    else:
                        inp.send_keys("N/A")
                    human_sleep_short()
            except Exception:
                continue

        # textareas
        tas = modal_element.find_elements(By.XPATH, ".//textarea")
        for ta in tas:
            try:
                if not ta.is_displayed():
                    continue
                val = (ta.get_attribute("value") or "").strip()
                if val:
                    continue
                ta.send_keys("Please find my profile attached. Thanks.")
                human_sleep_short()
            except Exception:
                continue

        # selects
        selects = modal_element.find_elements(By.XPATH, ".//select")
        for sel in selects:
            try:
                if not sel.is_displayed():
                    continue
                s = Select(sel)
                if len(s.options) > 1:
                    s.select_by_index(1)
                else:
                    s.select_by_index(0)
                human_sleep_short()
            except Exception:
                continue

        # radios
        radios = modal_element.find_elements(By.XPATH, ".//input[@type='radio']")
        for r in radios:
            try:
                if r.is_displayed() and not r.is_selected():
                    safe_click(r)
                    human_sleep_short()
            except Exception:
                continue

        # checkboxes
        checks = modal_element.find_elements(By.XPATH, ".//input[@type='checkbox']")
        for c in checks:
            try:
                if c.is_displayed() and not c.is_selected():
                    safe_click(c)
                    human_sleep_short()
            except Exception:
                continue

    except Exception:
        pass

def click_next_or_submit_in_modal(modal_element):
    buttons = modal_element.find_elements(By.XPATH, ".//button|.//input[@type='button' or @type='submit']")
    order = ["next", "review", "submit", "apply", "finish", "continue", "confirm"]
    for b in buttons:
        try:
            label = (b.text or b.get_attribute("value") or "").strip().lower()
            for keyword in order:
                if keyword in label:
                    if safe_click(b):
                        human_sleep_med()
                        return True
        except Exception:
            continue
    # fallback: click any visible button
    for b in buttons:
        try:
            if b.is_displayed() and safe_click(b):
                human_sleep_med()
                return True
        except Exception:
            continue
    return False

def detect_application_success():
    page = driver.page_source.lower()
    keywords = ["thank you", "application submitted", "application received", "you have applied", "application successful", "we have received your application"]
    for k in keywords:
        if k in page:
            return True
    try:
        toast = driver.find_elements(By.XPATH, "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'applied') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'application submitted')]")
        if toast:
            return True
    except Exception:
        pass
    return False

def handle_modal_flow_on_current_window():
    human_sleep_short()
    modal = find_modal_container()
    if not modal:
        f = find_iframe_with_apply()
        if f:
            try:
                driver.switch_to.frame(f)
                modal = find_modal_container()
            except Exception:
                modal = None
            finally:
                driver.switch_to.default_content()

    if not modal:
        human_sleep_med()
        return detect_application_success()

    for step in range(6):
        try:
            fill_modal_fields(modal)
            clicked = click_next_or_submit_in_modal(modal)
            human_sleep_med()
            if detect_application_success():
                return True
            modal = find_modal_container()
            if not modal:
                if detect_application_success():
                    return True
                else:
                    human_sleep_short()
                    modal = find_modal_container()
                    if not modal:
                        break
        except Exception:
            break
    return detect_application_success()

# =============== APPLY FLOW WITH SKIP LOGIC ===============
def apply_to_job_anchor(job_el):
    title = job_el.text.strip() or job_el.get_attribute("href")
    print(now(), "Opening:", title)
    old_handles = driver.window_handles.copy()

    # open job tab by clicking anchor
    try:
        driver.execute_script("arguments[0].click();", job_el)
    except Exception:
        href = job_el.get_attribute("href")
        if href:
            driver.execute_script("window.open(arguments[0], '_blank');", href)
        else:
            print(now(), "No href - skipping")
            return False, title, "nohref"

    # wait for new tab
    new_handle = wait_for_new_tab(old_handles, timeout=8)
    if new_handle:
        driver.switch_to.window(new_handle)
        human_sleep_long()
    else:
        print(now(), "No new tab - continuing in current window")

    # Try to find apply element in document
    apply_el = find_apply_button_in_doc(timeout=3)
    # If not found in doc, check if iframe contains apply (we'll inspect iframe later if needed)
    if not apply_el:
        iframe = find_iframe_with_apply()
        if iframe:
            driver.switch_to.frame(iframe)
            apply_el = find_apply_button_in_doc(timeout=2)
            driver.switch_to.default_content()

    # If we found an apply element, examine its visible text to decide action
    if apply_el:
        try:
            raw_text = (apply_el.text or "").strip().lower()
        except Exception:
            raw_text = ""

        # If the button indicates external company apply, skip and click Save instead
        if "company" in raw_text or "company site" in raw_text or "apply on company site" in raw_text or "external" in raw_text:
            print(now(), "External/company-site apply detected -> will Save and skip applying.")
            # try to click Save button (if present)
            try:
                save_xpath = "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'save') or contains(@class,'save-job') or contains(@class,'save-job-button')]"
                save_btn = None
                try:
                    save_btn = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, save_xpath)))
                except Exception:
                    # try alternative selector by visible "Save" text
                    candidates = driver.find_elements(By.XPATH, "//button")
                    for c in candidates:
                        try:
                            txt = (c.text or "").strip().lower()
                            if txt == "save" or txt == "save job":
                                save_btn = c
                                break
                        except Exception:
                            continue
                if save_btn:
                    safe_click(save_btn)
                    human_sleep_short()
                else:
                    print(now(), "Save button not found (fallback).")
            except Exception:
                pass

            close_extra_tabs()
            return False, title, "skipped_company"

        # else: proceed to click the apply button (in-site apply)
        print(now(), "In-site Apply detected; attempting to click.")
        safe_click(apply_el)
        human_sleep_med()

        # handle modal / multi-step form that appears after clicking apply
        success = handle_modal_flow_on_current_window()

        close_extra_tabs()
        return success, title, "applied" if success else "failed_modal"

    # If apply element not found in both doc and iframe, try fallback links/buttons
    try:
        fallback_candidates = driver.find_elements(By.XPATH, "//*[contains(translate(@href,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'apply') or contains(translate(@id,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'apply') or contains(translate(@class,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'apply')]")
        for c in fallback_candidates:
            try:
                if c.is_displayed():
                    txt = (c.text or "").strip().lower()
                    # skip company-site candidates
                    if "company" in txt or "company site" in txt or "external" in txt:
                        continue
                    print(now(), "Fallback apply candidate clicked")
                    safe_click(c)
                    human_sleep_med()
                    success = handle_modal_flow_on_current_window()
                    close_extra_tabs()
                    return success, title, "applied" if success else "failed_modal"
            except Exception:
                continue
    except Exception:
        pass

    # debug snippet if nothing worked
    try:
        snippet = driver.page_source[:2000]
        print(now(), "DEBUG page snippet:", snippet.replace("\n", " ")[:800])
    except Exception:
        pass

    close_extra_tabs()
    return False, title, "no_apply_found"

# =============== RUN SCRIPT ===============
def main():
    global MAIN_TAB
    driver.get(JOB_URL)
    human_sleep_long()
    MAIN_TAB = driver.current_window_handle
    print(now(), "Job results page loaded")

    # scroll to load jobs
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    human_sleep_med()

    job_anchors = driver.find_elements(By.CSS_SELECTOR, "a.title")
    print(now(), "Total jobs found:", len(job_anchors))

    applied = []
    failed = []
    skipped = []

    count = 0
    for job in job_anchors:
        if count >= MAX_APPLY:
            break
        success, title, status = apply_to_job_anchor(job)
        if status == "applied":
            print(now(), "Applied:", title)
            applied.append(title)
        elif status in ("skipped_company", "nohref"):
            print(now(), "Skipped:", title, status)
            skipped.append(title)
        else:
            print(now(), "Failed:", title, status)
            failed.append(f"{title} - {status}")
        count += 1
        human_sleep_med()

    # Save results
    try:
        pd.DataFrame(applied, columns=["Applied Jobs"]).to_excel(OUTPUT_FILE, index=False)
        pd.DataFrame(failed, columns=["Failed Jobs"]).to_csv(FAILED_FILE, index=False)
        pd.DataFrame(skipped, columns=["Skipped Jobs"]).to_csv(SKIPPED_FILE, index=False)
    except Exception as e:
        print(now(), "Error saving files:", e)

    print(now(), "Done. Applied:", len(applied), "Failed:", len(failed), "Skipped:", len(skipped))
    driver.quit()

if __name__ == "__main__":
    main()
