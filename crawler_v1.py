from selenium import webdriver
from bs4 import BeautifulSoup

#Pega o html utilizando selenium
class Page:
	def __init__(self, driver):
		self.driver = driver

chrome = webdriver.Chrome()
chrome.get("https://www.reclameaqui.com.br/empresa/oi-movel-fixo-tv/lista-reclamacoes/")
html = chrome.page_source

soup = BeautifulSoup(html, 'lxml')
#print(soup.prettify())



#Pega os titulos e descritivos das reclamações  com bs4
for dado in soup.find_all('div', class_="title-holder"):
	titulo = dado.find('p', class_="text-title ng-binding").text
	print("Título:", titulo)

for reclamacao in soup.find_all('p', class_="text-description ng-binding"):
	print("Reclamação:", reclamacao.text)

for info in soup.find_all('p', class_="text-detail"):
	qq = info.find("span")
	status = qq.find_next('span').text
	print("Status:", status)
	data = info.find('span', class_="hourAgo ng-binding")['title']
	print(data)
	local = info.find('span', class_="hidden-xs ng-binding").text
	print(local)