import requests

url = "https://skri.cnmiw.com/js/img/main.js"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
response.raise_for_status()

with open('main.js', 'w', encoding='utf-8') as f:
    f.write(response.text)

print("File saved to main.js")
print("First 500 characters:")
print(response.text[:500])