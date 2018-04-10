from bs4 import BeautifulSoup

import requests

def getHtmlText(url):
	try:
		r = requests.get(url, timeout=30)
		# 如果状态码不为200，则发HTTPError异常
		r.raise_for_status()
		# 设置正确的编码方式
		#r.encoding = r.apparent_encoding
		r.encoding = 'utf-8'
		return r.text
	except:
		return "ERROR"

def get_content(url):
	comments = []

	html = getHtmlText(url)

	soup = BeautifulSoup(html, 'lxml')

	liTags = soup.find_all('li', attrs={'class': 'j_thread_list'})

	for li in liTags:
		comment = {}

		try:
			comment['title'] = li.find('a', attrs={'class', 'j_th_tit'}).text.strip()
			comment['link'] = "http://tieba.baidu.com/" + li.find('a', attrs={'class', 'j_th_tit'})['href']
			comment['name'] = li.find('span', attrs={'class', 'tb_icon_author'}).text.strip()
			comment['time'] = li.find('span', attrs={'class', 'pull-right is_show_create_time'}).text.strip()
			comment['replyNum'] = li.find('span', attrs={'class', 'threadlist_rep_num center_text'}).text.strip()

			comments.append(comment)
		except:
			print('some error')
	return comments

def Out2File(dict):
	with open('TTBT.txt', 'a+') as f:
		for comment in dict:
			f.write('标题: {} \t 链接: {} \t 发帖人: {} \t 发帖时间: {} \t 回复数量: {} \n'.format(
				comment['title'], comment['link'], comment['name'], comment['time'], comment['replyNum']
			))
		print('finish')

def main(base_url, deep):
	url_list = []
	for i in range(0, deep):
		url_list.append(base_url + '&np=' + str(50 * i))
	print('all html get, start fetching')

	for url in url_list:
		content = get_content(url)
		Out2File(content)
	print('all finish')

base_url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8'

deep = 3

if __name__ == '__main__':
	main(base_url, deep)
