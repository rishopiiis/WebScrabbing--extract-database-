import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://people.ce.pdn.ac.lk/students/e20/"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Get all text and split by lines
all_text = soup.get_text()
lines = [line.strip() for line in all_text.split('\n') if line.strip()]

students = []

# Look for patterns: Name followed by E/20/ number
i = 0
while i < len(lines) - 1:
    current_line = lines[i]
    next_line = lines[i + 1] if i + 1 < len(lines) else ""
    
    # If next line is a registration number, current line is likely the name
    if re.match(r'^E/20/\d+$', next_line):
        students.append({
            'name': current_line,
            'registration_number': next_line
        })
        i += 2  # Skip next line since we used it
    else:
        i += 1

print(f"Found {len(students)} students")
for student in students:
    print(f"{student['name']} - {student['registration_number']}")

# Save the data
if students:
    with open('students20.json', 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=2, ensure_ascii=False)
    print("\nData saved to students20.json")
else:
    print("No data found. Please share the actual URL for more specific help.")