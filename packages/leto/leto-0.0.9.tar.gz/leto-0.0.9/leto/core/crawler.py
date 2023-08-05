# -*- coding: utf-8 -*-
# @author: leesoar

"""crawler.py

Usage：
    crawler = Crawler()
    crawler.set_proxies()

    url = "http://httpbin.org/post"
    res = crawler.crawl(url, method="post")
    crawler.log.debug(res)
"""

import abc

import crack
import requests
import urllib3
from anole import UserAgent
from selenium import webdriver

from ..common import config
from ..core.clone import ThreadPool
from ..core.scheduler import MicroQueue
from ..util.decorator import retry, ninja
from ..util.logger import Logger


class BaseCrawler(object, metaclass=abc.ABCMeta):
    """爬虫基类"""

    def __init__(self):
        self._ua = UserAgent()
        self._method = "GET"
        self._timeout = config.REQ_TIMEOUT
        self._stream = False
        self._allow_redirects = True
        self._verify = True
        self._proxies = None
        self.ninja_mode = False
        self.log = Logger(f"{__name__}.log").get_logger()

    def _init_req_params(self):
        """初始化请求参数"""
        self._req_params = {
            "method": self._method,
            "headers": {
                "user-agent": self._ua.random,
            },
            "timeout": self._timeout,
            "stream": self._stream,
            "allow_redirects": self._allow_redirects,
            "verify": self._verify,
            "proxies": self._proxies,
        }

    def disable_ssl(self):
        """取消ssl验证与警告"""
        urllib3.disable_warnings()
        self._verify = False

    def use_ninja(self, status=True):
        """忍者模式

        添加x-forward-for, client_ip头信息
        """
        self.ninja_mode = status

    @staticmethod
    def _close(r, *args, **kwargs):
        """关闭连接"""
        r.close()

    @staticmethod
    def hooks(*func, target="response"):
        return {target: func}

    @ninja
    @retry()
    def crawl(self, url, now=None, **kwargs):
        """请求核心方法

        Args:
            url: 请求网址(str)
            now: 是否立即返回
        Returns:
            res: 响应结果(requests.models.Response)
        """
        self.log.debug(f"正在爬取 {url}")
        self._init_req_params()
        self._req_params.update(kwargs)
        if 'user-agent' not in [key.lower() for key in kwargs.get("headers", {}).keys()]:
            self._req_params['headers']['user-agent'] = self._ua.random
        if 'hooks' in kwargs:
            res = requests.request(url=url, **self._req_params)
        else:
            res = requests.request(url=url, hooks=now and self.hooks(self._close), **self._req_params)
        url == res.url or self.log.debug(f"真实链接 {res.url}")   # 目标url与真实url不同时输出真实链接
        self.log.debug(f"方法：{kwargs.get('method') or self._method}  状态码：{res.status_code}")
        self.log.debug(f"返回长度：{len(res.text)}")
        self.log.debug(f"消耗时间：{res.elapsed.total_seconds()} 秒")
        return res


class Crawler(BaseCrawler):
    """普通爬取类"""

    def __init__(self):
        super().__init__()

    def set_proxies(self, proxies):
        """设置网络代理"""
        self._proxies = proxies

    def get_proxies(self):
        return self._proxies


class SimpleCrawler(BaseCrawler):

    def __init__(self):
        super().__init__()
        self._pool = ThreadPool()
        self._queue = MicroQueue()
        self._qname = crack.token_hex(16)

    def crawl(self, url, now=None, **kwargs):
        if isinstance(url, str):
            return super(SimpleCrawler, self).crawl(url, now=now, **kwargs)

        ret = {}
        self._queue.set_seed(self._qname, *set(url))

        def __crawl():
            while self._queue.qsize(self._qname):
                try:
                    u = self._queue.get_seed(self._qname)
                    ret.update({u: super(SimpleCrawler, self).crawl(u, now=now, **kwargs)})
                except requests.exceptions.ConnectionError:
                    pass

        self._pool.set_task(__crawl, workers=len(url))
        self._pool.start()
        return ret


class AutoCrawler:
    """自动化爬虫"""
    def __init__(self, driver_path):
        self._driver = None
        self._ua = UserAgent()
        self.options = webdriver.ChromeOptions()
        self._driver_path = driver_path
        self.log = Logger(f"{__name__}.log").get_logger()

    def _set_browser(self, name):
        """设置所用浏览器"""

        # 浏览器映射表
        browser_map = {
            "chrome": webdriver.Chrome,
            "firefox": webdriver.Firefox,
        }
        driver = browser_map.get(name.lower())

        if driver:
            self._driver = driver
            self._driver.xpath = self._driver.find_elements_by_xpath
        else:
            raise NameError("请检查浏览器名称是否拼写正确！")

    def set_proxies(self, proxies):
        """设置代理"""
        self.options.add_argument(f"--proxy-server={proxies}")

    def set_headless(self):
        """无界面模式"""
        self.options.add_argument("--headless")

    def develop(self):
        """开发者模式"""
        self.options.add_experimental_option("excludeSwitches", ['enable-automation'])

    def hidden(self):
        """无痕模式"""
        self.options.add_argument("--incognito")

    def disable_js(self):
        """禁用javascript"""
        self.options.add_argument("--disable-javascript")

    def _init_args(self):
        """初始化通用配置"""
        self.options.add_argument("--disable-infobars")   # 禁用浏览器正在被自动化程序控制的提示
        self.options.add_argument(f'--user-agent="{self._ua.random}"')
        self.options.add_argument("--disable-gpu")   # 规避bug
        self.options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
        self.options.add_argument("--disable-dev-shm-usage")

    def get_driver(self, name="chrome"):
        """获取驱动对象"""
        self._init_args()
        self._set_browser(name)
        return self._driver(options=self.options, executable_path=self._driver_path)
