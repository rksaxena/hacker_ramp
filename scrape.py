# -*- coding: utf-8 -*-
import requests
import scrapy
from scrapy.http import HtmlResponse
import tags
import string
import json

def start_zara():
    seedURL_women = "http://www.zara.com/in/en/new-in/woman/view-all-c811528.html"
    seedURL_men = "http://www.zara.com/in/en/new-in/man/view-all-c809013.html"
    s = requests.Session()
    response = {}
    #Wmen
    http_response = s.get(seedURL_women)
    scrapyObject = HtmlResponse(url="HTML Body", body=http_response.content)
    a = scrapyObject.xpath('//div[contains(@class,"product-info")]/a/text()')
    top_zara_article_types_women = a.extract()
    top_zara_article_types_women = [str(x.lower()) for x in top_zara_article_types_women[0:50]]
    response["women"] = top_zara_article_types_women[0:50]
    #Men
    http_response = s.get(seedURL_men)
    scrapyObject = HtmlResponse(url="HTML Body", body=http_response.content)
    a = scrapyObject.xpath('//div[contains(@class,"product-info")]/a/text()')
    top_zara_article_types_men = a.extract()
    top_zara_article_types_men = [str(x.lower()) for x in top_zara_article_types_men[0:50]]
    response["men"] = top_zara_article_types_men[0:50]
    return response

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


def create_zara_response():
    response = start_zara()
    out_response = {
        'zara': response
    }
    print json.dumps(out_response)
    return out_response

if __name__ == "__main__":
    start_with_file()
