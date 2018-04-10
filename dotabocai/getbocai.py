from bs4 import BeautifulSoup

import requests

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

	divTags = soup.find_all('div', attrs={'class': 'matchmain'})

	for div in divTags:
		comment = {}

		try:
			comment['time'] = div.find('div', attrs={'class', 'whenm'}).text.strip()
			teamname = div.find_all('span', attrs={'class', 'team_name'})
			if teamname[0].string[0:3] == 'php':
				comment['team1_name'] = 'no teamname'
			else:
				comment['team1_name'] = teamname[0].string
			if teamname[1].string[0:3] == 'php':
				comment['team2_name'] = 'no teamname'
			else:
				comment['team2_name'] = teamname[1].string
			comment['team1_winrate'] = div.find_all('span', attrs={'class', 'team_number_green'})[0].string
			comment['team2_winrate'] = div.find_all('span', attrs={'class', 'team_number_red'})[0].string
			comments.append(comment)
		except:
			print('some error')
	return comments

def Out2File(dict):
	with open('TTBT.txt', 'a+') as f:
		for comment in dict:
			f.write('比赛时间: {}, \n 队伍-: {} \t 胜率: {} \n 队伍二: {} \t 胜率: {} \n'.format(
				comment['time'], comment['team1_name'], comment['team1_winrate'], comment['team2_name'], comment['team2_winrate']
			))
		print('finish')

def main(base_url, deep):
	url_list = []
	for i in range(0, deep):
		url_list.append(base_url)
	print('all html get, start fetching')

	for url in url_list:
		content = get_content(url)
		Out2File(content)
	print('all finish')

base_url = 'http://dota2bocai.com/match'

deep = 1

if __name__ == '__main__':
	main(base_url, deep)
