import requests
from bs4 import BeautifulSoup
import json
import re
import csv
import os
from urllib.parse import urljoin
from PIL import Image
import io

def download_image(img_url, save_path):
    """Download and save an image from URL"""
    try:
        response = requests.get(img_url, stream=True)
        response.raise_for_status()
        
        # Check if content is actually an image
        content_type = response.headers.get('content-type', '')
        if 'image' not in content_type:
            return False
            
        # Save the image
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Error downloading image {img_url}: {e}")
        return False

def scrape_students_with_photos(url):
    # Create directories for photos
    os.makedirs('student_photos', exist_ok=True)
    os.makedirs('student_data', exist_ok=True)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    students = []
    
    # Get all text content
    all_text = soup.get_text()
    lines = [line.strip() for line in all_text.split('\n') if line.strip()]
    
    # Extract students using your method
    i = 0
    while i < len(lines) - 1:
        current_line = lines[i]
        next_line = lines[i + 1] if i + 1 < len(lines) else ""
        
        if re.match(r'^E/20/\d+$', next_line):
            students.append({
                'name': current_line,
                'registration_number': next_line,
                'photo_filename': ''
            })
            i += 2
        else:
            i += 1
    
    # Now find and download photos for each student
    print("Searching and downloading student photos...")
    
    # Find all images on the page
    img_tags = soup.find_all('img')
    
    for student in students:
        reg_number = student['registration_number']
        photo_found = False
        
        # Look for images that might belong to this student
        for img in img_tags:
            img_src = img.get('src', '')
            if img_src:
                # Check if this image is near the student's information
                parent = img.find_parent()
                if parent and reg_number in parent.get_text():
                    # Download the photo
                    full_img_url = urljoin(url, img_src)
                    photo_filename = f"{reg_number.replace('/', '_')}.jpg"
                    photo_path = os.path.join('student_photos', photo_filename)
                    
                    if download_image(full_img_url, photo_path):
                        student['photo_filename'] = photo_filename
                        student['photo_url'] = full_img_url  # Keep URL for reference
                        print(f"✅ Downloaded photo for {reg_number}")
                        photo_found = True
                        break
        
        if not photo_found:
            print(f"❌ No photo found for {reg_number}")
            student['photo_filename'] = 'No photo'
            student['photo_url'] = ''
    
    return students

# Main execution
url = "https://people.ce.pdn.ac.lk/students/e20/"

print("Scraping students and downloading photos...")
students = scrape_students_with_photos(url)

print(f"\nFound {len(students)} students")

# Save the data
if students:
    # Save as JSON
    json_path = os.path.join('student_data', 'students20_with_photos.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON data saved to {json_path}")
    
    # Save as CSV
    csv_path = os.path.join('student_data', 'students20_with_photos.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Registration Number', 'Photo Filename', 'Photo URL'])
        for student in students:
            writer.writerow([
                student['name'], 
                student['registration_number'], 
                student['photo_filename'],
                student.get('photo_url', '')
            ])
    print(f"✅ CSV data saved to {csv_path}")
    
    # Print summary
    photos_downloaded = sum(1 for s in students if s['photo_filename'] not in ['', 'No photo'])
    print(f"\n📊 Summary: {len(students)} students, {photos_downloaded} photos downloaded")
    print(f"📁 Photos saved in 'student_photos' folder")
    print(f"📁 Data saved in 'student_data' folder")

else:
    print("❌ No student data found.")