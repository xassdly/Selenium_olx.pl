#  OLX.pl Parser with Selenium

This is a simple Python project that uses **Selenium** to scrape product data (titles, prices and links) from [OLX.pl](https://www.olx.pl/).  
It demonstrates how to automate browsing, accept cookies, perform search queries and extract data from the dynamically loaded HTML.

---

##  Features
✅ Uses Selenium WebDriver (Chrome)  
✅ Accepts cookies automatically  
✅ Searches for a keyword on OLX.pl  
✅ Scrapes product titles and prices  
✅ Saves results to a CSV file

---

##  Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/olx-pl-scraper.git
   cd olx-pl-scraper
   ```

2. Install dependencies (you may want to use a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure you have Chrome installed and `chromedriver` in your PATH.

---

##  Usage

Edit the script or simply run:

```bash
python main.py
```

You can change the `query` inside the script to search for different products.

---

##  Example output

It will create a CSV file like:

```csv
Title,Price,Link
"iPhone 13 128GB","2 700 zł","https://www.olx.pl/d/oferta/iphone-13"
"Samsung Galaxy S22","1 900 zł","https://www.olx.pl/d/oferta/samsung-s22"
...
```
