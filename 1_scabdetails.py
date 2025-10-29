# import requests
# from bs4 import BeautifulSoup
# import json

# # Replace with the actual URL
# url = "https://people.ce.pdn.ac.lk/students/e20/"

# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')

# students = []

# # You'll need to inspect the actual HTML structure and adjust these selectors
# student_elements = soup.find_all(['strong', 'b', 'p'])  # Adjust based on actual structure

# for element in student_elements:
#     text = element.get_text(strip=True)
#     if 'E/20/' in text:
#         # Parse name and registration number
#         lines = [line.strip() for line in text.split('\n') if line.strip()]
#         if len(lines) >= 2:
#             students.append({
#                 'name': lines[0],
#                 'registration_number': lines[1]
#             })

# # Save as JSON
# with open('students.json', 'w') as f:
#     json.dump(students, f, indent=2)

# # Save as CSV
# import csv
# with open('students.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['Name', 'Registration Number'])
#     for student in students:
#         writer.writerow([student['name'], student['registration_number']])

#-----------------------------------------------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://people.ce.pdn.ac.lk/students/e20/"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

students = []

# Method 1: Look for E/20/ pattern in entire text
text_content = soup.get_text()
print("Looking for E/20/ pattern in text...")

# Find all registration numbers using regex
reg_numbers = re.findall(r'E/20/\d+', text_content)
print(f"Found {len(reg_numbers)} registration numbers: {reg_numbers}")

# Method 2: Extract based on the structure you showed
# Based on your sample, names are above registration numbers
lines = [line.strip() for line in text_content.split('\n') if line.strip()]
print(f"Found {len(lines)} lines of content")

# Process lines to find student data
for i, line in enumerate(lines):
    if line.startswith('E/20/'):
        # Registration number found, previous line might be name
        if i > 0:
            name = lines[i-1]
            students.append({
                'name': name,
                'registration_number': line
            })
            print(f"Found: {name} - {line}")

print(f"\nTotal students found: {len(students)}")

if students:
    # Save as JSON
    with open('student1.json', 'w') as f:
        json.dump(students, f, indent=2)
    print("Saved to student1.json")
    
    # Save as CSV
    import csv
    with open('student1.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Registration Number'])
        for student in students:
            writer.writerow([student['name'], student['registration_number']])
    print("Saved to student1.csv")
else:
    print("No students found. Let's debug further...")
    print("\nAll unique lines:")
    for i, line in enumerate(lines):
        print(f"{i}: {line}")