import os
import requests
from bs4 import BeautifulSoup

def download(url):
    # Download the webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Create a folder for the website
    folder_name = url.split('//')[1].split('/')[0]
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    # Download all the resources (CSS, JS, images) and replace the URLs in the HTML
    for link in soup.find_all(['link', 'script', 'img']):
        if link.has_attr('href'):
            file_url = link['href']
        elif link.has_attr('src'):
            file_url = link['src']
        else:
            continue

        if file_url.startswith('//'):
            file_url = 'https:' + file_url
        elif not file_url.startswith('http'):
            file_url = url + file_url if not url.endswith('/') else url[:-1] + file_url

        file_name = file_url.split('/')[-1]
        file_path = os.path.join(folder_name, file_name)

        # Download the file and save it locally
        try:
            response = requests.get(file_url, stream=True)
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
        except:
            continue

        # Replace the URL in the HTML with the local path
        if link.has_attr('href'):
            link['href'] = file_name
        elif link.has_attr('src'):
            link['src'] = file_name

    # Save the HTML with the local paths
    with open(os.path.join(folder_name, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    url = input('Enter the URL to clone: ')
    download(url)
