import os
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import argparse
from urllib.parse import urljoin, urlparse

def download_image(url, save_dir, timeout=10):
    try:
        response = requests.get(url, stream=True, timeout=timeout)
        response.raise_for_status()
        
        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        if not filename:
            filename = f"image_{hash(url)}.jpg"
        
        # Add extension if missing
        if not os.path.splitext(filename)[1]:
            content_type = response.headers.get('Content-Type', '')
            if 'image/jpeg' in content_type:
                filename += ".jpg"
            elif 'image/png' in content_type:
                filename += ".png"
            elif 'image/gif' in content_type:
                filename += ".gif"
            elif 'image/webp' in content_type:
                filename += ".webp"
            else:
                filename += ".jpg"
        
        save_path = os.path.join(save_dir, filename)
        
        # Download image
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✓ Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"✗ Failed to download {url}: {str(e)}")
        return False

def crawl_images(url, save_dir=None, max_workers=5, timeout=15):
    try:
        # Create save directory
        if not save_dir:
            save_dir = "downloaded_images"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # Fetch webpage with headers
        print(f"Fetching webpage: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Extract image URLs
        image_urls = []
        
        # Check all links
        links = soup.find_all('a')
        print(f"Found {len(links)} links")
        for link in links:
            href = link.get('href')
            if href:
                # Check if link is an image file
                if href.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg')):
                    if not href.startswith(('http://', 'https://')):
                        href = urljoin(url, href)
                    image_urls.append(href)
                    print(f"Found image link: {href}")
        
        # Check img tags
        img_tags = soup.find_all('img')
        print(f"Found {len(img_tags)} image tags")
        for img in img_tags:
            img_url = img.get('src')
            if not img_url:
                continue
            
            # Handle relative URLs
            if not img_url.startswith(('http://', 'https://')):
                img_url = urljoin(url, img_url)
            
            # Avoid duplicates
            if img_url not in image_urls:
                image_urls.append(img_url)
                print(f"Found img tag: {img_url}")
        
        # Check background images in style attributes
        style_tags = soup.find_all(style=True)
        print(f"Found {len(style_tags)} style tags")
        for tag in style_tags:
            style = tag.get('style')
            if 'background-image' in style:
                # Extract URL from background-image property
                import re
                matches = re.findall(r'url\(["\']?(.*?)["\']?\)', style)
                for match in matches:
                    if match:
                        if not match.startswith(('http://', 'https://')):
                            match = urljoin(url, match)
                        # Avoid duplicates
                        if match not in image_urls:
                            image_urls.append(match)
                            print(f"Found background image: {match}")
        
        # Check for JavaScript embedded images
        script_tags = soup.find_all('script')
        print(f"Found {len(script_tags)} script tags")
        for script in script_tags:
            src = script.get('src')
            if src:
                # Try to fetch external scripts and check for image URLs
                try:
                    script_url = urljoin(url, src)
                    print(f"Fetching external script: {script_url}")
                    script_response = requests.get(script_url, headers=headers, timeout=timeout)
                    script_response.raise_for_status()
                    script_content = script_response.text
                    
                    # Look for image URLs in script content
                    import re
                    patterns = [
                        r'https?://[^"\'\s]+\.(jpg|jpeg|png|gif|webp|bmp|svg)',
                        r'["\']([^"\']+\.(jpg|jpeg|png|gif|webp|bmp|svg))["\']'
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, script_content)
                        for match in matches:
                            if isinstance(match, tuple):
                                img_path = match[0]
                            else:
                                img_path = match
                            
                            if img_path:
                                if not img_path.startswith(('http://', 'https://')):
                                    img_url = urljoin(url, img_path)
                                else:
                                    img_url = img_path
                                if img_url not in image_urls:
                                    image_urls.append(img_url)
                                    print(f"Found image in external script: {img_url}")
                except Exception as e:
                    print(f"Error fetching script {src}: {str(e)}")
            else:
                script_content = script.string
                if script_content:
                    # Look for image URLs in inline script
                    import re
                    patterns = [
                        r'https?://[^"\'\s]+\.(jpg|jpeg|png|gif|webp|bmp|svg)',
                        r'["\']([^"\']+\.(jpg|jpeg|png|gif|webp|bmp|svg))["\']'
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, script_content)
                        for match in matches:
                            if isinstance(match, tuple):
                                img_path = match[0]
                            else:
                                img_path = match
                            
                            if img_path:
                                if not img_path.startswith(('http://', 'https://')):
                                    img_url = urljoin(url, img_path)
                                else:
                                    img_url = img_path
                                if img_url not in image_urls:
                                    image_urls.append(img_url)
                                    print(f"Found image in inline script: {img_url}")
        
        # Try common image filenames
        print("Trying common image filenames...")
        common_image_names = [
            '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg',
            '1.png', '2.png', '3.png', '4.png', '5.png',
            'image1.jpg', 'image2.jpg', 'image3.jpg',
            'photo1.jpg', 'photo2.jpg', 'photo3.jpg'
        ]
        
        for img_name in common_image_names:
            img_url = urljoin(url, img_name)
            try:
                # Check if the image exists
                img_response = requests.head(img_url, headers=headers, timeout=5)
                if img_response.status_code == 200:
                    if img_url not in image_urls:
                        image_urls.append(img_url)
                        print(f"Found common image: {img_url}")
            except Exception as e:
                pass
        
        # Check for dynamic loaded images via New.php
        print("Checking for dynamic loaded images via New.php...")
        page = 1
        while True:
            new_php_url = urljoin(url, f'New.php?page={page}')
            try:
                print(f"Fetching New.php?page={page}...")
                new_php_response = requests.get(new_php_url, headers=headers, timeout=timeout)
                new_php_response.raise_for_status()
                
                # Parse the response to find images
                new_php_soup = BeautifulSoup(new_php_response.content, 'lxml')
                
                # First try to find original image links from <a> tags
                a_tags = new_php_soup.find_all('a')
                original_images = []
                
                for a in a_tags:
                    href = a.get('href')
                    if href and 'img-original' in href:
                        # Clean up whitespace
                        href = href.strip()
                        if href not in original_images:
                            original_images.append(href)
                
                # Then find thumbnail images from <img> tags as fallback
                img_tags = new_php_soup.find_all('img')
                thumbnail_images = []
                
                for img in img_tags:
                    src = img.get('src')
                    if src:
                        if not src.startswith(('http://', 'https://')):
                            src = urljoin(url, src)
                        if src not in thumbnail_images:
                            thumbnail_images.append(src)
                
                # Use original images if available, otherwise use thumbnails
                if original_images:
                    print(f"Found {len(original_images)} original images on page {page}")
                    for img_url in original_images:
                        if img_url not in image_urls:
                            image_urls.append(img_url)
                            print(f"Found original image: {img_url}")
                elif img_tags:
                    print(f"Found {len(img_tags)} thumbnail images on page {page}")
                    for img_url in thumbnail_images:
                        if img_url not in image_urls:
                            image_urls.append(img_url)
                            print(f"Found thumbnail image: {img_url}")
                else:
                    print(f"No more images found on page {page}")
                    break
                
                page += 1
                # Limit to 10 pages to avoid infinite loop
                if page > 10:
                    print("Reached page limit (10 pages)")
                    break
                    
            except Exception as e:
                print(f"Error fetching New.php?page={page}: {str(e)}")
                break
        
        # Check meta tags and other possible image sources
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            if meta.get('property') == 'og:image' or meta.get('name') == 'image':
                img_url = meta.get('content')
                if img_url:
                    if not img_url.startswith(('http://', 'https://')):
                        img_url = urljoin(url, img_url)
                    if img_url not in image_urls:
                        image_urls.append(img_url)
                        print(f"Found meta image: {img_url}")
        
        print(f"Total image URLs found: {len(image_urls)}")
        
        # Download images concurrently
        success_count = 0
        if image_urls:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                for img_url in image_urls:
                    print(f"Downloading: {img_url}")
                    future = executor.submit(download_image, img_url, save_dir)
                    futures.append(future)
                
                for future in concurrent.futures.as_completed(futures):
                    if future.result():
                        success_count += 1
        
        print(f"\nCrawl completed!")
        print(f"Downloaded {success_count} out of {len(image_urls)} images")
        print(f"Images saved to: {os.path.abspath(save_dir)}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web page image crawler")
    parser.add_argument("url", help="URL of the webpage to crawl")
    parser.add_argument("--output", "-o", help="Directory to save images")
    parser.add_argument("--workers", "-w", type=int, default=5, help="Number of concurrent workers")
    parser.add_argument("--timeout", "-t", type=int, default=15, help="Request timeout in seconds")
    
    args = parser.parse_args()
    crawl_images(args.url, args.output, args.workers, args.timeout)