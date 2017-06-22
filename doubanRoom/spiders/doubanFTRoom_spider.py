# -*- coding: UTF-8 -*-
import scrapy
import logging
from scrapy.loader import ItemLoader
from doubanRoom.items import RoomInfoItem
from doubanRoom.mongoPipeline import MongoPipline
from scrapy.exceptions import CloseSpider
import re
import time
import string


class RoomDoubanFTspiders(scrapy.Spider):
	name = 'doubanFTRoom_spider'
	allowed_domains = ['www.douban.com']

	def start_requests(self):
		urls = ['https://www.douban.com/group/futianzufang/discussion?start=0']
		yield scrapy.http.Request(
			url=urls[0],
			callback = self.parse_more
			)


	def parse_more(self, response):
		import  doubanRoom.globalVarible
		while doubanRoom.globalVarible.current_no <= doubanRoom.globalVarible.total_no:
			#logging.log(logging.INFO, "*"*40)
			logging.log(logging.INFO, 'current No ' + str(doubanRoom.globalVarible.current_no))
			form = {'start':'0'}
			form['start'] = str(doubanRoom.globalVarible.current_no)
			doubanRoom.globalVarible.current_no = doubanRoom.globalVarible.current_no + 25
			yield scrapy.FormRequest(url = 'https://www.douban.com/group/futianzufang/discussion?',
									formdata = form,
									callback=self.parse_basic)

	def parse_basic(self, response):
		resList = response.css('table[class="olt"]').css('tr[class=""]')
		import  doubanRoom.globalVarible
		lastUpdate = doubanRoom.globalVarible.lastUpdateFT
		
		for res in resList:
			item=RoomInfoItem()
			resUrl = res.css('td[class="title"] a::attr(href)').extract_first()
			#l.add_value('url', resUrl)
			updateStr = '2017-' + res.css('td[class="time"]::text').extract_first()
			structUpDate = time.strptime(updateStr,"%Y-%m-%d %H:%M")
			upDateStr =  time.strftime("%Y/%m/%d %H:%M:%S", structUpDate)
			upNumDateStr =  time.mktime(structUpDate)
			if lastUpdate > upNumDateStr:
				doubanRoom.globalVarible.current_no = doubanRoom.globalVarible.total_no
				return 
			item['url'] = resUrl
			item['upDate'] = upDateStr
			item['upNumDate'] = upNumDateStr
			yield scrapy.http.Request(
				url=resUrl,
				cookies={'bid':'zKIXpQFdZbc', '_pk_id.100001.8cb4':'aaf3a2deda6343ca.1497539649.1.1497539649.1497539649.', '_pk_ses.100001.8cb4':'*', '__utmt':'1', '__utma':'30149280.1606629864.1497539650.1497539650.1497539650.1', '__utmb':'30149280.5.6.1497539650', '__utmc':'30149280', '__utmz':'30149280.1497539650.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)','__yadk_uid':'ABqQRLY3TPSw6WA34vI59IqBsrVYZWBT'},
				meta={'il': item},
				callback=self.parse_roomInfo)

	def parse_roomInfo(self, response):
		logging.log(logging.INFO, "*"*40)
		item = response.meta['il']
		cont_list = response.css('div[class="topic-content"] p').extract()
		ownerName = response.css('span[class="from"] a::text').extract_first()
		ownerurl = response.css('span[class="from"] a::attr(href)').extract_first()
		orgDate = response.css('span[class="color-green"]::text').extract_first()
		structOrgDate = time.strptime(orgDate, "%Y-%m-%d %H:%M:%S")
		orgDateNumStr = time.mktime(structOrgDate)
		orgDateStr = time.strftime("%Y/%m/%d %H:%M:%S", structOrgDate)
		tempList = ownerurl.split('/') 
		ownerId = tempList[len(tempList) - 2]
		#logging.log(logging.INFO, str(cont_list))
		all_cont = ""
		for cont in cont_list:
			all_cont = all_cont + cont
		all_cont = self.executeCont(all_cont)
		item['content'] = all_cont
		title = ""
		title = title + response.css('div[id="content"] h1::text').extract_first()
		title = string.replace(title,'\n','')
		title = string.replace(title,'	q','')
		
		item['title'] = title
		item['ownerName'] = ownerName
		item['ownerUrl'] = ownerurl
		item['ownerId'] = ownerId
		item['startTime'] = orgDateStr		
		item['startNumTime'] = orgDateNumStr		
		item['src'] = 'FT'
		yield item


	def executeCont(self, constr):
		constr = string.replace(constr,'<br>','')
		constr = string.replace(constr,'</br>','')
		constr = string.replace(constr,'<p>','')
		constr = string.replace(constr,'</p>','')
		return constr

	# def querycont()


