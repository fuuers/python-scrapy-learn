from scrapy.cmdline import execute
import selenium
from selenium import webdriver

if __name__ == '__main__':
    print('e')

    execute(["scrapy", "crawl", "fgo", "--nolog"])