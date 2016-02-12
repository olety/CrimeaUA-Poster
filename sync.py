import sys

import requests

from Tools.PageParser import PageParser

url = "https://crimeaua1.wordpress.com/"
page_name = "/page/"
page_num = 1

p = PageParser(url)

try:
    articles = p.get_articles()
except requests.RequestException as e:
    print(e, end='|')
    print("Problems, cap!")
    sys.exit(-1)

for i in range(0, len(articles), 1):
    print(articles[i])

