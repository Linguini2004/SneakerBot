import scrapy
import json

with open("depop1", 'rb') as f:
    for line in f:
        d = json.loads(line.strip())

current_shoe = {}
shoe_data_list = []
depop_data = {}
shoe_count = 0
previous_data = []


def url_extraction(dictionary):
    global url_dict
    url_dict = {}
    url_list = []
    for key in dictionary:
        for i in dictionary[key]:
            url_dict[i + "/"] = key
            url_list.append(i)
    return url_list

def condition(description):
    global newcount
    global count
    # remember lower case
    mark = 0
    pro_list = ["new", " ds", "deadstock", "never worn", "dswt", "bnwt", "10/10", "never been worn", "never worn"]
    con_list = [" used", "few times", "outside", "no accesories",  "life left", "restore", "good", "like new", "defect", "9/10",
                "9.5/10", "8/10", "8.5/10", "7/10" "replacement", "no og", "no og box", "no og", "pre-owned", "no box", "no box", "no original"]

    for i in pro_list:
        if description is not None and i in description.lower():
            mark += 1
    for i in con_list:
        if description is not None and i in description.lower():
            mark -= 1
    if mark > 0:
        return "new"


class DepopSpider(scrapy.Spider):
    name = "depop_items"
    start_urls = url_extraction(d)

    def parse(self, response):
        global shoe_data_list
        global previous_data
        global depop_data
        global shoe_count
        new_style = False
        shoe_count += 1
        if shoe_count != 1:
            if url_dict[previous_data[2]] == url_dict[response.request.url]:
                new_style = False
            else:
                new_style = True

        prices = response.css("span.fvDOul::text").getall()
        text = response.css("p.bWcgji::text").get()
        shoe_size = response.css("td.fxiPRF::text").get()

        if new_style == False:
            if condition(text) == "new" and float(prices[1]) > float(20) and shoe_size != "None":
                shoe_data_list.append([shoe_size, prices, response.request.url])

        elif new_style == True:
            current_shoe_name = url_dict[previous_data[2]]
            print(current_shoe_name)
            depop_data[current_shoe_name] = shoe_data_list
            shoe_data_list.clear()
            shoe_data_list.append([shoe_size, prices, response.request.url])



        previous_data = [shoe_size, prices, response.request.url]

        print(shoe_count)
        if shoe_count % 100 == 0:
            print(depop_data)


