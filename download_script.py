#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

def download_wikimedia_images(url):
    headers = { # User agent, just in case.
        "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    os.makedirs('wikimedia_images', exist_ok=True)
    images = soup.find_all('img')
    
    for img in images:
        # Try multiple ways to get image URL
        img_url = img.get('src') or img.get('data-src')
        
        if img_url:
            if not img_url.startswith(('http:', 'https:')):
                img_url = urllib.parse.urljoin(url, img_url)
            
            try:
                img_response = requests.get(img_url, headers=headers)
                if img_response.status_code == 200:
                    filename = os.path.join('wikimedia_images', img_url.split('/')[-1])
                    with open(filename, 'wb') as f:
                        f.write(img_response.content)
            except Exception as e:
                print(f"Something went terribly wrong while downloading: {img_url}: {e}")


if __name__ == "__main__":
    download_wikimedia_images("https://commons.wikimedia.org/wiki/Sovereign-state_flags")
    exit(0)
