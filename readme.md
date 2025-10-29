Student Data Scraper with Photo Download
📋 Project Overview
A Python web scraper that extracts student information (names, registration numbers) and downloads their profile photos from university websites. The tool automatically organizes data into JSON/CSV formats and saves actual image files locally.

🚀 Technology Stack
Core Technologies
Python 3.7+ - Primary programming language

BeautifulSoup4 - HTML parsing and web scraping

Requests - HTTP requests and file downloading

PIL (Pillow) - Image processing (optional)

Libraries Used
python
import requests       # HTTP requests and file downloads
import BeautifulSoup  # HTML parsing
import json          # JSON file operations
import csv           # CSV file operations
import re            # Regular expressions
import os            # File system operations
from urllib.parse import urljoin  # URL handling
Output Formats
JSON - Structured data storage

CSV - Spreadsheet-compatible format

JPG/PNG - Downloaded image files

🎯 Purpose & Features
Primary Purpose
Automate the extraction of student data from university department websites for:

Student database creation

Attendance systems

ID card generation

Academic administration

Research and analytics

Key Features
Multi-format Data Extraction

Student names and registration numbers

Profile photo URLs and local file paths

Batch Processing

Handle multiple student batches (E20, E21, E22, etc.)

Process entire department pages automatically

File Management

Automatic folder creation

Organized file naming

Local photo storage

Flexible Output

JSON for applications

CSV for spreadsheets

Local image files

📁 Project Structure
text
student_scraper/
│
├── scraper.py                 # Main scraping script
├── student_data/              # Generated data folder
│   ├── students_e20.json      # JSON output
│   └── students_e20.csv       # CSV output
├── student_photos/            # Downloaded images
│   ├── E_20_001.jpg
│   ├── E_20_002.jpg
│   └── ...
└── README.md                  # This file
⚙️ Installation & Setup
Prerequisites
bash
# Install required packages
pip install requests beautifulsoup4 pillow
Basic Usage
python
# Simple execution
python scraper.py

# Custom URL and batch
python scraper.py --url "https://people.ce.pdn.ac.lk/students/e20/" --batch "e20"
✅ Advantages
Pros
Time Efficiency

Automates manual data collection

Processes hundreds of students in minutes

Accuracy

Reduces human error in data entry

Consistent formatting across all records

Completeness

Captures both textual data and images

Creates comprehensive student profiles

Flexibility

Adaptable to different website structures

Configurable for various batches

Multiple output formats

Cost-Effective

No manual data entry costs

Uses free/open-source tools

⚠️ Limitations & Challenges
Cons
Website Dependency

Breaks if website structure changes

Requires updates for different university sites

Technical Limitations

Cannot handle JavaScript-heavy websites

May miss dynamically loaded content

Photo matching accuracy varies

Ethical Considerations

Must respect robots.txt and terms of service

Potential copyright issues with photos

Privacy concerns with student data

Technical Requirements

Requires stable internet connection

Needs sufficient storage for images

Python environment setup

Common Issues
Photo Detection

False positives/negatives in image matching

Inconsistent photo naming conventions

Data Parsing

Variations in name formatting

Special character handling

Inconsistent HTML structures

Performance

Large batches may take significant time

Memory usage with high-resolution images

🔧 Customization
Modifying for Different Websites
python
# Adjust these selectors based on target website
STUDENT_SELECTORS = ['div.student-card', 'li.student-item', 'tr']
PHOTO_SELECTORS = ['img.profile-photo', 'img.avatar', 'img.student-image']
Configuration Options
Batch codes (E20, E21, E22, etc.)

Output directory structure

Image quality and format

Data fields to extract

🛡️ Ethical Usage Guidelines
Responsible Scraping
Check robots.txt before scraping

Respect rate limits - add delays between requests

Use for legitimate purposes only

Comply with data protection laws (GDPR, FERPA, etc.)

Securely store collected data

Legal Considerations
Obtain permission when required

Respect copyright on images

Follow university data policies

Use data only for intended purposes

📈 Future Enhancements
Potential Improvements
Advanced Features

GUI interface

Scheduled scraping

Database integration

Cloud storage support

Technical Upgrades

Selenium integration for JS sites

AI-based image recognition

API-based data fetching

Multi-threaded downloading

User Experience

Progress bars

Error reporting

Configuration files

Logging system

🐛 Troubleshooting
Common Solutions
No data found

Check website accessibility

Verify URL and selectors

Inspect page structure changes

Photos not downloading

Check image URL construction

Verify file permissions

Ensure sufficient storage

Encoding issues

Use UTF-8 encoding for files

Handle special characters

Validate JSON output

📄 License
This project is intended for educational and administrative purposes. Users are responsible for complying with relevant laws and institutional policies when deploying this tool.

Note: Always use web scraping responsibly and ethically. Ensure you have proper authorization before collecting data from websites.
