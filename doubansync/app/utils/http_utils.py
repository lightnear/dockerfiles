import requests
import urllib3

class RequestUtils:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    __headers = None
    __cookies = None
    __proxies = None
    __timeout = 20
    __session = None

    def __init__(self, headers=None, cookies=None, proxies=False, session=None, timeout=None):
        if headers:
            self.__headers = headers
        else:
            self.__headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
        if cookies:
            if isinstance(cookies, str):
                self.__cookies = self.cookie_parse(cookies)
            else:
                self.__cookies = cookies
        if proxies:
            self.__proxies = proxies
        if session:
            self.__session = session
        if timeout:
            self.__timeout = timeout

    def get(self, url, params=None, allow_redirects=True):
        try:
            if self.__session:
                return self.__session.get(url, params=params, verify=False, headers=self.__headers,
                                          proxies=self.__proxies, cookies=self.__cookies, timeout=self.__timeout,
                                          allow_redirects=allow_redirects)
            else:
                return requests.get(url, params=params, verify=False, headers=self.__headers, proxies=self.__proxies,
                                    cookies=self.__cookies, timeout=self.__timeout, allow_redirects=allow_redirects)
        except requests.exceptions.RequestException:
            return None

    def post(self, url, params=None, data=None, allow_redirects=True):
        try:
            if self.__session:
                return self.__session.post(url, params=params, data=data, verify=False, headers=self.__headers,
                                           proxies=self.__proxies, cookies=self.__cookies,
                                           allow_redirects=allow_redirects)
            else:
                return requests.post(url, params=params, data=data, verify=False, headers=self.__headers,
                                     proxies=self.__proxies, cookies=self.__cookies, allow_redirects=allow_redirects)
        except requests.exceptions.RequestException:
            return None

    def request(self, method, url, params=None, data=None):
        try:
            if self.__session:
                return self.__session.request(method=method, url=url, params=params, data=data, verify=False,
                                              headers=self.__headers, proxies=self.__proxies, cookies=self.__cookies,
                                              allow_redirects=True)
            else:
                return requests.request(method=method, url=url, params=params, data=data, verify=False,
                                        headers=self.__headers, proxies=self.__proxies, cookies=self.__cookies,
                                        allow_redirects=True)
        except requests.exceptions.RequestException:
            return None

    @staticmethod
    def cookie_parse(cookies_str):
        if not cookies_str:
            return {}
        cookie_dict = {}
        cookies = cookies_str.split(';')
        for cookie in cookies:
            cstr = cookie.split('=')
            if len(cstr) > 1:
                cookie_dict[cstr[0]] = cstr[1]
        return cookie_dict
