from selenium import webdriver
from bs4 import BeautifulSoup
import json


#Pega o html utilizando selenium
class Page:
	def __init__(self, driver):
		self.driver = driver


count = 11
for page in range(count):
	chrome = webdriver.Chrome()
	chrome.get(f"https://www.reclameaqui.com.br/empresa/oi-movel-fixo-tv/lista-reclamacoes/?pagina={page+1}")
	html = chrome.page_source
	soup = BeautifulSoup(html, 'lxml')

	def extrair_titulos():
		titulo = list()

		for dado in soup.find_all('div', class_="title-holder"):
			titulo.append(dado.find('p', class_="text-title ng-binding"))
		return titulo 

	def extrair_reclamacao():
		relato = list()

		for tag in soup.find_all('p', class_="text-description ng-binding"):
			relato.append(tag)
		return relato

	def extrair_status():
		situacao = list()

		for info in soup.find_all('p', class_="text-detail"):
			qq = info.find('span')
			situacao.append(qq.find_next('span'))
		return situacao

	def extrair_data():
		data = list()

		for info in soup.find_all('p', class_="text-detail"):	
			localizar_dt = info.find('span', class_="hourAgo ng-binding")['title']
			dt = localizar_dt.split('às')[0]
			data.append(dt)
		return data

	def extrair_local():
		local = list()

		for info in soup.find_all('p', class_="text-detail"):	
			localizar_local= info.find('span', class_="hidden-xs ng-binding")
			local.append(localizar_local)
		return local

	

	aux = extrair_titulos()

	contador = len(aux)

	for x in range(contador):

		titulos = extrair_titulos()
		reclamacoes = extrair_reclamacao()
		status = extrair_status()
		datas = extrair_data()
		localidades = extrair_local()


		arq_titulo = titulos[x].text
		arq_reclamacao = reclamacoes[x].text
		arq_status = status[x].text
		arq_data = datas[x]
		arq_localidade = localidades[x].text
		
		ReclameAqui = {'Titulo' : arq_titulo, 'Reclamacao' : arq_reclamacao, 'Status' : arq_status, 'Data' : arq_data, 'Localidade' : arq_localidade }
		#print(ReclameAqui)
		reclamacoes = {"Reclamaçoes" : ReclameAqui}
		reclamacoes = json.dumps(reclamacoes, indent=6, sort_keys=False)

		arquivo_json = open('reclamaçoes_Oi.json', 'a')
		arquivo_json.write(reclamacoes)
		arquivo_json.close()