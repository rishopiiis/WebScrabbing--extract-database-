# error version


import requests
from bs4 import BeautifulSoup
import json
import re
import csv
from urllib.parse import urljoin

def scrape_students_with_photos(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    students = []
    
    # Method 1: Look for student cards or list items
    student_elements = soup.find_all(['div', 'li', 'tr', 'p', 'strong'])
    
    for element in student_elements:
        text = element.get_text().strip()
        
        # Check if this element contains a registration number
        reg_match = re.search(r'(E/20/\d+)', text)
        if reg_match:
            reg_number = reg_match.group(1)
            
            # Find the name (usually before the registration number)
            name = extract_name(text, reg_number)
            
            # Find photo in this element or nearby
            photo_url = find_photo_url(element, url)
            
            if name:
                students.append({
                    'name': name.strip(),
                    'registration_number': reg_number,
                    'photo_url': photo_url
                })
    
    # Remove duplicates based on registration number
    unique_students = {}
    for student in students:
        reg = student['registration_number']
        if reg not in unique_students:
            unique_students[reg] = student
    
    return list(unique_students.values())

def extract_name(text, reg_number):
    """Extract name from text containing registration number"""
    # Remove the registration number and clean up
    name_part = text.replace(reg_number, '').strip()
    # Remove common suffixes and clean
    name_part = re.sub(r'[-•·\s]+$', '', name_part)
    return name_part

def find_photo_url(element, base_url):
    """Find photo URL in or near the given element"""
    # Look for img tag in the element
    img = element.find('img')
    if img and img.get('src'):
        return urljoin(base_url, img.get('src'))
    
    # Look in parent element
    parent = element.parent
    if parent:
        parent_img = parent.find('img')
        if parent_img and parent_img.get('src'):
            return urljoin(base_url, parent_img.get('src'))
    
    # Look in sibling elements
    if element.previous_sibling:
        prev_img = element.previous_sibling.find('img') if hasattr(element.previous_sibling, 'find') else None
        if prev_img and prev_img.get('src'):
            return urljoin(base_url, prev_img.get('src'))
    
    return 'No photo found'

# Main execution
url = "https://people.ce.pdn.ac.lk/students/e20/"

print("Scraping students with photos...")
students = scrape_students_with_photos(url)

print(f"\nFound {len(students)} students")
for student in students:
    print(f"✅ {student['name']} - {student['registration_number']}")
    if student['photo_url'] != 'No photo found':
        print(f"   📸 {student['photo_url']}")

# Save the data
if students:
    # Save as JSON
    with open('students20_with_photos.json', 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=2, ensure_ascii=False)
    print(f"\n✅ JSON data saved to students20_with_photos.json")
    
    # Save as CSV
    with open('students20_with_photos.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Registration Number', 'Photo URL'])
        for student in students:
            writer.writerow([student['name'], student['registration_number'], student['photo_url']])
    print(f"✅ CSV data saved to students20_with_photos.csv")
    
    # Print summary
    photos_found = sum(1 for s in students if s['photo_url'] != 'No photo found')
    print(f"\n📊 Summary: {len(students)} students, {photos_found} with photos")
    
else:
    print("❌ No student data found.")