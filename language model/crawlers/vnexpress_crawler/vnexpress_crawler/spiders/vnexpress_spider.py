# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from vnexpress_crawler.items import VnexpressCrawlerItem

page_count = 0
item_count = 0

class VnexpressSpiderSpider(CrawlSpider):
	name = 'vnexpress_spider'
	allowed_domains = ['vnexpress.net']

	def start_requests(self):
		head_urls = [
			'https://vnexpress.net/tin-tuc/thoi-su/',
			'https://vnexpress.net/tin-tuc/the-gioi/',
			'https://kinhdoanh.vnexpress.net/',
			'https://giaitri.vnexpress.net/',
			'https://thethao.vnexpress.net/',
			'https://vnexpress.net/tin-tuc/phap-luat/',
			'https://vnexpress.net/tin-tuc/giao-duc/',
			'https://suckhoe.vnexpress.net/',
			'https://giadinh.vnexpress.net/',
			'https://dulich.vnexpress.net/',
			'https://vnexpress.net/tin-tuc/khoa-hoc/',
			'https://sohoa.vnexpress.net/',
			'https://vnexpress.net/tin-tuc/oto-xe-may/',
			'https://vnexpress.net/tin-tuc/cong-dong/',
			'https://vnexpress.net/tin-tuc/tam-su/'
		]

		gocnhin = 'https://vnexpress.net/ajax/goc-nhin?page=%d'

		for url in head_urls:
			for i in range(1,501):
				yield scrapy.Request(url=url + 'page/%d.html' % i, callback=self.parse_item)

		for i in range(1,101):
			yield scrapy.Request(url=gocnhin % i, callback=self.parse_gocnhin)
	
	def parse_item(self, response):
		global page_count
		page_count += 1
		print('Processing..' + response.url)
		print('Page_Count: %d' % page_count)

		item_links = response.css('.title_news > a:first-of-type::attr(href)').extract()
		for a in item_links:
			yield scrapy.Request(a, callback=self.parse_detail_page)

	def parse_detail_page(self, response):
		global item_count
		item_count += 1
		print('Item_Count: %d' % item_count)

		title = response.css('.title_news_detail::text').extract()[0].strip()
		description = response.css('.description::text').extract()[0].strip()
		content_list = response.css('.content_detail > p::text, .content_detail > p > span::text').extract()
		content = ''
		for i in content_list:
			content += i

		print('Title: ' + title)

		item = VnexpressCrawlerItem()
		# item['title'] = title
		# item['description'] = description
		item['content'] = title + '\n' + description + '\n' + content
		item['url'] = response.url
		yield item

		file = open('vnexpress.txt', 'a+')
		file.write(title.encode('utf-8') + '\n' + description.encode('utf-8') + '\n' + content.encode('utf-8') + '\n\n')
		file.close()

	def parse_gocnhin(self, response):
		global page_count
		page_count += 1
		print('Processing..' + response.url)
		print('Page_Count: %d' % page_count)
		
		item_links = response.css('.title_item > a:first-of-type::attr(href)').extract()
		for a in item_links:
			yield scrapy.Request(a, callback=self.parse_detail_gocnhin)

	def parse_detail_gocnhin(self, response):
		global item_count
		item_count += 1
		print('Item_Count: %d' % item_count)

		title = response.css('.title_gn_detail::text').extract()[0].strip()
		content_list = response.css('.fck_detail > .Normal::text').extract()
		content = ''
		for i in content_list:
			content += i

		print('Title: ' + title)

		item = VnexpressCrawlerItem()
		# item['title'] = title
		# item['description'] = description

		item['content'] = title + '\n' + content
		item['url'] = response.url
		yield item

		file = open('vnexpress.txt', 'a+')
		file.write(title.encode('utf-8') + '\n' + content.encode('utf-8') + '\n\n')
		file.close()