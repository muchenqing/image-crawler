import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://skri.cnmiw.com/img/Pixivusers/45015081/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Fetch New.php
page = 1
new_php_url = urljoin(url, f'New.php?page={page}')
response = requests.get(new_php_url, headers=headers)
response.raise_for_status()

# Save the content to a file
with open('new_php.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

print("New.php content saved to new_php.html")
print("First 500 characters:")
print(response.text[:500])

# Parse and analyze
soup = BeautifulSoup(response.content, 'lxml')

# Check for any links or data that might contain original image URLs
print("\nChecking for original image links...")
links = soup.find_all('a')
for link in links:
    href = link.get('href')
    if href and 'original' in href:
        print(f"Found original image link: {href}")

# Check for any data attributes or scripts that might contain original image URLs
print("\nChecking for data attributes...")
data_tags = soup.find_all('[data-original]')
for tag in data_tags:
    original_url = tag.get('data-original')
    print(f"Found data-original: {original_url}")