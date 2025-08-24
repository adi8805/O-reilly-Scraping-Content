
# 📘 O'Reilly Books & Courses Scraper

A **Playwright-based asynchronous scraper** for extracting **books and course metadata** from [O'Reilly Online Learning](https://www.oreilly.com/).  
Scrapes titles, categories, authors, page count/duration, and publisher information efficiently, saving directly into a CSV.

---

## 📌 Features
- 🚀 **Asynchronous scraping** using `playwright` and `asyncio` for speed  
- 🖥 Supports **dynamic content rendering** (JS-loaded pages)  
- 💾 **Continuous CSV export** during scraping  
- 🔁 Handles **pagination automatically**  
- 🔧 Skips overlays, popups, and cookie banners for smooth scraping  

---

## 📥 Installation

Ensure you have **Python 3.7+** installed, then install dependencies:

```bash
git clone https://github.com/adi8805/O-reilly-Scraping-Content
cd oreilly-scraper
pip install -r requirements.txt
````


Install Playwright browsers:

```bash
python -m playwright install
```

---

## ⚡ Usage

```bash
python3 scraper.py
```

By default, it scrapes the first **100 results per page** and iterates through all available pages automatically, saving data to `oreilly_full_data.csv`.

---

### **Custom Modifications**

- Change **output CSV file name**:
    

```python
with open('my_oreilly_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    ...
```

- Adjust **headless mode**:
    

```python
browser = await p.chromium.launch(headless=True)  # Run in background without GUI
```

---

## 🖥 Expected Output

```text
Scraping page 1...
Python Basics | Book | John Doe | 350 pages | O'Reilly
JavaScript Essentials | Book | Jane Smith | 420 pages | O'Reilly
Scraping page 2...
Scraping complete; data saved to oreilly_full_data.csv
```

---

## 📊 CSV Output Format

|title|category|author|page_count_or_duration|publisher|
|---|---|---|---|---|
|Python Basics|Book|John Doe|350 pages|O'Reilly|
|JavaScript Essentials|Book|Jane Smith|420 pages|O'Reilly|
|Advanced Machine Learning|Course|Alex Johnson|3h 45m|O'Reilly|

---

## ⚙️ Script Overview

|Variable|Description|Default|
|---|---|---|
|`url`|Base search URL for O'Reilly content|`https://www.oreilly.com/search/skills/?rows=100`|
|`fieldnames`|CSV columns|`['title','category','author','page_count_or_duration','publisher']`|
|`oreilly_full_data.csv`|Output CSV filename|`oreilly_full_data.csv`|
|`headless`|Browser UI visibility|`False` (change to `True` for background)|

---

## 📜 License

This project is licensed under the **MIT License**.  
Feel free to use, modify, and distribute.

---

## 🤝 Contributing

Contributions are welcome!  
Fork the repo, make your changes, and submit a pull request.

---

## ⚠️ Disclaimer

This tool is for **educational and research purposes only**.  
Scraping websites without permission may violate their terms of service — use responsibly.
