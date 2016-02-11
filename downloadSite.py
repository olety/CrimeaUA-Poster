import requests
from bs4 import BeautifulSoup
import re
import sys

class Parser(object):
    url = ''
    title_pattern = '«(.+?)»'
    text_pattern = '.+?'

    def __init__(self, url, title_pattern='', text_pattern=''):
        if url is None:
            raise Exception()
        self.url = url
        if title_pattern != '':
            self.title_pattern = title_pattern
        if text_pattern != '':
            self.text_pattern = text_pattern
        self.titlePattern = re.compile(self.title_pattern)
        self.text_pattern = re.compile(self.text_pattern)

    def _get_article_title(self, article):
        text = article.get_text()
        text = re.findall(self.title_pattern, text)
        text = text[0]
        return text

    def _get_article_text(self, article):
        text = article.find_all("div", {"class":"entry"})
        return text

    def _get_links(self):
        try:
            page = requests.get(url=self.url)
        except requests.RequestException:
            print("Can't get a requested starting url")
            raise requests.RequestException

        soup = BeautifulSoup(page.text, "html.parser")
        links = []
        for title in soup.find_all("h2", {"class": "pagetitle"}):
            link = title.find_all("a", href=True)
            link = link[0]['href']
            links.append(link)
        return links

    def get_articles(self):
        article_list = []

        try:
            links = self._get_links()
        except requests.RequestException:
            print("Can't get the list of links")
            raise

        for link in links:
            content_list = []
            try:
                article = requests.get(link)
            except requests.RequestException:
                print("Can't connect to an article page. Continuing.")
                continue

            soup = BeautifulSoup(article.text, "html.parser")
            title = self._get_article_title(soup)
            text = self._get_article_text(soup)
            content_list.append(title)
            content_list.append(link)
            content_list.append(text)
            article_list.append(content_list)

        return article_list

url = "https://crimeaua1.wordpress.com/"
pageName = "/page/"
pageNum = 1

p = Parser(url)

try:
    articles = p.get_articles()
except requests.RequestException:
    print("Problems, cap!")
    sys.exit(-1)

for i in range(0,len(articles),1):
    print(articles[i])