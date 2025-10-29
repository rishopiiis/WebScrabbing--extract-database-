# still url
import requests
from bs4 import BeautifulSoup
import json
import re
import csv
from urllib.parse import urljoin

url = "https://people.ce.pdn.ac.lk/students/e20/"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

students = []

# Find all images first and map them
all_images = soup.find_all('img')
print(f"Found {len(all_images)} images on the page")

# Get text content
all_text = soup.get_text()
lines = [line.strip() for line in all_text.split('\n') if line.strip()]

# Extract students using your original method
i = 0
while i < len(lines) - 1:
    current_line = lines[i]
    next_line = lines[i + 1] if i + 1 < len(lines) else ""
    
    if re.match(r'^E/20/\d+$', next_line):
        # Try to find a photo near this student
        photo_url = 'No photo found'
        
        # Search for images that might be related to this student
        for img in all_images:
            img_src = img.get('src', '')
            if img_src:
                # Check if this image is near the student's text
                parent_text = img.find_parent().get_text() if img.find_parent() else ""
                if current_line in parent_text or next_line in parent_text:
                    photo_url = urljoin(url, img_src)
                    break
        
        students.append({
            'name': current_line,
            'registration_number': next_line,
            'photo_url': photo_url
        })
        i += 2
    else:
        i += 1

print(f"\nFound {len(students)} students")
for student in students:
    photo_status = "✅" if student['photo_url'] != 'No photo found' else "❌"
    print(f"{photo_status} {student['name']} - {student['registration_number']}")

# Save data
if students:
    # JSON
    with open('students20_with_photos.json', 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=2, ensure_ascii=False)
    
    # CSV
    with open('students20_with_photos.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Registration Number', 'Photo URL'])
        for student in students:
            writer.writerow([student['name'], student['registration_number'], student['photo_url']])
    
    print(f"\n✅ Saved {len(students)} students with photo URLs")