### proxy_parser
Парсит прокси с сайта http://free-proxy.cz/en/proxylist/country/all/https/ping/all . 
```python
#пример использования

import proxy_parser
#добавляем парсер в свой проект

a = proxy_parser.proxy_parser()  
#создание объекта класса

a.get_proxies('https',1)  
#парсит прокси с сайта в объект класса  
#первый аргумент тип прокси - https,http,socks4,socks5,socks,all.  
#следующий аргумент количество страниц с проксями из сайта(обычно 35 прокси из 1 страницы).  

print (a.server[1]['ip'], a.server[1]['port'],  a.server[1]['protocol'], len(a.server), a.next_proxy())  
#вывод будет таким  
#200.73.132.107 3129 HTTPS 35 {'ip': '51.161.116.223', 'port': '3128', 'protocol': 'HTTPS'}
```
