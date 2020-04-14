import scrapy
import pickle
import json

with open("sneakers") as f:
  names = [line.strip() for line in f]
root = "https://stockx.com/"
start_point = int(input("What round, Davide? "))
amount = int(input("How many shoes this time round? "))
shoe_counter = 0
stockx_data = []

def url_formation(search):
    global start_point
    global names
    global shoe_names
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
    floor_num = (start_point - 1) * amount
    roof_num = start_point * amount
    for i in range(floor_num):
        shoe_names.pop(0)
    for i in range(len(names) - roof_num):
        shoe_names.pop(amount)
    return shoe_names

def dictionary_creation(price, size, url, name):
    # SIZES
    stockx_dict = {}
    size.pop(0)
    size.remove("us All")
    previous = ""
    current = ""
    to_delete = 0
    delete = False
    for i in range(len(size)):
        if delete == False:
            current = size[i].split()
        if i > 0 and "W" not in current[1] and "W" not in previous and "Y" not in current[1] and "Y" not in previous:
            if float(current[1]) < float(previous):
                delete = True
                to_delete = i
            if delete == True:
                size.pop(to_delete)
        previous = current[1]
    for i in range(len(size)):
        size[i] = size[i].upper()
    #PRICES
    price.pop(0)
    while len(price) != len(size):
        price.pop(-1)
    mprice = []
    for i in price:
        if i != "Bid":
            i = i.replace(",", "")
            i = i.replace("K", "000")
            length = (len(i) - 1) * -1
            mprice.append([i[0], float(i[length:])])
        else:
            mprice.append(["","Bid"])

    size_price = {}
    sp_list = []
    for n, i in enumerate(size):
        size_price[i] = mprice[n]

    stockx_dict[name] = size_price, url
    return stockx_dict


class StockxSpider(scrapy.Spider):
    name = "stockx"

    start_urls = url_formation(names)

    def parse(self, response):
        global shoe_names
        global shoe_counter
        global stockx_data
        shoe_counter += 1
        print(shoe_counter)
        sizes = response.css("div.title::text").getall()
        prices = response.css("div.subtitle::text").getall()

        stockx_data.append(dictionary_creation(prices, sizes, response.request.url, names[shoe_counter - 1]))
        if shoe_counter == len(shoe_names):
            filename = "stockx1"
            if start_point == 1:
                mode = "wb"
            else:
                mode = "ab"
            with open(filename, mode) as f:
                for shoe in stockx_data:
                    f.write(json.dumps(shoe).encode("utf-8") + b"\n")
                    mode = "ab"
            f.close()

# text = response.css("span.fvDOul::text").getall()
# scrapy shell "https://www.depop.com/products/oxclothing-air-jordan-1-mid-chicago/"
# url[3] ---> url[26]
