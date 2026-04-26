import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://skri.cnmiw.com/img/Pixivusers/45015081/"

# Fetch webpage with headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)
response.raise_for_status()

# Save the HTML content to a file
with open('debug.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

# Parse HTML
soup = BeautifulSoup(response.content, 'lxml')

# Debug information
print("=== Debug Information ===")
print(f"Status code: {response.status_code}")
print(f"Content length: {len(response.content)} bytes")
print()

# Check all links
print("=== Links ===")
links = soup.find_all('a')
print(f"Found {len(links)} links:")
for i, link in enumerate(links):
    href = link.get('href')
    text = link.get_text(strip=True)
    print(f"  {i+1}. {href} - '{text}'")
print()

# Check img tags
print("=== Image Tags ===")
img_tags = soup.find_all('img')
print(f"Found {len(img_tags)} img tags:")
for i, img in enumerate(img_tags):
    src = img.get('src')
    alt = img.get('alt', '')
    print(f"  {i+1}. {src} - '{alt}'")
print()

# Check style tags
print("=== Style Tags ===")
style_tags = soup.find_all(style=True)
print(f"Found {len(style_tags)} elements with style attribute:")
for i, tag in enumerate(style_tags):
    style = tag.get('style')
    tag_name = tag.name
    print(f"  {i+1}. <{tag_name}> - style: {style[:100]}...")
print()

# Check script tags
print("=== Script Tags ===")
script_tags = soup.find_all('script')
print(f"Found {len(script_tags)} script tags:")
for i, script in enumerate(script_tags):
    src = script.get('src')
    if src:
        print(f"  {i+1}. External script: {src}")
    else:
        content = script.string
        if content:
            # Look for any image-related content
            if any(ext in content.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                print(f"  {i+1}. Internal script with image content (length: {len(content)} chars)")
                # Print first 200 chars of content
                print(f"     {content[:200]}...")
            else:
                print(f"  {i+1}. Internal script (length: {len(content)} chars)")
        else:
            print(f"  {i+1}. Empty script tag")
print()

print("Debug information saved to debug.html")