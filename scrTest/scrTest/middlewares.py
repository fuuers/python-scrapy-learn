# -*- coding: utf-8 -*-

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumMiddleware():

    # 可以拦截到request请求
    def process_request(self, request, spider):
        # 在进行url访问之前可以进行的操作, 更换UA请求头, 使用其他代理等
        pass

    # 可以拦截到response响应对象(拦截下载器传递给Spider的响应对象)
    def process_response(self, request, response, spider):
        if "post" in request.url:
            spider.browser.get(url=request.url)
            try:
                wait = WebDriverWait(spider.browser, 20)
                # 判断所有图片元素加载完成（是否可见）
                element = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@id='gal-nnn']/img[@border='0']")))
                element = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//span[@id='pag-nnn']//a")))
                #element = wait.until(element_has_css_class((By.ID, 'gal-nnn'), "myCSSClass"))

                row_response = spider.browser.page_source
                return HtmlResponse(url=spider.browser.current_url, body=row_response, encoding="utf-8",
                                    request=request,
                                    status=200)  # 参数url指当前浏览器访问的url(通过current_url方法获取), 在这里参数url也可以用request.url
                # 参数body指要封装成符合HTTP协议的源数据, 后两个参数可有可无
            finally:
                pass

        else:
            return response  # 原来的主页的响应对象

class element_has_css_class(object):
    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        # 查找引用的元素
        if self.css_class in element.get_attribute("class"):
            return element
        else:
            return False
