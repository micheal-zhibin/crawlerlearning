from scrapy.selector import Selector

body = open('demo.xml', 'r').read()

# print(body) 

print('get first class content: ')
print(Selector(text=body).xpath('/html/body/class[1]').extract())

print('get last class content: ')
print(Selector(text=body).xpath('/html/body/class[last()]').extract())

print('get first class attr[name]: ')
print(Selector(text=body).xpath('/html/body/class[last()]/name/text()').extract())

print('嵌套使用xpath: ')
subbody=Selector(text=body).xpath('/html/body/class[2]').extract()
print(Selector(text=subbody[0]).xpath('//name/text()').extract())
print(Selector(text=subbody[0]).xpath('//class/name/text()').extract())
print(Selector(text=subbody[0]).xpath('//class/sex/text()').extract())