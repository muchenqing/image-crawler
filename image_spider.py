import os
import requests
from bs4 import BeautifulSoup

def download_image(url, save_dir):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        # Extract filename from URL
        filename = os.path.basename(url)
        if not filename:
            filename = f"image_{hash(url)}.jpg"
        
        # Add extension if missing
        if not os.path.splitext(filename)[1]:
            filename += ".jpg"
        
        save_path = os.path.join(save_dir, filename)
        
        # Download image
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Failed to download {url}: {str(e)}")
        return False

def crawl_images(url):
    try:
        # Create save directory
        save_dir = "downloaded_images"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # Fetch webpage
        print(f"Fetching webpage: {url}")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Find all image tags
        img_tags = soup.find_all('img')
        print(f"Found {len(img_tags)} image tags")
        
        # Extract and download images
        success_count = 0
        for img in img_tags:
            img_url = img.get('src')
            if not img_url:
                continue
            
            # Handle relative URLs
            if not img_url.startswith(('http://', 'https://')):
                from urllib.parse import urljoin
                img_url = urljoin(url, img_url)
            
            if download_image(img_url, save_dir):
                success_count += 1
        
        print(f"\nCrawl completed!")
        print(f"Downloaded {success_count} out of {len(img_tags)} images")
        print(f"Images saved to: {os.path.abspath(save_dir)}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    url = input("Enter the URL to crawl: ")
    crawl_images(url)