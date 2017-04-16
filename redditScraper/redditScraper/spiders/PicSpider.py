from scrapy import Spider
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
import redditScraper.items as ItemStack

class ImageSpider(CrawlSpider):
    name = "picSpider"

    start_urls=[
       "https://www.reddit.com/r/pics/"
    ]

    allowed_domains=[
#Domain allowed to scrape
        "www.reddit.com"
    ]


    rules = (
        # Extract links matching 'below Regex'
        # and follow links from them (No callback means follow=True by default).
        Rule(LinkExtractor(allow=(".*\/r\/pics\/\?count=\d*&after=(\w*)",)),callback='parse_next',follow=True),
    )



    def parse_next(self,response):
     #Selecting list of elements and parsing one by one
        selector_list=response.xpath("//div[contains(@class,'thing')]")
        for selector in selector_list:
            print(selector)
            item=ItemStack.PicItem()
            item['title']=selector.xpath("div/p/a/text()").extract()
#            item['link_url']=selector.xpath('p[contains(@class,\'title\')]/a/@href').extract()
            item['image_urls']=selector.xpath("a[contains(@class,'thumbnail')]/@href").extract()
            yield item

