import scrapy


class ScrapyTestSpider(scrapy.Spider):
    name = "multi page scraping using scrapy"
    allowed_domains = ["www.scrapethissite.com"]
    start_urls = ["https://www.scrapethissite.com/pages/forms/"]

    def parse(self, response):
        # Extracting "a" elements for each country
        pages_group = response.xpath('//*[@id="hockey"]/div/div[5]/div[1]/ul/li')
        for page in pages_group:
            page_number = page.xpath(".//text()").get()
            link = page.xpath(".//@href").get()
            yield response.follow(url=link, callback=self.parse_page)


    def parse_page(self, response):
            hockey_teams = response.xpath('//*[@id="hockey"]/div/table/tr')
            # Looping through the countries list
            for teams in hockey_teams:
                Team_name = teams.xpath('//td[1]/text()').get().strip()
                Year = teams.xpath('//td[2]/text()').get().strip()
                Wins = teams.xpath('//td[3]/text()').get().strip()
                OTS = teams.xpath('//td[4]/text()').get().strip()
                Losses = teams.xpath('//td[5]/text()').get().strip()
                Win_percent = teams.xpath('//td[6]/text()').get().strip()
                Goals_for = teams.xpath('//td[7]/text()').get().strip()
                Goals_aganist = teams.xpath('//td[8]/text()').get().strip()
                Difference = teams.xpath('//td[9]/text()').get().strip()
                # country_name = country.xpath(".//text()").get()
                # link = country.xpath(".//@href").get()
                # Return data extracted
                yield {
                    'team_name': Team_name,
                    'Year': Year,
                    'Wins': Wins,
                    'OTS': OTS,
                    'Losses': Losses,
                    'Win_percent': Win_percent,
                    'Goals_for': Goals_for,
                    'Goals_aganist': Goals_aganist,
                    'Difference': Difference
                        }





