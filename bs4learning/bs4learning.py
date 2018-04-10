from bs4 import BeautifulSoup

soup = BeautifulSoup(open('./alice.html'), 'lxml')

# print(soup.prettify())
# for link in soup.find_all('a'):
# 	print(link.get('href'))
# print(soup.get_text())
# print(soup.body.b)
# for child in soup.head.descendants:
# 	print(child)
for string in soup.strings:
	print(repr(string))