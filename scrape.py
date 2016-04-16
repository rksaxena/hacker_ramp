# -*- coding: utf-8 -*-
import requests
import scrapy
from scrapy.http import HtmlResponse
import tags
import string
import json

def start_elle():
    seedURL = "http://elle.in/fashion/street-style/"
    s = requests.Session()
    http_response = s.get(seedURL)
    scrapyObject = HtmlResponse(url="HTML Body", body=http_response.content)
    url_xpath = '//div[contains(@class,"first")]/div[DIV_NO]/a/@href'
    data_urls = []
    for i in range(1,17):
        ammended_xpath = url_xpath.replace("DIV_NO",str(i))
        a = scrapyObject.xpath(ammended_xpath)
        u = a.extract()
        if u:
            data_urls.append("http://elle.in"+ u[0])
    print "Extracting data from: " + str(data_urls)

    data = []
    f = open("CrawledOutputElle.txt", 'w')
    all_tags = []
    for url in data_urls:
        httpres = s.get(url)
        s_object = HtmlResponse(url="HTML Body", body=httpres.content)
        a = s_object.xpath('//p[contains(@class,"tags")]/a/span/text()')
        extracted_data = a.extract()
        all_tags = all_tags + extracted_data
        #f.write(str(extracted_data))
        print extracted_data
#        printable = string.printable
#        for line in extracted_data:
#            text = filter(lambda x: x in printable, line)
#            f.write(text + "\n")
    seen = set()
    seen_add = seen.add
    all_tags = [x for x in all_tags if not (x in seen or seen_add(x))]
    f.write(str(all_tags))
    f.close()



def start_zara():
    seedURL_women = "http://www.zara.com/in/en/new-in/woman/view-all-c811528.html"
    seedURL_men = "http://www.zara.com/in/en/new-in/man/view-all-c809013.html"
    s = requests.Session()
    #Wmen
    http_response = s.get(seedURL_women)
    scrapyObject = HtmlResponse(url="HTML Body", body=http_response.content)
    a = scrapyObject.xpath('//div[contains(@class,"product-info")]/a/text()')
    top_zara_article_types_women = a.extract()
    top_zara_article_types_women = [x.lower() for x in top_zara_article_types_women[0:50]]
    print top_zara_article_types_women[0:50]
    #Men
    http_response = s.get(seedURL_men)
    scrapyObject = HtmlResponse(url="HTML Body", body=http_response.content)
    a = scrapyObject.xpath('//div[contains(@class,"product-info")]/a/text()')
    top_zara_article_types_men = a.extract()
    top_zara_article_types_men = [x.lower() for x in top_zara_article_types_men[0:50]]
    print top_zara_article_types_men[0:50]

def start_vogue():
    seedURL = "http://www.vogue.in/fashion/fashion-trends/"
    s = requests.Session()
    http_response = s.get(seedURL)
    scrapyObject = HtmlResponse(url="HTML Body", body=http_response.content)
    data_urls = []
    url_xpath = '//*[@id="eight_grid_block0"]/section[SEC_NO]/div[1]/h3/a/@href'

    for i in range(1,20):
        ammended_xpath = url_xpath.replace("SEC_NO",str(i))
        a = scrapyObject.xpath(ammended_xpath)
        u = a.extract()
        if u:
            data_urls.append(u[0])

    print "Extracting data from: " + str(data_urls)

    data = []
    count_tags = {}
    f = open("CrawledOutput.txt", 'w')
    for url in data_urls:
        httpres = s.get(url)
        s_object = HtmlResponse(url="HTML Body", body=httpres.content)
        a = s_object.xpath('//div[contains(@class,"midContent")]/article/div[1]/p/text()')
        extracted_data = a.extract()
        printable = string.printable
        for line in extracted_data:
            text = filter(lambda x: x in printable, line)
            f.write(text + "\n")
    f.close()


def start_with_file():
    f = open("CrawledOutput.txt", 'r')
    output_tags = {}
    for line in f:
        output_tags.update(tags.main(line))
    json_response = tags.create_response(output_tags)
    print json_response



if __name__ == "__main__":
    start_elle()
