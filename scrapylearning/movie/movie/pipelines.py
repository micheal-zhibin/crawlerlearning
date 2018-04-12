# -*- coding: utf-8 -*-
import os
import requests
import json
import codecs
import pymysql

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MoviePipeline(object):
	def process_item(self, item, spider):
		base_dir = os.getcwd()

		filename = base_dir + '/data/movie.txt'

		with open(filename, 'a') as f:
			f.write(item['title'] + '\t')
			f.write(item['names'] + '\n')
			f.write(item['intro'] + '\n')
			f.write('\n')

		with open(base_dir + '/data/' + item['title'] + '.png', 'wb') as f:
			f.write(requests.get(item['img']).content)
		return item

class W2json(object):
	def process_item(self, item, spider):
		base_dir = os.getcwd()
		filename = base_dir + '/data/movie.json'

		with codecs.open(filename, 'a') as f:
			line = json.dumps(dict(item), ensure_ascii=False) + '\n'
			f.write(line)

		return item

class W2mysql(object):
	def process_item(self, item, spider):

		title = item['title']
		names = item['names']
		intro = item['intro']
		img = item['img']

		connection = pymysql.connect(
			host='localhost',
			user='root',
			passwd='root',
			db='scrapyDB',
			charset='utf8mb4',
			cursorclass=pymysql.cursors.DictCursor)

		try:
			with connection.cursor() as cursor:
				sql = "INSERT INTO MOVIE(title,names,intro,img) VALUES (%s,%s,%s,%s)"
				cursor.execute(sql, (title, names, intro, img))
			connection.commit()
		finally:
			connection.close()

		return item
