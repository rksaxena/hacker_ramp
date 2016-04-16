import requests
import scrapy
from scrapy.http import HtmlResponse

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
for url in data_urls:
    httpres = s.get(url)
    s_object = HtmlResponse(url="HTML Body", body=httpres.content)
    a = s_object.xpath('//div[contains(@class,"midContent")]/article/div[1]/p/text()')
    data.append(a.extract())

print data
    
