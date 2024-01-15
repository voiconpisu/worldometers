import scrapy
import logging


class ContriesSpider(scrapy.Spider):
    name = "contries"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    # sử dụng method request.meta

    def parse(self, response):
        contries = response.xpath("//td/a")  # get danh sách các bộ chọn
        for contry in contries:
            name = contry.xpath(".//text()").get()
            link = contry.xpath(".//@href").get()

            yield response.follow(url = link, callback=self.parse_country, meta ={'country_name': name})


    def parse_country(self, response):
        name=response.request.meta['country_name']
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()

            yield {
                'country_name': name,
                # 'name': self.country_name,
                'year': year,
                'population': population
            }

    # def parse(self, response):   # crawl tiêu đề và danh sách tên quốc gia
    #     title = response.xpath("//h1/text()").get()
    #     contries = response.xpath("//td/a/text()").getall()

    #     yield {
    #         'title': title,
    #         'countries': contries
    #     }

    # def parse(self, response):
    #     contries = response.xpath("//td/a")  # get danh sách các bộ chọn
    #     for contry in contries:
    #         name = contry.xpath(".//text()").get()
    #         link = contry.xpath(".//@href").get()

    #     # yield {  #cách 1
    #     #     'country_name': name,
    #     #     'country_link': link
    #     # }
    #         # # absolute_url=f"https://worldometers.info{link}"
    #         # absolute_url=response.urljoin(link)  # cách tạo url tuyệt đối
    #         # yield scrapy.Request(url = absolute_url)
    #         # yield response.follow(url=link)         # cách sử dụng url tương đối
    #         yield response.follow(url=link, callback=self.parse_country)

    # #cách không sử dụng meta
    # country_name=''

    # def parse(self, response):
    #     contries = response.xpath("//td/a")  # get danh sách các bộ chọn
    #     for contry in contries:
    #         name = contry.xpath(".//text()").get()
    #         self.country_name = name
    #         link = contry.xpath(".//@href").get()

    #         yield response.follow(url = link, callback=self.parse_country)


    # def parse_country(self, response):
    #     # logging.info(response.url)
    #     rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
    #     for row in rows:
    #         year = row.xpath(".//td[1]/text()").get()
    #         population = row.xpath(".//td[2]/strong/text()").get()

    #         yield {
    #             'name': self.country_name,
    #             'year': year,
    #             'population': population
    #         }

