import scrapy

newcount = 0
count = 0
name = "test"   #input("what is the name of the item? ")
#query = input("What do you want to search? ")
query = ["jordan gatorade", "jordan 1 pine green"]
print(query)

current_shoe = []
root = "https://www.depop.com/search/"
price_dict = {}

def url_formation(search):
    global url3
    url3 = []
    for s in search:
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


def condition(description):
    global newcount
    global count
    count += 1
    # remember lower case
    mark = 0
    pro_list = ["new", " ds", "deadstock", "never worn", "dswt", "bnwt", "10/10", "never been worn", "never worn"]
    con_list = ["used", "few times", "outside", "no accesories",  "life left", "restore", "good", "like new", "defect", "9/10",
                "9.5/10", "8/10", "8.5/10", "7/10" "replacement", "no og", "no og box", "no og", "pre-owned", "no box", "no box", "no original"]
    print(description)

    for i in pro_list:
        if description is not None and i in description.lower():
            print("p", i)
            mark += 1
    for i in con_list:
        if description is not None and i in description.lower():
            print("c", i)
            mark -= 1
    print(mark)
    if mark > 0:
        newcount +=1
        print("new")
        return "new"


dep_url = url_formation(query)


class DepopSpider(scrapy.Spider):
    name = "depop"
    start_urls = dep_url

    def parse(self, response):
        global price_dict

        prices = response.css("span.fvDOul::text").getall()
        text = response.css("p.bWcgji::text").get()
        shoe_size = response.css("td.fxiPRF::text").get()
        print(shoe_size)

        if "?q=" not in response.request.url:
            if condition(text) == "new" and float(prices[1]) > float(20):
                current_shoe.append([shoe_size, prices, response.request.url])
                price_dict[name] = current_shoe

        url_list = response.css("a::attr(href)").getall()
        root = "https://www.depop.com"
        depop_items = []

        print("n", newcount)
        print("c", count)

        for i in url_list:
            if "/products/" in i:
                product_url = root + i
                depop_items.append(product_url)

        for i in depop_items:
            next_page = i
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

        filename = "depop1"
        with open(filename, 'w') as f:
            f.write(str(price_dict))

# text = response.css("span.fvDOul::text").getall()
# scrapy shell "https://www.depop.com/products/oxclothing-air-jordan-1-mid-chicago/"
# url[3] ---> url[26]
