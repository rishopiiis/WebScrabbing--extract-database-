import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_students(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if request was successful
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Debug: Save the raw HTML to see what we're working with
        with open('debug_page.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print("Saved raw HTML to debug_page.html for inspection")
        
        # Get all text content
        all_text = soup.get_text()
        lines = [line.strip() for line in all_text.split('\n') if line.strip()]
        
        print(f"Total lines found: {len(lines)}")
        print("First 20 lines:")
        for i, line in enumerate(lines[:20]):
            print(f"{i}: {line}")
        
        students = []
        
        # Method 1: Look for E/22/ pattern (for E22 batch)
        print("\n=== Searching for E/22/ pattern ===")
        for i, line in enumerate(lines):
            if re.search(r'E/22/\d+', line):
                print(f"Found registration at line {i}: {line}")
                # Look for name in previous lines
                name = find_name(lines, i)
                if name:
                    students.append({
                        'name': name,
                        'registration_number': line
                    })
                    print(f"Added: {name} - {line}")
        
        # Method 2: Alternative approach - look for specific patterns
        if not students:
            print("\nTrying alternative method...")
            for i in range(len(lines) - 1):
                current_line = lines[i]
                if (not re.search(r'E/22/\d+', current_line) and 
                    re.search(r'E/22/\d+', lines[i+1]) and
                    len(current_line) > 2):  # Name should be more than 2 characters
                    students.append({
                        'name': current_line,
                        'registration_number': lines[i+1]
                    })
        
        return students
        
    except Exception as e:
        print(f"Error: {e}")
        return []

def find_name(lines, reg_index):
    """Find the name preceding a registration number"""
    # Look backwards for the name
    for i in range(reg_index-1, max(-1, reg_index-5), -1):
        line = lines[i]
        # Skip lines that are clearly not names
        if (not re.search(r'E/22/\d+', line) and 
            not line.lower() in ['view', 'procurement', 'research', 'kaggle'] and
            len(line) > 2 and 
            not line.startswith('http')):
            return line
    return None

# Main execution
url = "https://people.ce.pdn.ac.lk/students/e20/"
print(f"Scraping from: {url}")

students = scrape_students(url)

print(f"\n=== RESULTS ===")
print(f"Total students found: {len(students)}")

if students:
    # Save as JSON
    with open('students_e20.json', 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=2, ensure_ascii=False)
    print("Saved to students_e20.json")
    
    # Save as CSV
    import csv
    with open('students_e20.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Registration Number'])
        for student in students:
            writer.writerow([student['name'], student['registration_number']])
    print("Saved to students_e20.csv")
    
    # Print the results
    print("\nStudent List:")
    for student in students:
        print(f"{student['name']} - {student['registration_number']}")
else:
    print("No students found. Check debug_page.html to see the actual page structure.")