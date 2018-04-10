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
		return "Something Wrong!"