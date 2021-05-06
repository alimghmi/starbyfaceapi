import requests
import re
import os
import random
import time
import json
import requests
import re
from bs4 import BeautifulSoup


def scraper(photo):
    url = "https://starbyface.com/"
    
    headers = {
        'Host':'starbyface.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'DNT': '1',
        'Origin': 'https://starbyface.com',
        'Referer': 'https://starbyface.com/',
        'Connection': 'close'
    }

    req = requests.Session()
    _res_ = {
        'name': None,
        'similarity': None,
        'pic': None,
        'download': None

    }

    data = {'name': 'imageUploadForm'}
    files = {'imageUploadForm': open(photo, "rb")}
    req.get(url, headers=headers)

    cookies = {
        '.ASPXANONYMOUS': req.cookies.get('.ASPXANONYMOUS')
    }

    x = req.post(url=url + '/Home/LooksLikeByPhoto', data=data, \
        headers=headers, cookies=cookies, files=files)
    cookies['ASP.NET_SessionId'] = req.cookies.get('ASP.NET_SessionId')

    soup = BeautifulSoup(x.text, features="html.parser")
    case = soup.find_all('div', class_ = \
        'col-lg-3 col-offset-3 candidate realCandidate text-left')[0]

    _res_['name'] = case['name']
    
    _res_['similarity'] = case.find('div', \
        class_ = 'progress progress-striped').text.strip()
    
    _res_['pic'] = case.find('img', class_ = 'img-thumbnail')['src']
    
    result = url + case.find('button', \
        class_ = 'btn btn-default')['gridhref'] + '&type=0'
    
    soup_ = BeautifulSoup(req.get(result, headers=headers).text \
            , features="html.parser")
    
    _res_['download'] = url + soup_.find('img',  \
        class_ = 'img-thumbnail')['src']

    return _res_
