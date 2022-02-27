__author__ = 'Hiroyuki Kakara'

import bs4
import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
import shutil
import subprocess
import sys
import time

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
headers = {'User-Agent':user_agent}

def get_web_content(url):
    try:
        res = requests.get(url, headers=headers, timeout=7, verify=False)
        time.sleep(5)
        if 'content-type' in res.headers:
            if res.status_code == 200 and 'text/html' in res.headers['content-type']:
                web_soup = bs4.BeautifulSoup(res.text, 'html.parser')
                return web_soup
            else:
                return False
        else:
            return False
    except Exception as e:
        return False

def judge_opendir(web_soup):
    if web_soup.title != None:
        if "Index of " in web_soup.title.string:
            return True
        else:
            return False
    else:
        return False

def get_opendir_parent(url):
    url_previous = url
    url_elem = url.split('/')
    base_url = f"{url_elem[0]}//{url_elem[2]}"
    for i in range(len(url_elem)-1, 2, -1):
        path = ''
        for j in range(3,i,1):
            path = f"{path}/{url_elem[j]}"
        web_soup = get_web_content(base_url + path)
        if web_soup != False:
            if judge_opendir(web_soup):
                url_previous = base_url + path
            else:
                return url_previous
        else:
           return url_previous
    return url_previous

def get_child_links(web_soup):
    links_tmp = [url.get('href') for url in web_soup.find_all('a')]
    links = []
    for link in links_tmp:
        if not re.search("^\?C=[A-Z];O=[A-Z]$", link) and not link=='/' and not link=='../':
            links.append(link.replace('/',''))
    return links

def write_content(output_path, content):
    with open(output_path,'wb') as f:
        f.write(content)

def get_screenshot(url, output):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'--user-agent={user_agent}')
        chrome_service = service.Service(executable_path
         ='!!解凍したWebドライバのフルパスを入力!!')
        driver = webdriver.Chrome(service=chrome_service, options=options)
        driver.set_page_load_timeout(10)
        driver.get(url)
        width = driver.execute_script('return document.body.scrollWidth')
        height = driver.execute_script('return document.body.scrollHeight')
        driver.set_window_size(int(width),int(height))
        driver.save_screenshot(output)
        driver.quit()
        time.sleep(5)
        return 1
    except Exception as e:
        print(e)
        return -1

class GOD:
    def get_opendir(self, url, output):
        content_count = 0
        if not url.startswith('http://') and not url.startswith('https://'):
            print('Only http:// or https:// are acceptable.')
            exit()
        web_soup = get_web_content(url)
        if web_soup != False:
            if judge_opendir(web_soup):
                opendir_parent = get_opendir_parent(url)
                base_path = url.split('/')[2].replace(':', '_')
                image_dir = os.path.join(output, f"{base_path}_image")
                os.makedirs(image_dir, exist_ok=True)
                opendir_urls = [opendir_parent]
                imagepath_list = list()
                for opendir_url in opendir_urls:
                    print(f"Processing {opendir_url}...")
                    web_soup = get_web_content(opendir_url)
                    opendir_name = opendir_url.replace('http://','').replace('https://','').replace(':', '_')
                    outputdir = os.path.join(output, opendir_name)
                    os.makedirs(outputdir, exist_ok=True)
                    links = get_child_links(web_soup)
                    for link in links:
                        if content_count > 10:
                            break
                        res = requests.get(f"{opendir_url}/{link}", headers=headers)
                        time.sleep(5)
                        link_filename = os.path.join(outputdir, link.replace('/',''))
                        if res.status_code == 200:
                            if 'content-type' in res.headers:
                                if 'text/html' in res.headers['content-type']:
                                    web_soup = get_web_content(f"{opendir_url}/{link}")
                                    if web_soup != False:
                                        if judge_opendir(web_soup):
                                            opendir_urls.append(opendir_url + "/" + link ) # ❼
                                        else:
                                            write_content(link_filename, res.content)
                                else:
                                    write_content(link_filename, res.content)
                            else:
                                write_content(link_filename, res.content)
                        content_count += 1
                    imagepath = os.path.join(image_dir, opendir_url.replace('/','_').replace(':','').replace('.','_') +'.png')
                    if get_screenshot(opendir_url, imagepath) > 0:
                        print('Successfully got screenshot: ' + imagepath )
                        imagepath_list.append(imagepath)
                    else:
                        print(f"Couldn't get screenshpt: {imagepath}")
                if os.name == 'posix' and os.path.exists('/usr/bin/zip'):
                    subprocess.call(['zip', '-r', '-e', '--password=novirus', f'{base_path}.zip', base_path], cwd=output)
                elif os.name == 'nt' and os.path.exists('C:\\Windows\\System32\\wsl.exe') and subprocess.call(['wsl', 'which', 'zip'], stdout=subprocess.DEVNULL) == 0:
                    subprocess.call(['wsl', 'zip', '-r', '-e', '--password=novirus', f'{base_path}.zip', base_path], cwd=output)
                else:
                    shutil.make_archive(os.path.join(output, base_path), 'zip', root_dir=os.path.join(output, base_path)) # without password
                shutil.rmtree(os.path.join(output, base_path))
                output_zip = os.path.join(output, f"{base_path}.zip")
                print(f"Saved to {output_zip}" )
                imagepath = os.path.join(output, f"{opendir_parent.replace('/','_').replace(':','').replace('.','_')}.png")
                return [output_zip, imagepath_list]
            else:
                return ['This is not an OpenDir.']
        else:
            return ["Couldn't get html content from this URL."]

if __name__ == '__main__':
    god = GOD()
    res = god.get_opendir(sys.argv[1], '<Your ourput directory>')
    print(res)