# -*- coding:UTF-8 -*-
import requests
import demjson


class ImageType:
    def __init__(self, url, pid, cookie):
        self.url = url
        self.pid = pid
        self.cookie = cookie

    def verifyType(self):
        print(__file__)
        proxy_addr = None
        pages_headers = {
            'Connection': 'close',
            "referer": self.url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
        }
        pages = 'https://www.pixiv.net/ajax/illust/' + self.pid + '/pages'
        if proxy_addr is not None:
            pages_meta_body = requests.get(pages, proxies=proxy_addr, headers=pages_headers,
                                           cookies={'PHPSESSID': self.cookie})
        else:
            pages_meta_body = requests.get(pages,headers=pages_headers,
                                           cookies={'PHPSESSID': self.cookie})

        pages_meta_src = demjson.decode(pages_meta_body.text)['body']
        return pages_meta_src


