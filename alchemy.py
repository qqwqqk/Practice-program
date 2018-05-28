from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import os
import requests

def download(url, filename):
    if os.path.exists(filename):
        print('file exists!')
        return
    try:
        r = requests.get(url, stream=True, timeout=60)
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  
                    f.write(chunk)
                    f.flush()
        return filename
    except KeyboardInterrupt:
        if os.path.exists(filename):
            os.remove(filename)
        raise KeyboardInterrupt
    except Exception:
        traceback.print_exc()
        if os.path.exists(filename):
            os.remove(filename)
            
if __name__=="__main__":
    # wiki首页链接
    root_url="https://tagatame.huijiwiki.com/wiki/%E9%A6%96%E9%A1%B5"

    # 下载文件夹名称
    if os.path.exists('alchemy') is False:
        os.makedirs('alchemy')

    # 查找属性角色链接
    gradings = set()
    cache = {}
    try:
        response = requests.get(root_url)
        html_cont = response.text
        soup = BeautifulSoup(html_cont, 'html.parser')
        links = soup.find_all('a', title = re.compile(r"属性角色"))
        for link in links:
            new_url = link['href']
            new_full_url = urljoin(root_url, new_url)
            cache['title'] = link['title']
            cache['url'] = new_full_url
            # print(cache['title'], cache['url'])
            gradings.add(new_full_url)
    except:
        print('角色属性分类查找失败')

    # 查找各角色链接
    gradings2 = set()
    count = 0
    while len(gradings) != 0:
        try:
            temp_url = gradings.pop()
            response = requests.get(temp_url)
            html_cont = response.text
            soup = BeautifulSoup(html_cont, 'html.parser')
            links = soup.find('div', class_ = "mw-content-ltr").find_all('a', href = re.compile(r"/wiki/"))
            for link in links:
                new_url = link['href']
                new_full_url = urljoin(root_url, new_url)
                if new_full_url not in gradings2:
                    count = count + 1
                    cache['title'] = link['title']
                    cache['url'] = new_full_url
                    # print(count, cache['title'], new_full_url)
                    gradings2.add(new_full_url)
        except:
            print('抓取失败~')

    # 下载各角色人物图片
    count = 0
    while len(gradings2) != 0:
        try:
            temp_url = gradings2.pop()
            response = requests.get(temp_url)
            html_cont = response.text
            soup = BeautifulSoup(html_cont, 'html.parser')
            links = soup.find('div', class_ = "flex-list unit-gallery").find_all('a', class_ = re.compile(r"image"))
            for link in links:
                new_url = link['href']
                new_full_url = urljoin(root_url, new_url)

                response = requests.get(new_full_url)
                html_cont = response.text
                soup = BeautifulSoup(html_cont, 'html.parser')
                img = soup.find('div', class_="fullImageLink").find('img')
    
                if 'UnitIllustration' in img['alt'] or 'Skin' in img['alt']:
                    count = count + 1
                    target_url = img['src']
                    filename = os.path.join('alchemy', target_url.split('/')[-1])
                    download(target_url, filename)
                    print (count, img['alt'])
        except:
            print('图片下载失败~')
            










            
