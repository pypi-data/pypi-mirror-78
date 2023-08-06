import re
from time import time
from lxml import etree
from urllib.parse import unquote


class Spider:
    default_header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    # default_proxy = {"http": "socks5://127.0.0.1:22230", "https": "socks5://127.0.0.1:22230"}

    # def __init__(self, url, headers=None):
    #     self.url = url
    #     if type(headers) == str:
    #         self.headers = Spider._get_header(headers)
    #     elif type(headers) == dict:
    #         self.headers = headers.copy()
    #     elif not headers:
    #         self.headers = Spider.default_header.copy()
    #     else:
    #         raise ValueError('Unexpected type -> %s' % type(headers))
    #     if not self.headers.get('User-Agent'): self.headers.update(Spider.default_header)

    @staticmethod
    def get_time_now(n=13):
        return str(time()).replace('.', '')[:n]

    @staticmethod
    def del_dict_attr(dic, pattern_del: []):
        for x in pattern_del.split():
            del (dic[x])
            print('del->', x)

    @staticmethod
    def request_headers_string_to_dict(str_headers: str) -> dict:
        return dict(
            [[k_or_v.strip() for k_or_v in line.split(':', maxsplit=1)] for line in str_headers.strip().splitlines()])

    @staticmethod
    def search_query_join(url: str, data_d: dict) -> str:
        if not url.endswith('?'):
            url += '?'
        return url + '&'.join('{}={}'.format(k, v) for k, v in data_d.items())

    @staticmethod
    def search_query_split(url: str) -> dict:
        sq = re.sub('(^.*\?)|(#.*$)', '', url)
        return dict([[unquote(x) for x in k_v.split('=')] for k_v in sq.split('&')])

    @staticmethod
    def cookie_dict_to_str(dict_cookie: dict) -> str:
        return ';'.join(['='.join(k_v) for k_v in dict_cookie.items()])

    @staticmethod
    def cookie_string_to_dict(str_cookie: str) -> dict:
        return dict([x.strip().split('=', maxsplit=1) for x in str_cookie.split(';')])

    @staticmethod
    def get_chinese_char(s: str) -> list:
        return re.findall('[\u4e00-\u9fa5]+', s)

    @staticmethod
    def response_to_xpath(res):
        return etree.HTML(res.text)
