import requests
import lxml
from bs4 import BeautifulSoup


class ParserInvesting:
    def __init__(self):
        self.url_news = 'https://www.rbc.ru/crypto/tags/?tag=%D0%9A%D1%80%D0%B8%D0%BF%D1%82%D0%BE%D0%B2%D0%B0%D0%BB%D1%8E%D1%82%D0%B0'
        self.url_value = "https://www.cbr.ru/currency_base/daily/"
        self.url_crypt = "https://mainfin.ru/crypto/rates"
        self.url_news_headers = {'user-agent': 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 '
                                               'Safari/537.36', 'accept': '*/*'}
        self.url_value_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                                'like Gecko) Chrome/94.0.4606.81 Safari/537.36', 'accept': '*/*'}
        self.url_crypt_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                                'like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

    @staticmethod
    def get_html(url, headers, paramse=None):
        r = requests.get(url=url, headers=headers, params=paramse)
        return r.text

    def get_news(self):
        soup_news = BeautifulSoup(self.get_html(self.url_news, self.url_news_headers), 'lxml')
        news_list = soup_news.find_all(name='div', class_='item item_image-mob js-tag-item')
        news = []
        for item in news_list:
            news.append(
                {'text': item.find(name='a', class_='item__link').get('href'),
                 'link': item.find(name='a', class_='item__link').get_text(strip=True),
                 'time': item.find(name='span', class_='item__category').get_text(strip=True)},
            )

        return news

    def get_value(self):
        soup_value = BeautifulSoup(self.get_html(self.url_value, self.url_value_headers).encode('utf-8').strip(),
                                   'lxml')
        value_info = soup_value.find(name='h2', class_='h3').text.strip()
        value_table = soup_value.find(name='table', class_='data')
        table = []
        for i in value_table.find_all('td'):
            title = i.text.strip()
            table.append(title)
        return value_info, table

    def get_crypt(self):
        soup_crypt = BeautifulSoup(self.get_html(self.url_crypt, self.url_crypt_headers), 'lxml')
        crypt_table = soup_crypt.find_all(name='tr', class_ = 'row body odd')
        crypto = []
        soup = BeautifulSoup(self.get_html(self.url_crypt, self.url_crypt_headers), 'lxml')
        tes = soup.find(name='tr', class_ = 'row body odd')
        te = tes.find(name='tr', class_ = ' ')
        for item in crypt_table:
            crypto.append(
                {'name': item.find(name='div', class_='s-bold').get_text(strip=True),
                 'link': item.find(name='a').get('href'),
                 'value': item.find_all(name='td', class_= ' ',text= True)
                 }
            )
        return tes


