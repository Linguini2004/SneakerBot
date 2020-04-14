import scrapy
import json

item_num = 0
depop_items = {}

with open("sneakers") as h:
  query = [line.strip() for line in h]
  shoe_names = query
root = "https://www.depop.com/search/"

def url_formation(search):
    global url3
    url3 = []
    for s in search:
        # Contraband :-)
        if "air" in s and "nike" not in s:
            s = s.replace("air ", "")
        if "nike" in s:
            s = s.replace("nike ", "")
        if "converse" in s:
            s = s.replace(" converse ", "")
        if "adidas" in s:
            s = s.replace("adidas ", "")
        # Contraband
        search_list = s.split()
        url1 = "?q="
        url2 = ""
        for (n, i) in enumerate(search_list):
            url2 += str(i)
            if n < (len(search_list) - 1):
                url2 += "%20"
        final = root + url1 + url2
        url3.append(final)
    return url3


dep_url = url_formation(query)


class DepopSpider(scrapy.Spider):
    name = "depop"
    start_urls = dep_url


    def parse(self, response):
        global item_num
        global depop_items
        url_listv2 = []

        print(shoe_names[item_num])

        url_list = response.css("a::attr(href)").getall()
        print(len(url_list))
        root = "https://www.depop.com"
        for i in range(len(url_list)):
            url_list[i] = root + url_list[i]
        for i in url_list:
            if "/products" in i:
                url_listv2.append(i)
        depop_items[shoe_names[item_num]] = url_listv2
        print(item_num)
        item_num += 1
        if item_num == len(shoe_names):
            num1 = []
            num2 = []
            for key in depop_items:
                for i in depop_items[key]:
                    num1.append(i)
                    num2.append(key)
            print(len(num1))
            print(len(num2))

            filename = "depop1"
            with open(filename, 'ab') as f:
                f.write(json.dumps(depop_items).encode("utf-8"))
            #    f.write(str(price_dict))

