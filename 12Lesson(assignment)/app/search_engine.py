import requests
import os
from bs4 import BeautifulSoup


class SearchWiki:

    filepath = os.getcwd()

    headers = {
        'content-type': 'text',
        'Connection': 'keep-alive',
        'Search-Version': 'v3',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.129 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    def wiki_search(self, wiki_request):
        self.wiki_request = wiki_request
        print("Hello")
        self.res = requests.get(f"https://en.wikipedia.org/wiki/Special:Search?search={self.wiki_request}&go=Go"
                                   f"&ns0=1", headers=self.headers, allow_redirects=True).text
        with open(self.filepath+f"/app/testhtml/{self.wiki_request}.html", "w+", encoding='utf-8') as file:
            file.write(self.res)

        intro = self.pattern_method(self.res)
        return intro

    def pattern_method(self, res):
        try:
            test1 = BeautifulSoup(res, 'html.parser').find('div', attrs={'id': 'bodyContent'})

        # Этот блок for in : мне не нравится очень сильно, но я не знаю как его красивее сделать.
        # Разве что засунуть это все в список-словарь  и брать оттуда запросы. Но по сути - это те же яйца, только в
        # профиль.
        # Тут происходит постепенная обрезка html страницы до приемлимого (+-) нам формата.
        # "Обрезание" должно быть последовательным... (Выслушаю с удовольствие критики и руководство, как сделать
        # "красивше")
            for excl_content in test1.find_all('table', attrs={'id': 'disambigbox'}):
                excl_content.extract()
            for excl_content in test1.find_all('div', attrs={'class': 'printfooter'}):
                excl_content.extract()
            for excl_content in test1.find_all('div', attrs={'class': 'mw-normal-catlinks'}):
                excl_content.extract()
            for excl_content in test1.find_all('div', attrs={'class', 'catlinks'}):
                excl_content.extract()
            for excl_content in test1.find_all('noscript'):
                excl_content.extract()
            for excl_content in test1.find_all('a', attrs={'class': 'mw-jump-link'}):
                excl_content.extract()

            del_empty_lines = [line for line in test1.get_text().splitlines() if line != '']

            print(del_empty_lines)

            with open(self.filepath + f"/app/testhtml/{self.wiki_request}-test.html", "w", encoding='utf-8') as file:
                file.write(str(test1))

            sum_line = ""
            with open(self.filepath + f"/app/testhtml/{self.wiki_request}-test-text.html", "w", encoding='utf-8') as \
                    file:
                for line in del_empty_lines:
                    sum_line += line+'\n'
                    file.write(str(line + '\n'))
            return sum_line
        except Exception as e:
            print(e)
            return "\nNothing found, specify the request"
