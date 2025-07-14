# ⚡ EAV LLM Monitor

A lightweight pipeline for monitoring and classifying social media posts about **Rivian Electric Adventure Vehicle (EAV)** reliability issues using **web scraping**, **preprocessing**, and **LLM-based triage**.

This project is designed to simulate a real-world workflow where large language models assist engineering or product teams in **triaging social media signals** for early signs of product reliability problems.

---

## 🚀 Features

- ✅ Reddit scraper for collecting public user posts about Rivian vehicles
- ✅ Preprocessing to clean and filter post text
- ✅ GPT-powered classification for:
  - Is it about a **Rivian**?
  - Is it a **reliability issue**?
  - What **vehicle system** is affected?
  - What is the **severity**?
  - Is it a **firsthand account**?
- ✅ Output labeled CSVs for further analysis or dashboarding
- 🛠️ Modular architecture ready for expansion (Twitter/X, dashboard, etc.)

---

## 🧠 Example LLM Output

```json
{
  "is_rivian": "Yes",
  "is_issue": "Yes",
  "system": "charging",
  "severity": "High",
  "firsthand": "Yes"
}
```

---

## 📁 Project Structure

eav-llm-monitor/  
├── data/                # Raw and processed CSVs  
├── notebooks/           # Dev notebooks for exploration  
├── src/  
│   ├── scrape/          # Reddit scraping tools  
│   ├── preprocess/      # Text cleanup and prep  
│   ├── llm/             # Prompting + classification  
│   ├── utils/           # Paths, I/O, credentials  
│   └── main_pipeline.py # End-to-end execution  

---

## ⚙️ How to Run  
1. Install Requirements  
``` bash
pip install -r requirements.txt
```
  
2. Set Up Credentials  
Create src/utils/reddit_creds.json and src/utils/openai_creds.json (not tracked by Git) with your Reddit and OpenAI keys:  

```json
{
  "REDDIT_CLIENT_ID": "xxx",
  "REDDIT_SECRET": "xxx",
  "REDDIT_USER_AGENT": "eav-monitor/0.1"
}
{
  "OPENAI_API_KEY": "xxx"
}
```

3. (Eventually, WIP) Run the Full Pipeline
``` bash
python src/main_pipeline.py
```

This will:
* Scrape new Reddit posts
* Preprocess and clean the text
* Classify with GPT (based on instructions.json)
* Save to data/processed/

## 🧩 What's Next
* Add Twitter scraping using Selenium (with login/session handling)
* Build a dashboard for weekly issue trends
* Summarize trends over time or by system
* Include sample outputs and structured prompt testing

## ✍️ Author
Giancarlo Garbagnati
Data Analyst/Engineer with a passion for LLM workflows and real-world reliability use cases.