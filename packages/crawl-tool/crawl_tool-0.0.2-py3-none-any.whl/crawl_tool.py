# -*- coding: utf-8 -*-
import requests
from lxml import etree
import re

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}

class crawlerTool:

    def __init__(self):
        self.session = requests.session()
        self.proxy_now = ''
        pass

    def __del__(self):
        self.session.close()

    @staticmethod
    def get(url, proxies=None, cookies={}, referer='',headers={}):
        if not headers:
            if referer:
                headers = {'Referer': referer}
                headers.update(HEADERS)
            else:
                headers = HEADERS
        if proxies:
            rsp = requests.get(url, timeout=10, headers=headers, cookies=cookies,proxies=proxies)
        else:
            rsp = requests.get(url, timeout=30, headers=headers, cookies=cookies)
        return rsp.content  # 二进制返回

    @staticmethod
    def post(url,data,headers={}): # 必须传入字典，中文不用编码！
        if headers:
            rsp = requests.post(url, data, timeout=10,headers=headers)
        else:
            rsp = requests.post(url,data,timeout=10)
        return rsp.content


    def sget(self,url,cookies={},headers = {}):
        headers = headers.update(HEADERS)
        if cookies:
            rsp = self.session.get(url,timeout=10,headers=headers,cookies=cookies)
        else:
            rsp = self.session.get(url, timeout=10, headers=headers)
        return rsp.content # 二进制返回

    def spost(self,url,data,allow_redirects=True,headers = {}):
        headers = headers.update(HEADERS)

        rsp = self.session.post(url,data,timeout=10,headers=headers,allow_redirects=allow_redirects)
        return rsp.content



    # 获取xpath 要判断一下输入类型，或者异常处理
    @staticmethod
    def getXpath(xpath, content):   #xptah操作貌似会把中文变成转码&#xxxx;  /text()变unicode编码
        hparser = etree.HTMLParser(encoding='utf-8')

        tree = etree.HTML(content,hparser)
        out = []
        results = tree.xpath(xpath)
        for result in results:
            if  'ElementStringResult' in str(type(result)) or 'ElementUnicodeResult' in str(type(result)) :
                out.append(result)
            else:
                out.append(etree.tostring(result))
        return out

    # 获取xpath 要判断一下输入类型，或者异常处理
    @staticmethod
    def getXpath1(xpath, content):   #python3的xpath传入的应该是字符串！！
        hparser = etree.HTMLParser(encoding='utf-8')
        tree = etree.HTML(content,hparser)
        out = []
        results = tree.xpath(xpath)
        for result in results:
            if  'ElementStringResult' in str(type(result)) or 'ElementUnicodeResult' in str(type(result)) :
                out.append(result)
            else:
                out.append(etree.tostring(result))
        if out:
            return out[0]
        return ''

    @staticmethod
    def getRegex(regex, content):
        if type(content) == type(b''):
            content = content.decode('utf8')
        rs = re.search(regex,content)
        if rs:
            return rs.group(1)
        else:
            return ''

    @staticmethod
    def parser_urlpars(pars):
        # pars= 'q=GENER8%20MARITIME%2C%20INC.&quotesCount=6&newsCount=4&enableFuzzyQuery=false&quotesQueryId=tss_match_phrase_query&multiQuoteQueryId=multi_quote_single_token_query&newsQueryId=news_cie_vespa&enableCb=true&enableNavLinks=true&vespaNewsTimeoutMs=600'
        from urllib.parse import quote, unquote
        pars = pars.replace('+', ' ')
        field_pars = pars.split('&')
        par_dict = {}
        for field_par in field_pars:
            field = field_par.split('=')
            if len(field) == 1:
                par_dict[unquote(field[0])] = None
            else:
                par_dict[unquote(field[0])] = unquote(field[1])
        return par_dict

    @staticmethod
    def parser_cookie(cookie_str):
        # cookie_str = '_vcooline_ikcrm_production_ikcrm.com_session_=bHpKZVZSUzNoZ3MraFVBK1BrV1MvbjF1Mzdtdk9lZ0pxWm0zY1hUVDRnVXhBWTNmek9pQ2xNelJFRE1obVRoaVg4RkJldU5JR0xrKzNUSE5RUWxTWU5DSlVRVjBtTkhrMmJWMzRDTjJ3MXNhQjVwSjlsZkRsRjJYR0FUbERhdWtNdEhrM1V5emdBd1VzN0FIR0ppOTNYZjNGSHJ0cjVCcmJBVXhPdVFCdWkyeTF6b0RiRFA3ZVV0VWRNelQ5NHIweWsxSkxRSkRWbTUxaHBKaGFnc1NlSEl1MjZnQUFBdDhXUm8xV3pYWmcwVTVCbnpkT0tpNlNOZlVUdEUzUUo4YlhVelBBMkhyL3QzR0hHenpiM0hnVzZickMzTDBvMTBvNkFhenNJOWZxTGMyQk9VUnl3aVV2ellzZ05HeGZ2L1EtLUhwOWNLZEwxWm5xN0M5TjhxL2JpQVE9PQ%3D%3D--7085cd9bc2c7ff4f2e1f60bf29a838f21ef41ede; domain=.ikcrm.com; path=/'
        cookie_dict = {}
        for cookie in cookie_str.split(';'):
            l = cookie.split('=')
            key, value = l[0],'='.join(l[1:])
            cookie_dict[key] = value
        return cookie_dict

    @staticmethod
    def get_text(page_source):
        if type(page_source) == type(b''):
            page_source = page_source.decode('utf8')
        return re.sub('(<.*?>)',"",page_source)

    @staticmethod
    def quote(input):
        from urllib import parse
        return parse.quote(input)

    @staticmethod
    def unquote(input):
        from urllib import parse
        return parse.unquote(input)

    @staticmethod
    def quote(input):
        from urllib import parse
        return parse.quote(input)

    def get_by_proxy(self,url,success_symbol = '',failed_symbol_symbol='',cookies={}, referer=''):
        '''

        :param success_symbol:  访问成功的标志
        :param failed_symbol_symbol:  访问失败的标志
        :return:
        '''
        page_buf = ''
        for retry_times in range(2):
            if not self.proxy_now:
                self.proxy_now = self.get_new_5min_proxy()
            page_buf = self.get(url,referer=referer,cookies=cookies,proxies = {'http':'http://'+self.proxy_now ,'https':'http://'+self.proxy_now }).decode('utf8')
            if success_symbol and success_symbol in page_buf:
                return page_buf
            if failed_symbol_symbol in page_buf:
                continue
            return page_buf

    def get_regular_file_name(self,file_name):
        file_name = file_name.replace('\t','').replace('\n','')
        file_name = re.sub(u"([/\\\\:*?<>|])", "", file_name)
        return file_name


    @staticmethod
    def writer_to_csv(datas,file_path):
        import csv
        with open(file_path,'w',encoding='utf_8_sig',newline='',) as fout:
            writer = csv.writer(fout)
            for data in datas:
                writer.writerow(data)
                fout.flush()








if __name__ == '__main__':
    page = crawlerTool.get('https://es.thefreedictionary.com/Jyv%C3%A4skyl%C3%A4')
    with open('1.html','w',encoding='utf8') as f:
        f.write(page.decode('utf8'))

