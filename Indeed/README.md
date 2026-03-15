# 🚀 Indeed Job Apply Automation Bot (Python + Selenium)

Automated **Indeed Job Application Bot** built using Python and Selenium that intelligently applies to jobs, handles multi-step applications, form filling, captcha detection, and pagination.

This project demonstrates real-world **browser automation, intelligent form handling, and scalable job application workflows** similar to automation systems used in productivity engineering.

---

# 🎯 Project Objective

Help job seekers automate repetitive job application tasks on Indeed by:

- Automatically applying to jobs with **Easy Apply / Apply on Indeed**
- Handling **multi-step job applications**
- Automatically filling job application forms
- Detecting **captcha challenges**
- Managing job pages with **pagination**
- Logging applied, failed, and captcha jobs

---

# ⚡ Key Features

## 🤖 Fully Automated Job Application

- Opens job listings automatically
- Detects **Apply on Indeed** buttons
- Applies to jobs automatically
- Processes multiple pages of job listings

---

## 🧠 Intelligent Form Filling

Automatically fills common job application fields:

- Name
- Email
- Phone number
- Location
- LinkedIn profile
- Salary expectations
- Experience
- Notice period
- Resume upload

The automation detects input fields using **labels, placeholders, and aria attributes**.

---

## 📑 Multi-Step Application Handling

Handles complex application workflows such as:

- Continue steps
- Review pages
- Submit application
- Confirmation messages

---

## 🔒 Captcha Detection

The bot detects:

- reCAPTCHA frames
- captcha widgets

If captcha appears:

- The tab remains open
- Application is logged as **captcha required**

---

## 📊 Job Tracking System

The bot generates structured reports:

| File | Description |
|-----|-------------|
| applied.xlsx | Successfully submitted applications |
| captcha.xlsx | Applications blocked by captcha |
| failed.xlsx | Applications that failed |

---

# 🧠 Automation Workflow

```

Open Indeed Job Search
↓
Collect Job Listings
↓
Open Job in New Tab
↓
Check Apply Button
↓
If External Apply → Skip
↓
If Apply on Indeed → Start Application
↓
Auto Fill Form Fields
↓
Handle Radio Buttons & Checkboxes
↓
Click Continue / Submit
↓
Detect Application Success
↓
Log Results
↓
Move to Next Job

```

---

# 🛠️ Tools & Technologies Used

## Programming Language

- Python 3

## Automation Framework

- Selenium WebDriver

## Browser Automation

- ChromeDriver
- Chrome Profile Automation

## Data Processing

- Pandas
- Excel file generation

## Automation Techniques

- XPath automation
- Form field detection
- Multi-step form automation
- Captcha detection
- Pagination automation

---

# 📊 Key Skills Demonstrated

- Browser Automation with Selenium
- Real-world Workflow Automation
- Dynamic Form Interaction
- Automation Script Engineering
- Error Handling in Automation
- Web Scraping and DOM Inspection
- Scalable Job Application Automation

---

# 📁 Project Structure

```

Indeed/
│
├── indeed.py
│
└── README.md

```

---

# ⚙️ Installation & Setup

## Step 1: Clone Repository

```

git clone [https://github.com/pk861510/Automation.git](https://github.com/pk861510/Automation.git)
cd Automation/Indeed

```

---

## Step 2: Install Dependencies

```

pip install -r requirements.txt

```

Required libraries:

```

selenium
pandas
openpyxl

```

---

## Step 3: Configure Settings

Inside the script update:

```

CONFIG = {

"resume_path": "path_to_resume",

"email": "your_email",

"phone": "your_phone",

"full_name": "your_name",

"linkedin": "linkedin_profile",

"location": "city"
}

```

---

## Step 4: Run Automation

```

python indeed_automation_v2_7.py

```

---

# 📈 Output Generated

The automation generates structured reports:

```

indeed_outputs/
│
├── applied.xlsx
├── captcha.xlsx
└── failed.xlsx

```

These files track the job application status.

---

# 💼 Real-World Value

This automation helps job seekers:

- Save **5–10 hours per week**
- Apply to **hundreds of jobs automatically**
- Avoid repetitive job applications
- Focus more on **interview preparation**

This project demonstrates automation skills useful in:

- Data Engineering
- QA Automation
- Workflow Automation
- Productivity Engineering
- Data Analyst Tooling

---

# 🧠 Learning Outcomes

Through this project I learned:

- Advanced Selenium automation
- Handling real-world job portals
- Dynamic form detection
- Captcha handling
- Multi-step application automation
- Browser tab management

---

# 🚀 Future Improvements

Planned enhancements:

- AI-based job filtering
- GPT-based auto answers
- Cover letter generation
- Cloud-based automation
- Resume optimization system

---

# 👨‍💻 Author

Prince Kumar  
Aspiring Data Analyst | Python Automation Developer  

LinkedIn  
https://www.linkedin.com/in/pk861510

GitHub  
https://github.com/pk861510

---

# ⭐ Support

If you found this project useful:

⭐ Star the repository  
🔁 Share on LinkedIn  
🚀 Follow for more automation and data analytics projects

---

# 📢 Disclaimer

This project is for **educational purposes only**.  
Please ensure compliance with Indeed's terms of service while using automation tools