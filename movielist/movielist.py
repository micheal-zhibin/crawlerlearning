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

	liTags = soup.find('ul', attrs={'class': 'picList clearfix'}).find_all('li')

	for li in liTags:
		comment = {}
		time = ''
		if li.find('div', class_="txt").find('span', class_="sIntro") == None:
			time = '暂无上映时间'
		else: 
			time = li.find('div', class_="txt").find('span', class_="sIntro").string
		comment['name'] = li.find('div', class_="pic").img['title'] + ' ' + time
		comment['img'] = li.find('img')['src']
		comment['intro'] = li.find('p', attrs={'class': 'pTxt pIntroShow'}).text.strip()

		names = []
		linames = li.find('p', attrs={'class': 'pActor'}).find_all('a')

		for atag in linames:
			names.append(atag.string)
		comment['names'] = names

		comments.append(comment)

	return comments

def Out2File(dict):
	with open('TTBT.txt', 'a+') as f:
		for comment in dict:
			f.write('片名: {} \n主演: '.format(
				comment['name']
			))
			for liname in comment['names']: 
				f.write(' {}'.format(
					liname
				))
			f.write('\n')
			f.write('简介: {} \n'.format(
				comment['intro']
			))
			get_pic_from_url('http:' + comment['img'], comment['name'] + '.jpg')
		print('finish')

def get_pic_from_url(url, filename):
	pic_content = requests.get(url, stream=True).content
	open(filename, 'wb').write(pic_content)

def main(base_url, deep):
	url_list = []
	for i in range(0, deep):
		url_list.append(base_url)
	print('all html get, start fetching')

	for url in url_list:
		content = get_content(url)
		Out2File(content)
	print('all finish')

base_url = 'http://dianying.2345.com/top/'

deep = 1

if __name__ == '__main__':
	main(base_url, deep)
