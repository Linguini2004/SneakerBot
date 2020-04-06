import scrapy

snkr_list = open("sneakers", "r")
names = snkr_list.read()
names = names.strip('][').split(', ')
print(names)
root = "https://stockx.com/"
shoe_counter = []
stockx_data = []

def url_formation(search):
    global names
    shoe_names = []
    for s in search:
        search_list = s.split()
        url_part2 = ""
        for (n, i) in enumerate(search_list):
            url_part2 += str(i)
            if n < (len(search_list) - 1):
                url_part2 += "-"
        firsts = root + url_part2
        shoe_names.append(firsts)
        return shoe_names

def dictionary_creation(price, size, url, name):
    # SIZES
    stockx_dict = {}
    size.pop(0)
    print(size)
    size.remove("us All")
    previous = ""
    current = ""
    to_delete = 0
    delete = False
    for i in range(len(size)):
        if delete == False:
            current = size[i].split()
        if i > 0:
            if float(current[1]) < float(previous):
                delete = True
                to_delete = i
            if delete == True:
                size.pop(to_delete)
        previous = current[1]
    for i in range(len(size)):
        size[i] = size[i].upper()
    print(size)
    #PRICES
    price.pop(0)
    while len(price) != len(size):
        price.pop(-1)
    mprice = []
    for i in price:
        if i != "Bid":
            length = (len(i) - 1) * -1
            mprice.append([i[0], float(i[length:])])
        else:
            mprice.append(["","Bid"])

    size_price = {}
    sp_list = []
    print(len(size))
    for n, i in enumerate(size):
        size_price[i] = mprice[n]

    stockx_dict[name] = size_price, url
    return stockx_dict


class StockxSpider(scrapy.Spider):
    name = "stockx"

    start_urls = url_formation(names)

    def parse(self, response):
        global shoe_counter
        global stockx_data
        shoe_counter += 1
        sizes = response.css("div.title::text").getall()
        prices = response.css("div.subtitle::text").getall()

        stockx_data.append(dictionary_creation(prices, sizes, response.request.url, query))
        if shoe_counter == len(names):
            filename = "stockx1"
            with open(filename, 'w') as f:
                f.write(str(stockx_data))

# text = response.css("span.fvDOul::text").getall()
# scrapy shell "https://www.depop.com/products/oxclothing-air-jordan-1-mid-chicago/"
# url[3] ---> url[26]
