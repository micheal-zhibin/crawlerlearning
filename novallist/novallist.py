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

	divTags = soup.find_all('div', attrs={'class': 'index_toplist'})

	for div in divTags:
		comment = {}
		comment['lists'] = []
		comment['title'] = div.find('div', class_='toptab').span.string

		general_list = div.find(style='display: block;')

		liTags = general_list.find_all('li')

		for li in liTags:
			listitem = {}
		# try:
			listitem['name'] = li.find('a').text.strip()
			listitem['link'] = 'http://www.qu.la/' + li.find('a')['href']
			comment['lists'].append(listitem)
			nov_url_list.append(listitem['link'])
		# except:
		# 	print('some error')
		comments.append(comment)
	return comments

def Out2File(dict):
	with open('TTBT.txt', 'a+') as f:
		for comment in dict:
			f.write('小说种类: {} \n'.format(
				comment['title']
			))
			for listitem in comment['lists']: 
				f.write('小说名: {} \t 小说地址: {} \n'.format(
					listitem['name'], listitem['link']
				))
			f.write('\n')
		print('finish')

def get_txt_url(url):
	comments = []

	html = getHtmlText(url)

	soup = BeautifulSoup(html, 'lxml')

	ddTags = soup.find_all('dd')

	name = soup.find('div', id="info").h1.string

	with open('{}.txt'.format(name), 'a+') as f:
		for dd in ddTags:
			f.write('章节: {} \n'.format(
				dd.a.text.strip()
			))
			novurl = url + dd.a['href']
			html = getHtmlText(novurl)
			soup = BeautifulSoup(html, 'lxml')
			f.write('内容: {} \n'.format(
				soup.find('div', id="content").text.strip()
			))
	print('finish get_txt_url')
	return comments

def main(base_url, deep):
	url_list = []
	for i in range(0, deep):
		url_list.append(base_url)
	print('all html get, start fetching')

	for url in url_list:
		content = get_content(url)
		Out2File(content)
	for url in nov_url_list:
		get_txt_url(url)
	print('all finish')

base_url = 'http://www.qu.la/paihangbang/'

deep = 1

if __name__ == '__main__':
	main(base_url, deep)
