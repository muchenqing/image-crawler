import os
import requests
from bs4 import BeautifulSoup
import concurrent.futures
from urllib.parse import urljoin, urlparse
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading

class ImageSpiderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("网页图片爬虫")
        self.root.geometry("700x500")
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 调整窗口大小和布局
        root.update_idletasks()
        root.minsize(600, 500)
        
        # URL输入区域
        url_frame = ttk.LabelFrame(main_frame, text="网址输入", padding="10")
        url_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(url_frame, text="HTTPS:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # 协议选择
        self.protocol_var = tk.StringVar(value="https")
        ttk.Radiobutton(url_frame, text="HTTPS", variable=self.protocol_var, value="https").grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(url_frame, text="HTTP", variable=self.protocol_var, value="http").grid(row=0, column=2, sticky=tk.W, pady=5)
        
        # URL输入框
        ttk.Label(url_frame, text="URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        # 图片尺寸选择
        size_frame = ttk.LabelFrame(main_frame, text="图片尺寸", padding="10")
        size_frame.pack(fill=tk.X, pady=10)
        
        self.size_var = tk.StringVar(value="原图")
        sizes = ["原图", "中等尺寸", "缩略图", "适应"]
        for i, size in enumerate(sizes):
            ttk.Radiobutton(size_frame, text=size, variable=self.size_var, value=size).grid(row=0, column=i, sticky=tk.W, pady=5)
        
        # 自定义尺寸输入
        ttk.Checkbutton(size_frame, text="输入自定义尺寸或链接").grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=5)
        
        # 图片预览区域
        preview_frame = ttk.LabelFrame(main_frame, text="预览", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 下载列表显示（带滚动条）
        scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL)
        self.download_list = tk.Listbox(preview_frame, width=50, height=10, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.download_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20), pady=20)
        self.download_list.pack(side=tk.LEFT, padx=(20, 0), pady=20, fill=tk.BOTH, expand=True)
        self.download_list.insert(tk.END, "已下载的图片:")
        self.download_list.insert(tk.END, "------------------------")
        
        # 状态信息
        self.status_var = tk.StringVar(value="就绪")
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(status_frame, text="状态:").pack(side=tk.LEFT)
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT, padx=10)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="开始爬取", command=self.start_crawl).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="从文件导入", command=self.import_from_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="浏览图片", command=self.browse_images).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="退出", command=root.quit).pack(side=tk.RIGHT, padx=5)
    
    def download_image(self, url, save_dir):
        try:
            response = requests.get(url, stream=True, timeout=10)
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
            
            # Update download list in GUI
            self.root.after(0, lambda: self.download_list.insert(tk.END, filename))
            
            return True
        except Exception as e:
            return False
    
    def crawl_images(self, url):
        try:
            # Extract folder name from URL
            parsed_url = urlparse(url)
            # Get the domain and path to create a unique folder name
            domain = parsed_url.netloc.replace('.', '_')
            path = parsed_url.path.strip('/').replace('/', '_')[:50]
            folder_name = f"{domain}_{path}" if path else domain
            # Remove invalid characters
            folder_name = ''.join(c for c in folder_name if c.isalnum() or c in ('_', '-'))
            
            # Create save directory
            save_dir = os.path.join("downloaded_images", folder_name)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            self.status_var.set("正在获取网页...")
            
            # Fetch webpage with headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            timeout = 15
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract image URLs
            image_urls = []
            
            # Check all links
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href:
                    # Check if link is an image file
                    if href.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg')):
                        if not href.startswith(('http://', 'https://')):
                            href = urljoin(url, href)
                        image_urls.append(href)
            
            # Check img tags
            img_tags = soup.find_all('img')
            self.status_var.set(f"找到 {len(img_tags)} 个图片标签")
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
            
            # Check background images in style attributes
            style_tags = soup.find_all(style=True)
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
            
            # Check for JavaScript embedded images
            script_tags = soup.find_all('script')
            for script in script_tags:
                script_content = script.string
                if script_content:
                    import re
                    # Look for image URLs in JavaScript
                    js_image_matches = re.findall(r'https?://[^"\'\s]+\.(jpg|jpeg|png|gif|webp|bmp|svg)', script_content)
                    for match in js_image_matches:
                        if match:
                            # Extract the full URL
                            full_url = re.search(r'(https?://[^"\'\s]+\.' + match + ')', script_content)
                            if full_url:
                                full_url = full_url.group(1)
                                if full_url not in image_urls:
                                    image_urls.append(full_url)
            
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
            
            # Check for dynamic loaded images via New.php
            self.status_var.set("正在检查动态加载的图片...")
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
                    # Don't break, continue to next page
                    page += 1
                    if page > 10:
                        break
            
            total_images = len(image_urls)
            self.status_var.set(f"找到 {total_images} 个图片URL")
            
            # Download images concurrently
            success_count = 0
            if total_images > 0:
                self.status_var.set(f"正在下载 {total_images} 张图片...")
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    futures = []
                    for img_url in image_urls:
                        future = executor.submit(self.download_image, img_url, save_dir)
                        futures.append(future)
                    
                    for future in concurrent.futures.as_completed(futures):
                        if future.result():
                            success_count += 1
            
            self.status_var.set(f"下载完成！成功 {success_count}/{total_images}")
            messagebox.showinfo("完成", f"成功下载 {success_count} 张图片\n保存到: {os.path.abspath(save_dir)}")
            
        except Exception as e:
            self.status_var.set(f"错误: {str(e)}")
            messagebox.showerror("错误", str(e))
    
    def start_crawl(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("警告", "请输入网址")
            return
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            protocol = self.protocol_var.get()
            url = f"{protocol}://{url}"
        
        # Clear download list
        self.download_list.delete(0, tk.END)
        self.download_list.insert(tk.END, "已下载的图片:")
        self.download_list.insert(tk.END, "------------------------")
        
        # Run crawl in separate thread to avoid GUI freezing
        thread = threading.Thread(target=self.crawl_images, args=(url,))
        thread.daemon = True
        thread.start()
    
    def browse_images(self):
        save_dir = "downloaded_images"
        if os.path.exists(save_dir):
            os.startfile(save_dir)
        else:
            messagebox.showinfo("提示", "还没有下载图片")
    
    def import_from_file(self):
        # 打开文件选择对话框
        file_path = filedialog.askopenfilename(
            title="选择包含图片URL的txt文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if not file_path:
            return
        
        # Clear download list
        self.download_list.delete(0, tk.END)
        self.download_list.insert(tk.END, "已下载的图片:")
        self.download_list.insert(tk.END, "------------------------")
        
        # Run download in separate thread
        thread = threading.Thread(target=self.download_from_file, args=(file_path,))
        thread.daemon = True
        thread.start()
    
    def get_original_url(self, url):
        # 尝试从缩略图URL获取原图URL
        # 常见的缩略图模式
        patterns = [
            # Pixiv thumbnail patterns
            ('/c/(\d+)x(\d+)_img-master/', '/img-original/'),
            ('/_master1200.jpg', '.jpg'),
            ('/_master1200.png', '.png'),
            ('/_master1200.webp', '.webp'),
            # General thumbnail patterns
            ('/thumbnail/', '/'),
            ('/thumb/', '/'),
            ('/small/', '/'),
            ('/medium/', '/'),
            ('_thumb', ''),
            ('_small', ''),
            ('_medium', ''),
        ]
        
        original_url = url
        for pattern, replacement in patterns:
            if pattern in url:
                original_url = url.replace(pattern, replacement)
                break
        
        return original_url
    
    def download_from_file(self, file_path):
        try:
            # Create save directory
            save_dir = "downloaded_images"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            # Read URLs from file
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Extract valid image URLs and try to get original images
            image_urls = []
            original_urls = []
            
            for line in lines:
                line = line.strip()
                if line and line.startswith(('http://', 'https://')):
                    # Check if it's an image URL
                    if line.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg')):
                        image_urls.append(line)
                        # Try to get original URL
                        original_url = self.get_original_url(line)
                        original_urls.append(original_url)
            
            total_images = len(image_urls)
            self.status_var.set(f"找到 {total_images} 个图片URL")
            
            # Download images concurrently, prefer original URLs
            success_count = 0
            if total_images > 0:
                self.status_var.set(f"正在下载 {total_images} 张图片...")
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    futures = []
                    for i, img_url in enumerate(image_urls):
                        # Use original URL if different from thumbnail
                        download_url = original_urls[i] if original_urls[i] != img_url else img_url
                        future = executor.submit(self.download_image_with_fallback, download_url, img_url, save_dir)
                        futures.append(future)
                    
                    for future in concurrent.futures.as_completed(futures):
                        if future.result():
                            success_count += 1
            
            self.status_var.set(f"下载完成！成功 {success_count}/{total_images}")
            messagebox.showinfo("完成", f"成功下载 {success_count} 张图片\n保存到: {os.path.abspath(save_dir)}")
            
        except Exception as e:
            self.status_var.set(f"错误: {str(e)}")
            messagebox.showerror("错误", str(e))
    
    def download_image_with_fallback(self, original_url, fallback_url, save_dir):
        # Try to download original image first, fallback to thumbnail if fails
        try:
            response = requests.get(original_url, stream=True, timeout=10)
            response.raise_for_status()
            
            parsed_url = urlparse(original_url)
            filename = os.path.basename(parsed_url.path)
            
            if not filename:
                filename = f"image_{hash(original_url)}.jpg"
            
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
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            self.root.after(0, lambda: self.download_list.insert(tk.END, f"[原图] {filename}"))
            return True
        except Exception as e:
            # Fallback to thumbnail
            return self.download_image(fallback_url, save_dir)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSpiderGUI(root)
    root.mainloop()