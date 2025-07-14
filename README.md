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