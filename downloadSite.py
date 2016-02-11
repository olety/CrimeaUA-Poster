import requests
from bs4 import BeautifulSoup
import re
class Parser (object):
    url = ''

    def __init__(self, url = ''):
        self.url = url

    def getTitleText(self, title = None):
        pattern = '«(.+?)»'
        pattern = re.compile(pattern)
        text = title.get_text()
        text = re.findall(pattern, text)
        text = ''.join(text)
        return text

    def getLinkText(self, title = None):
        pattern = 'href="(.+?)"'
        pattern = re.compile(pattern)
        link = title.find_all("a", href=True)
        link = link[0]['href']
        return link


    def getTitles(self):
        page = requests.get(url = self.url)
        soup = BeautifulSoup(page.text, "html.parser")
        titles = []
        for title in soup.find_all("h2", {"class" : "pagetitle"}):
            content = []
            content.append(self.getTitleText(title))
            content.append(self.getLinkText(title))
            titles.append(content)
        return titles

    def getArticles(self):
        for title in self.getTitles():
            head = title[0]
            link = title[1]
            article = requests.get(link)
            soup = BeautifulSoup(article.text, "html.parser")
            print(soup)


url = "https://crimeaua1.wordpress.com/"
pageName = "/page/"
pageNum = 1
file = requests.get(url=url)
p = Parser(url)
articles = p.getArticles()

#for content in titles:
#    print(content[0] + " " + content[1])

"""while (file != '<Response [404]>'):
    text = file.text
    soup = BeautifulSoup(text, "html.parser")

    pageNum += 1
    file = requests.get(url=url+pageName+str(pageNum))
    """