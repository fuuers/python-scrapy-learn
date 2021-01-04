import scrapy
from scrTest.items import ScrtestItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options    # 使用无头浏览器
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re

class FgoSpider(scrapy.Spider):
    base_url = 'www.baidu.com'
    name = 'mm'
    allowed_domains = ['www.baidu.com']
    start_urls = [base_url]

    def __init__(self):
        chorme_options = Options()
        # 无头浏览器
        # chorme_options.add_argument("--headless")
        # chorme_options.add_argument("--disable-gpu")

        # 设置浏览器非阻塞
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["pageLoadStrategy"] = "none"

        # 不加载图片
        prefs = {'profile.default_content_setting_values': {'images': 2}}
        chorme_options.add_experimental_option('prefs', prefs)

        self.browser = webdriver.Chrome(chrome_options=chorme_options, desired_capabilities=desired_capabilities)

    def start_requests(self):
        for page in range(2, 10):
            url = self.base_url + str(page)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def close(spider, reason):
        spider.browser.quit()

    def parse(self, response):
        urls = []
        objs = response.xpath('//h2[@class="entry-title"]/a')
        for obj in objs:
            href = str(obj.attrib["href"])
            title = str(obj.attrib["title"])
            url = self.base_url + href
            urls.append(url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.pageParse, dont_filter=True)

    def pageParse(self, response):
        page = "00P_"
        objs = response.xpath("//div[@id='gal-nnn']/img")
        path = response.xpath("/html/head/title/text()")[0].root
        for obj in objs:
            item = ScrtestItem()
            item["name"] = page + str(objs.index(obj))
            item["link"] = obj.attrib["src"]
            item["path"] = path
            yield item

        urls = self.getOtherPageUrl(response)
        for url in urls:
            page = (str(int(urls.index(url)) + 1)).rjust(2, '0') + "P_"
            yield scrapy.Request(url=url, meta={"page": page}, callback=self.parseItem, dont_filter=True)

    # 后续页码的处理
    def parseItem(self, response):
        page = response.meta["page"]
        print(f"parseItem============================================================第{page}页")
        objs = response.xpath("//div[@id='gal-nnn']/img")
        path = response.xpath("/html/head/title/text()")[0].root
        for obj in objs:
            item = ScrtestItem()
            item["name"] = page + str(objs.index(obj))
            item["link"] = obj.attrib["src"]
            item["path"] = path
            yield item

    # 传入第一页的html的xpath对象，获取剩余页码的地址
    def getOtherPageUrl(self, response):
        objs = response.xpath('//*[@class="last"]')
        pagesUrl = []
        if len(objs) > 0:
            reobj = re.search(pattern=r'page=([0-9]+)', string=str(objs[0].attrib['href']))
            if reobj:
                post = re.search(pattern=r'post/([0-9]+)', string=str(objs[0].attrib['href'])).group(1)
                n = reobj.group(1)
                n = int(n) + 1
                for i in range(2, n):
                    pagesUrl.append(self.base_url + post + "/" + '?page=' + str(i))
        else:
            objs = response.xpath('//*[@class="page smaller"]')
            for page in objs:
                pagesUrl.append(self.base_url + str(page.attrib['href']))
        return pagesUrl

