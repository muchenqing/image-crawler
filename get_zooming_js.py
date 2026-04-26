import requests

url = "https://skri.cnmiw.com/img/Pixivusers/zooming.PC.js"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
response.raise_for_status()

with open('zooming.PC.js', 'w', encoding='utf-8') as f:
    f.write(response.text)

print("File saved to zooming.PC.js")
print("First 500 characters:")
print(response.text[:500])