import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://skri.cnmiw.com/img/Pixivusers/45015081/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Fetch New.php to analyze image URLs
page = 1
new_php_url = urljoin(url, f'New.php?page={page}')
response = requests.get(new_php_url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.content, 'lxml')
img_tags = soup.find_all('img')

print("Current image URLs:")
for img in img_tags:
    img_url = img.get('src')
    if img_url:
        print(f"  {img_url}")

print("\nAnalyzing URL patterns...")
# Analyze URL patterns for possible original image URLs
for img in img_tags:
    img_url = img.get('src')
    if img_url and 'master1200' in img_url:
        # Try to find original image URL pattern
        original_url = img_url.replace('master1200', 'original')
        print(f"  Original URL candidate: {original_url}")
        
        # Test if the original URL exists
        try:
            test_response = requests.head(original_url, headers=headers, timeout=5)
            if test_response.status_code == 200:
                print(f"  ✓ Original URL exists: {original_url}")
            else:
                print(f"  ✗ Original URL not found: {original_url}")
        except Exception as e:
            print(f"  ✗ Error checking original URL: {e}")