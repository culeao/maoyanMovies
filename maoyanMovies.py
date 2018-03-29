#!/usr/bin/evn python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       maoyanMovie
   Description:     
   Author:          litong
   date:            2018/3/29
-------------------------------------------------
   Change Activity: 2018/3/29:
-------------------------------------------------
"""
from time import sleep

__author__ = 'litong'

import requests
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
}


def getOnePage(url, headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except requests.RequestException:
        return None


def parse_one_page(html, page):
    pattern = re.compile('"name"><a.+?films/\d+?" title="(.+?)".+?主演：(.+?)\n.*?上映时间：(.+?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>',re.S)
    results = re.findall(pattern, html)
    for i, item in enumerate(results):
        yield {
            'index': 10 * page + i,
            'title': item[0],
            'actors': item[1],
            'data': item[2],
            'score': item[3] + item[4]
        }


def write_to_json(content):
    with open('movie.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    for offset in range(10):
        url = 'http://maoyan.com/board/4?' + 'offset={}'.format(offset * 10)
        page = getOnePage(url, headers)
        print(url)
        for i in parse_one_page(page, offset):
            write_to_json(i)
        sleep(1)
