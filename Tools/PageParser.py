import requests
from bs4 import BeautifulSoup
import re


class PageParser(object):
    url = ''
    _pattern_title = '«(.+?)»'
    _pattern_html_tag = '<.+?>'
    _pattern_text_break = '\\n.+?\.|\\n'
    _repl_break = '<center></center>'

    def __init__(self, url, title_pattern='', text_html_pattern='', text_break_pattern = ''):
        if url is None:
            raise Exception()
        self.url = url
        if title_pattern != '':
            self._pattern_title = title_pattern
        if text_html_pattern != '':
            self._pattern_html_tag = text_html_pattern
        if text_break_pattern != '':
            self._pattern_text_break = text_break_pattern

        self._titlePattern = re.compile(self._pattern_title)
        self._pattern_html_tag = re.compile(self._pattern_html_tag)
        self._pattern_text_break = re.compile(self._pattern_text_break)

    def _get_article_title(self, article):
        text = article.get_text()
        text = re.findall(self._pattern_title, text)
        text = text[0]
        return text

    def _get_article_text(self, article):
        text = article.find_all("div", {"class":"entry"})[0]
        text = text.get_text()
        text = text.split('Помощь блогу:')[0]
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

    def _fancify_text(self, text=''):
        # Remove HTML tags. Commented, because facebook supports HTML in posts now
        # text = re.sub(pattern=self.text_pattern, string=text, repl='')
        # Substitute \n[1-xx] with <center></center>
        text = re.sub(self._pattern_text_break, self._repl_break, text)
        return text

    def get_articles(self, multiple_pages = False):
        if multiple_pages:
            pass
        article_list = []

        try:
            links = self._get_links()
        except requests.RequestException as rq_exc:
            print(rq_exc, end='|')
            print("Can't get the list of links")
            raise

        for link in links:
            content_list = []
            try:
                article = requests.get(link)
            except requests.RequestException as article_exc:
                print(article_exc, end='|')
                print("Can't connect to an article page. Continuing.")
                continue

            soup = BeautifulSoup(article.text, "html.parser")
            title = self._get_article_title(soup)
            text = self._fancify_text(self._get_article_text(soup))
            content_list.append(title)
            content_list.append(link)
            content_list.append(text)
            article_list.append(content_list)

        return article_list