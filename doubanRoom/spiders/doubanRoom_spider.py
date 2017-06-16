import scrapy
import logging
from scrapy.loader import ItemLoader
from doubanRoom.items import RoomInfoItem
import re


class RoomDoubanspiders(scrapy.Spider):
	name = 'doubanRoom'
	allowed_domains = ['www.douban.com']

	def start_requests(self):
		urls = ['https://www.douban.com/group/106955/discussion?start=0']
		yield scrapy.http.Request(
			url=urls[0],
			callback = self.parse_more
			)


	def parse_more(self, response):
		total_No = 1000
		current_no = 25

		while current_no <= total_No:
			#logging.log(logging.INFO, "*"*40)
			logging.log(logging.INFO, 'current No ' + str(current_no))
			form = {'start':'0'}
			form['start'] = str(current_no)
			current_no = current_no + 25
			yield scrapy.FormRequest(url = 'https://www.douban.com/group/106955/discussion?',
									formdata = form,
									callback=self.parse_basic)

	def parse_basic(self, response):
		resList = response.css('table td[class="title"] a::attr(href)').extract()
		for res in resList:
			l = ItemLoader(item=RoomInfoItem(), response=response)
			l.add_value('url', res)
			yield scrapy.http.Request(
				url=res,
				cookies={'bid':'TGxolmTLUrY','ap':'1','__utmt':'1','__utma':'30149280.584559304.1493105814.1493105814.1493105814.1','__utmb':'30149280.7.4.1493105814','__utmc':'30149280','__utmz':'30149280.1493105814.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)','_pk_id.100001.8cb4':'672d2319542ee755.1493105802.1.1493105827.1493105802.','_pk_ses.100001.8cb4':'*'},
				meta={'il': l},
				callback=self.parse_roomInfo)

	def parse_roomInfo(self, response):
		logging.log(logging.INFO, "*"*40)
		l = response.meta['il']
		cont_list = response.css('div[class="topic-content"] p').extract()
		#logging.log(logging.INFO, str(cont_list))
		all_cont = ""
		for cont in cont_list:
			all_cont = all_cont + cont
		l.add_value('content', all_cont)
		l.add_value('title', response.css('div[id="content"] h1::text').extract_first())
		yield l.load_item()


