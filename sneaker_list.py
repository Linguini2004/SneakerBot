import scrapy

name_list = []
sneaker_counter = 0

def page_finder():
    pages = []
    root = "https://stockx.com/sneakers/most-popular?page="
    for i in range(1, 26):
        current_url = root + str(i)
        pages.append(current_url)
    return pages



class SneakerList(scrapy.Spider):
    name = "sneaker_list"
    start_urls = page_finder()

    def parse(self, response):
        global name_list
        global sneaker_counter

        sneaker_counter += 1
        print(sneaker_counter)

        current_pages = response.css("a::attr(href)").getall()
        for i in range(32):
            current_pages.pop(0)
        for i in range(39, len(current_pages)):
            current_pages.pop(39)
        for i in current_pages:
            name_list.append(i)

        for i in range(len(name_list)):
            name_list[i] = name_list[i].replace("/", "")
            name_list[i] = name_list[i].replace("-", " ")

        print(len(name_list))
        if sneaker_counter == 25:
            filename = "sneakers"
            with open(filename, 'w') as f:
                print("hello")
                for i in name_list:

                    f.write(i + "\n")




