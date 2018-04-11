from bs4 import BeautifulSoup

import requests

nov_url_list=[]

def getHtmlText(url):
	try:
		r = requests.get(url, timeout=30)
		# 如果状态码不为200，则发HTTPError异常
		r.raise_for_status()
		# 设置正确的编码方式
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return "ERROR"

def get_content(url):
	comments = []

	html = getHtmlText(url)

	soup = BeautifulSoup(html, 'lxml')

	liTags = soup.find('ul', attrs={'id': 'rankList'}).find_all('li')

	for li in liTags:
		comment = {}

		comment['scroe'] = li.find('div', class_="score_box").h3.string
		comment['rank'] = li.find('div', class_="top_num").text.strip()
		comment['name'] = li.find('div', class_="info").h3.a.string
		comment['time'] = li.find('p', class_="c9").text.strip()
		comment['singer'] = li.find('p', class_="cc").find('a', class_="special").text.strip()

		comments.append(comment)

	return comments

def Out2File(dict, type):
	with open('TTBT.txt', 'a+') as f:
		title = ''
		if type == 'ML':
			title = '内地排行榜'
		elif type == 'HT':
			title = '港台排行榜'
		elif type == 'US':
			title = '欧美排行榜'
		elif type == 'JP':
			title = '韩国排行榜'
		elif type == 'KR':
			title = '日本排行榜'
		f.write('{} \n'.format(
			title
		))
		for comment in dict:
			f.write('分数: {}, 排名: {}, 名字: {}, 发布时间: {}, 歌手: {} \n'.format(
				comment['scroe'], comment['rank'], comment['name'], comment['time'], comment['singer']
			))
		f.write('\n')
		print('finish')

def get_pic_from_url(url, filename):
	pic_content = requests.get(url, stream=True).content
	open(filename, 'wb').write(pic_content)

def main(base_url, deep):
	url_list = []
	for i in deep:
		content = get_content(base_url + i)
		Out2File(content, i)
	print('all finish')

base_url = 'http://vchart.yinyuetai.com/vchart/trends?area='

deep = ['ML','HT','US','JP','KR']

if __name__ == '__main__':
	main(base_url, deep)
