import random
import time
import requests

"""
requests 网络请求工具
"""
user_agents = ["Mozilla/5.0 (Windows NT 10.0; WOW64)", 'Mozilla/5.0 (Windows NT 6.3; WOW64)',
               'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
               'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
               'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
               'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']


def get_html_text(url):
    request = None
    while True:
        try:
            # 在短時間使用多次requests会Failed to establish a new connection這樣一個錯誤，设置'Connection': 'close'
            headers = {'User-Agent': random.choice(user_agents), 'Connection': 'close'}
            request = requests.get(url, headers=headers, timeout=None)

            if request is not None:
                request.raise_for_status()
                request.encoding = request.apparent_encoding
                # print(r.url)
                if request.status_code == 200:
                    rst = request.text
                    request.close()
                    return rst
                request.close()
            return ""
        except Exception as e:
            request.close()
            print(f'请求发生错误：{e}')
            time.sleep(2)


def get_page_json(url):
    headers = {'cookie': '',
               'User-Agent': random.choice(user_agents)
               , 'Connection': 'close'}
    # url = 'https://www.csdn.net/api/articles?type=more&category=home&shown_offset=0'
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        if r.status_code == 200:
            return r.json()
        return ""
    except ConnectionError as e:
        print(e)
        return ""


def get_page_detail(url):
    headers = {
        'user-agent': random.choice(user_agents), 'Connection': 'close'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        print('Error occurred')
        return None


def download_image(url):
    print('Downloading', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except ConnectionError:
        return None


def save_image(content):
    import os
    file_path = '{0}'.format(os.getcwd() + '\images')
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    from _md5 import md5
    image_path = '{0}/{1}.{2}'.format(os.getcwd() + '\images', md5(content).hexdigest(), 'jpg')
    if not os.path.exists(image_path):
        with open(image_path, 'wb') as f:
            f.write(content)
            f.close()
