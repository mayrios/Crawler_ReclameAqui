from bs4 import BeautifulSoup
import requests

site = requests.get('https://www.reclameaqui.com.br/').text

soup = BeautifulSoup(site, 'lxml')

print(soup.prettify())

#for reclamacao in soup.find_all('li', class_='ng-scope'):
#	titulo = li.a.href.content
#	print(titulo)
 
