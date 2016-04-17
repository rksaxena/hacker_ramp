# -*- coding: utf-8 -*-
import requests
# import scrapy
# from scrapy.http import HtmlResponse
import tags
import string
import json
import re


def start_elle(demo=False):
    if demo:
        return
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
    printable = string.printable
    for tag in all_tags:
        text = filter(lambda x: x in printable, tag)
        f.write(str(text) + "\n")
    # f.write(str(all_tags))
    f.close()


def start_zara(demo=False):
    if demo:
        return

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
    response["tags"] = top_zara_article_types_women[0:50]
    #Men
    http_response = s.get(seedURL_men)
    scrapyObject = HtmlResponse(url="HTML Body", body=http_response.content)
    a = scrapyObject.xpath('//div[contains(@class,"product-info")]/a/text()')
    top_zara_article_types_men = a.extract()
    top_zara_article_types_men = [str(x.lower()) for x in top_zara_article_types_men[0:50]]
    [response["tags"].append(x) for x in top_zara_article_types_men[0:50]]
    f = open("CrawledOutputZara.txt", "w")
    for r in response["tags"]:
        f.write(r + "\n")
    f.close()
    return response


def start_vogue(demo=False):
    if demo:
        return
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

    f = open("CrawledOutputVogue.txt", 'w')
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


def start_with_file_vogue():
    f = open("CrawledOutput.txt", 'r')
    output_tags = {}
    para = ""
    for line in f:
        para += line + "\n"
    output_tags = tags.main(para)
    json_response = tags.create_response(output_tags)
    return add_source(json_response, "vogue")


def add_source(response, source):
    response = json.loads(response)
    response['source'] = source
    return response


def create_elle_response(demo=False):
    start_elle(demo)
    f = open("CrawledOutputElle.txt", 'r')
    tags = []
    for line in f:
        tags.append(line.rstrip()[:-1])
    f.close()
    res = {'source': 'elle', 'brands': tags}
    return res


def create_zara_response(demo=False):
    out = start_zara(demo)
    if demo:
        f = open('CrawledOutputZara.txt', 'r')
        values = []
        for line in f:
            values.append(line)
        f.close()
    else:
        values = out["tags"]

    # values = ['culottes', 'oversized studio shirt', 'studs and chain cross body bag', 'long embroidered bomber jacket', 'multicoloured striped dress', 'frayed peplum top', 'leather platform slides', 'white dungarees with rips', 'blouse with lace trim', 'denim dress', 'high waist skinny trousers', 'denim shirt dress', 'bandana print silk style scarf', 'asymmetric hem shirt', 'cropped trousers with front pleat', 'roll-up sleeve jacket', 'tribal linen coat', 'short tribal skirt', 'crossover metallic sandals', 'bleach wash denim jacket', 'guipure lace bermuda shorts', 'guipure lace bomber jacket', 'wrap skirt', 'oversized linen t-shirt', 'sequin patchwork jacket', 'leather strap sandals', 'tie-dye midi skirt', 'blouse with open back', 'tie-dye jacquard culottes', 'tie-dye hand embroidered poncho', 'mid-rise biker trousers', 'short jumpsuit', 'lace midi dress', 'triple choker necklace', 'straight leg flowing trousers', 'jacket with asymmetric back', 'short jumpsuit', 'striped blouse', 'lace tube skirt', 'guipure lace top', 'bird print flowing bermuda shorts', 'casual roman sandals', 'short jumpsuit', 'mid-rise power stretch trousers', 'short sleeve sweater', 'flat metallic leather sandals', 'lace tube dress', 'openwork coat', 'guipure lace tube dress', 'leather sandals with buckle', 'bomber style jacket', 'plain twill shirt', 'striped back and pocket t-shirt', 'striped indigo shirt', 'striped back and pocket t-shirt', 'striped fabric seamed t-shirt', 'bull denim shirt', 'textured weave suit blazer', 'textured weave suit trousers', 'aviator sunglasses', 'faded denim jumpsuit', 't-shirt with zip on sleeves', 'sweatshirt', 'printed t-shirt', 'flower print t-shirt', 'bleach effect skinny trousers', 'bull denim shirt', 'vintage fade denim dungarees', 'faded indigo striped shirt', 'patch bomber jacket', 'raglan sleeve sweatshirt', 'raglan sleeve sweatshirt', 'textured t-shirt', 'creased texture t-shirt', 'darted trousers with cord', 'textured t-shirt', 'paisley print blazer', 'poplin shirt', 'stretch shirt with mandarin collar', 'paisley print bermuda shorts', 'striped shirt', 'horizontal stripe shirt', 'contrast blue jacket', 'tribal jacquard scarf', 'micro polka dot textured weave bermuda shorts', 'stretch shirt with mandarin collar', 'micro polka dot textured weave blazer', 'poplin shirt with contrasting collar', 'short sleeve nautical print polo shirt', 'short sleeve nautical print polo shirt', 'darted trousers with cord', 'darted trousers with cord', 'short sleeve t-shirt with oversized pocket', 'straw hat', 'short sleeve t-shirt with oversized pocket', 't-shirt with zip on sleeves', 'poplin shirt', 'short sleeve t-shirt with oversized pocket', 'short sleeve t-shirt with oversized pocket', 'street top']
    print len(values)
    values = [re.sub('[^A-Za-z ]+', '', x) for x in values]
    values = [x.lower() for x in values]
    mappings = tags.create_article_type_map_zara(values)
    res = {
        'source': 'zara',
        'misc': []
    }
    for value in values:
        if value in mappings['direct_map']:
            print "Skipped value - " + str(value)
            continue
        if value in mappings['dist_map']:
            at = mappings['dist_map'][value]
            if at not in res:
                res[at] = []
            # if value not in res[at]:
            res[at].append(value)
            continue
        if value in mappings['partial_map']:
            at = mappings['partial_map'][value]
            if at not in res:
                res[at] = []
            # if value not in res[at]:
            res[at].append(value)
            continue
        res['misc'].append(value)
    return res


def create_vogue_response(demo=False):
    start_vogue(demo)
    f = open("CrawledOutputVogue.txt", 'r')
    output_tags = {}
    para = ""
    for line in f:
        para += line + "\n"
    output_tags = tags.main(para)
    json_response = tags.create_response(output_tags)
    return add_source(json_response, "vogue")

if __name__ == "__main__":
    response = [create_vogue_response(True), create_zara_response(True), create_elle_response(True)]
    # response.append(create_zara_response())
    print json.dumps(response)
    # create_elle_response()
