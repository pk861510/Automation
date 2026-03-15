
---

# 🚀 Naukri Job Apply Automation Bot (Python + Selenium)

Automated **Naukri Job Application Bot** built using Python and Selenium that intelligently applies to jobs with **in-site "Apply" buttons**, handles multi-step application forms, popups, iframes, and automatically logs applied, skipped, and failed job applications.

This project demonstrates real-world **browser automation, workflow automation, dynamic form handling, and job application scaling** similar to automation tools used in productivity engineering.

---

# 🎯 Project Objective

Help job seekers automate repetitive Naukri job application workflows by:

* Automatically applying to jobs with **Naukri in-site Apply**
* Skipping jobs that redirect to **company websites**
* Handling **multi-step application forms**
* Filling **common job application fields automatically**
* Managing **popups, iframes, and dynamic forms**
* Logging applied, failed, and skipped jobs

---

# ⚡ Key Features

## 🤖 Automated Job Applications

* Automatically opens job listings
* Applies to jobs with **"Apply" button**
* Skips jobs with **"Apply on company site"**
* Processes multiple job listings automatically

## 🧠 Intelligent Form Filling

Automatically fills common job application fields:

* Phone number
* Email
* Experience
* Expected salary
* Notice period
* Radio buttons
* Checkboxes
* Dropdown fields
* Textarea responses

## 📑 Multi-Step Application Handling

Handles complex application workflows including:

* Next step forms
* Review steps
* Submit forms
* Confirmation screens

## 🧩 Iframe and Popup Handling

Many job applications appear inside **modals or iframes**.
The bot intelligently detects and interacts with:

* Modal dialogs
* Embedded iframes
* Dynamic form containers

## 📊 Smart Job Filtering

The bot ensures:

* Only **Naukri in-site applications** are submitted
* Jobs redirecting to **external company sites are skipped**
* Saved jobs are marked when external apply is detected

## 🔒 Safe Automation Features

* Handles **stale elements**
* Uses **human-like delays**
* Automatically closes extra browser tabs
* Detects successful applications
* Prevents crashes during automation

---

# 🧠 Automation Workflow

```
Open Naukri Job Search Page
        ↓
Load Job Listings
        ↓
Open Job in New Tab
        ↓
Check Apply Button
        ↓
If External Apply → Skip & Save Job
        ↓
If In-Site Apply → Click Apply
        ↓
Detect Modal / Form
        ↓
Auto Fill Fields
        ↓
Handle Multi-Step Form
        ↓
Submit Application
        ↓
Log Result
        ↓
Move to Next Job
```

---

# 🛠️ Tools & Technologies Used

## Programming Language

* Python 3

## Automation Framework

* Selenium WebDriver

## Browser Automation

* ChromeDriver
* Webdriver Manager

## Data Handling

* Pandas

## Automation Techniques

* XPath automation
* CSS selectors
* Modal form automation
* Iframe detection
* Multi-step workflow automation
* Browser tab management

---

# 📊 Key Skills Demonstrated

* Browser Automation using Selenium
* Real-world Workflow Automation
* Dynamic Web Form Handling
* Web Scraping & Interaction
* Error Handling in Automation
* Browser Session Management
* Automation Script Debugging
* Scalable Job Application Automation



# ⚙️ Installation & Setup

## Step 1: Clone Repository

```
Clone The Repository
```

---

## Step 2: Install Dependencies

```
pip install selenium webdriver-manager pandas openpyxl
```

---

## Step 3: Run the Automation Script

```
python naukri_apply_final.py
```

---

# 📈 Output Generated

## applied_jobs.xlsx

Contains list of successfully applied jobs.

## failed_jobs.csv

Contains job applications that failed due to form or automation issues.

## skipped_jobs.csv

Contains jobs skipped because they redirect to **external company websites**.

---

# 💼 Real-World Value

This automation helps job seekers:

* Save **5–10 hours per week**
* Apply to **large numbers of jobs automatically**
* Avoid repetitive manual job applications
* Focus more on **interview preparation instead of repetitive tasks**

It demonstrates real-world **automation engineering and workflow optimization skills** useful in:

* Data Engineering
* Automation Engineering
* QA Automation
* Productivity Engineering
* Data Analyst tooling

---

# 🧠 Learning Outcomes

Through this project, I learned:

* Advanced Selenium automation
* Handling dynamic web pages
* Modal and iframe automation
* Multi-step form automation
* Browser tab management
* Debugging real-world automation workflows

---

# 🚀 Future Improvements

Possible enhancements:

* AI-based job filtering
* Resume auto-upload automation
* Cover letter generation using GPT
* Cloud-based automation
* Scheduled job search automation
* Job recommendation system

---

# 👨‍💻 Author

Prince Kumar
Aspiring Data Analyst | Python Automation Developer

LinkedIn:
[https://www.linkedin.com/in/pk861510](https://www.linkedin.com/in/pk861510)

GitHub:
[https://github.com/pk861510](https://github.com/pk861510)

---

# ⭐ Support

If you found this project useful:

* Star the repository ⭐
* Share on LinkedIn 🔁
* Follow me for more automation and data analytics projects 🚀

---

# 📢 Disclaimer

This project is for **educational purposes only**.
Please ensure you follow Naukri's terms of service while using automation tools.

---

If you want, I can also help you **make this README even stronger for recruiters** by adding:

* **Architecture diagram**
* **Automation screenshots**
* **demo GIF**
* **better GitHub structure**

That will make your GitHub profile look **10× more professional for data/automation roles**.
