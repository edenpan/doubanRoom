# -*- coding: UTF-8 -*-
import pymongo
import globalVarible
class MongoPipline(object):
	collection_name = 'doubanFTRoom'
	# global lastUpdate
	# global lastOrgdate
	# lastOrgdateFT = 0.0
	# lastOrgdateSZ = 0.0
	def __init__(self, mongo_uri, mongo_db):
		self.mongo_uri = mongo_uri
		self.mongo_db = mongo_db

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			mongo_uri = crawler.settings.get('MONGO_URI'),
			mongo_db = crawler.settings.get('MONGO_DATABASE', 'items')
			)

	def open_spider(self, spider):
		self.client = pymongo.MongoClient(self.mongo_uri)
		self.db = self.client[self.mongo_db]
		dataSZ = self.db[self.collection_name].find({'src':'SZ'}).sort([('upNumDate',pymongo.DESCENDING)]).limit(1)
		dataFT = self.db[self.collection_name].find({'src':'FT'}).sort([('upNumDate',pymongo.DESCENDING)]).limit(1)
		if dataFT.count() > 0:
			globalVarible.lastUpdateFT  = dataFT[0].get('upNumDate')	
			globalVarible.lastOrgdateFT  = dataFT[0].get('startNumTime')
		else :
			globalVarible.lastUpdateFT = 0.0	
			globalVarible.lastOrgdateFT = 0.0	
		if dataSZ .count() > 0:
			globalVarible.lastUpdateSZ  = dataSZ[0].get('upNumDate')
			globalVarible.lastOrgdateSZ  = dataSZ[0].get('startNumTime')
		else :
			globalVarible.lastUpdateSZ = 0.0
			globalVarible.lastOrgdateSZ = 0.0
		# global lastOrgdate 
		# lastOrgdate = globalVarible.lastOrgdate
		

	def close_spider(self, spider):
		self.client = pymongo.MongoClient(self.mongo_uri)
		self.db = self.client[self.mongo_db]

	def process_item(self, item, spider):
		if (item.get('startNumTime') is not None):
			if (u'求租' not in item.get('content')) and (u'求租' not in item.get('title')):
				if(item.get('src') == 'FT'):
					if(globalVarible.lastOrgdateFT < item['startNumTime']):
						self.db[self.collection_name].insert(dict(item))
				if(item.get('src') == 'SZ'):
					if(globalVarible.lastOrgdateSZ < item['startNumTime']):
						self.db[self.collection_name].insert(dict(item))
		return item			

# def getLastUpdate():
# 	return lastUpdate

# def getLastOrgdate():
# 	return lastOrgdate