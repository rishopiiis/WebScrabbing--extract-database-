from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import re
import time

def scrape_with_selenium(url):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize the driver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(3)  # Wait for page to load
        
        # Get page source
        page_source = driver.page_source
        
        # Save for debugging
        with open('debug_selenium.html', 'w', encoding='utf-8') as f:
            f.write(page_source)
        print("Saved Selenium HTML to debug_selenium.html")
        
        # Parse with BeautifulSoup
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Extract text and process
        all_text = soup.get_text()
        lines = [line.strip() for line in all_text.split('\n') if line.strip()]
        
        students = []
        for i, line in enumerate(lines):
            if re.search(r'E/22/\d+', line):
                # Look for name in previous non-empty lines
                for j in range(i-1, max(-1, i-10), -1):
                    prev_line = lines[j]
                    if (not re.search(r'E/22/\d+', prev_line) and 
                        len(prev_line) > 2 and
                        not any(keyword in prev_line.lower() for keyword in ['view', 'http', 'research'])):
                        students.append({
                            'name': prev_line,
                            'registration_number': line
                        })
                        break
        
        return students
        
    finally:
        driver.quit()

# Try Selenium approach if regular scraping fails
print("Trying Selenium approach...")
students = scrape_with_selenium("https://people.ce.pdn.ac.lk/students/e22/")

if students:
    with open('students_e22_selenium.json', 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=2, ensure_ascii=False)
    print(f"Found {len(students)} students with Selenium")
else:
    print("Selenium also found no students.")