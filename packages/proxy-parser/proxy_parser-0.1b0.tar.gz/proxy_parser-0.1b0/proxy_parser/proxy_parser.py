import requests
from bs4 import BeautifulSoup
import base64
import random

header = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	#'Cookie': 'fp=babc03b28b44f60e58ef9a592ff389cf; __utma=104525399.1053798887.1597920914.1597920914.1597920914.1; __utmc=104525399; __utmz=104525399.1597920914.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=104525399.7.10.1597920914',
	'DNT': '1',
	'Host': 'free-proxy.cz',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
	}

class proxy_parser(object):	
	def __init__(self):
		self.index = -1
		self.server   = []
		return

	def get_proxies(self, get_protocol='all', get_list = 1 ):
		"""Constructor get_protocol = https,http,socks4,socks5,socks,all"""		

		for j in range(1, get_list+1): #количество страниц
			response = requests.get('http://free-proxy.cz/ru/proxylist/country/all/'+get_protocol.lower()+'/ping/all/'+ str(j), headers=header ).content.decode()
			soup = BeautifulSoup(response, 'lxml')
	        
			tr = soup.findAll( "tbody")[0].findAll("tr")	# нашел таблицу айпишниками. 

			for i in range( 0, len(tr) ):	                #len(tr) = равен количествк строк в таблице
				if len(tr[i].findAll('td', {'colspan' : "11"} )) != 0: # проверка на пустую строку в tr
					continue	
				ip   =  base64.b64decode( str(tr[i].findAll("td")[0]).split('"')[-2] ).decode("UTF-8") # спарсил ип
				port =  tr[i].findAll("td")[1].text                                                    # спарсил порт
				protocol =  str(tr[i].findAll("td")[2].text).lower()                                   # спарсил протокол

				self.server.append( { "ip":ip, "port":port, "protocol":protocol } )

				print ( i, ip,'\t ', port ,'\t ', protocol,  len(tr) )

		return self.server
	def next_proxy(self):
		"""
		возвращает по одной прокси, с начала до конца списка  
		"""
		self.index = self.index + 1	
		if 	self.index >= len(self.server):
			self.index = 0
		return self.server[ self.index ]

	def random_proxy(self):
		"""
		рандомная прокся из массива server
		"""
		return random.choice(self.server)

#a = proxy_parser() 
#a.get_proxies('https', 1)
#print (a.server[1]['ip'], a.server[1]['port'] ,  a.server[1]['protocol'] , len(a.server), a.next_proxy(), a.random_proxy())
