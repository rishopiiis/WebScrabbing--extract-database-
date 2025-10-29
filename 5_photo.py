import requests
from bs4 import BeautifulSoup
import json
import re
import csv
from urllib.parse import urljoin

url = "https://people.ce.pdn.ac.lk/students/e20/"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Get all text and split by lines
all_text = soup.get_text()
lines = [line.strip() for line in all_text.split('\n') if line.strip()]

students = []

# Extract photo URLs by looking for img tags
print("Searching for student photos...")
img_tags = soup.find_all('img')
photo_map = {}

for img in img_tags:
    src = img.get('src', '')
    alt = img.get('alt', '')
    
    # Look for images that might be student photos
    if src and any(photo_indicator in src.lower() for photo_indicator in ['photo', 'image', 'img', 'student', 'e20', '.jpg', '.jpeg', '.png']):
        # Get the full URL for the image
        full_photo_url = urljoin(url, src)
        
        # Try to find associated name or registration number
        parent = img.find_parent()
        if parent:
            parent_text = parent.get_text()
            # Look for registration numbers in the parent element
            reg_match = re.search(r'E/20/\d+', parent_text)
            if reg_match:
                reg_number = reg_match.group()
                photo_map[reg_number] = full_photo_url
                print(f"Found photo for {reg_number}: {full_photo_url}")

# Look for patterns: Name followed by E/20/ number
i = 0
while i < len(lines) - 1:
    current_line = lines[i]
    next_line = lines[i + 1] if i + 1 < len(lines) else ""
    
    # If next line is a registration number, current line is likely the name
    if re.match(r'^E/20/\d+$', next_line):
        # Find photo for this registration number
        photo_url = photo_map.get(next_line, 'No photo found')
        
        students.append({
            'name': current_line,
            'registration_number': next_line,
            'photo_url': photo_url
        })
        i += 2  # Skip next line since we used it
    else:
        i += 1

print(f"\nFound {len(students)} students")
for student in students:
    print(f"{student['name']} - {student['registration_number']} - Photo: {student['photo_url']}")

# Save the data
if students:
    # Save as JSON
    with open('students20_with_photos.json', 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=2, ensure_ascii=False)
    print("\nData saved to students20_with_photos.json")
    
    # Save as CSV
    with open('students20_with_photos.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Registration Number', 'Photo URL'])
        for student in students:
            writer.writerow([student['name'], student['registration_number'], student['photo_url']])
    print("Data saved to students20_with_photos.csv")
    
else:
    print("No data found.")