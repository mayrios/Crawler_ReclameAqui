import nltk
from nltk.corpus import stopwords
import string
import pandas as pd
import csv
import re
import unicodedata

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.metrics import classification_report, confusion_matrix


arquivo = open('tituloscomsentimentos.csv', encoding='latin-1')
texto = csv.reader(arquivo)


def processa_texto(text):
	regex = re.compile('[%s]' % re.escape(string.punctuation))

	vetor_texto = []

	words = text.split()

	for row in words:
		new_token = regex.sub(u'', row)
		if not new_token == u'':
			vetor_texto.append(new_token)

	stopwords = nltk.corpus.stopwords.words('portuguese')
	conteudo = [w for w in vetor_texto if w.lower().strip() not in stopwords]

	clean_text = []

	for palavra in conteudo:

		nfkd = unicodedata.normalize('NFKD', palavra)
		palavraSemAcento = u''.join([c for c in nfkd if not unicodedata.combining(c)])
		q = re.sub('[^a-zA-Z0-9 \\\]',' ',palavraSemAcento)

		clean_text.append(q.lower().strip())

	tokens = [t for t in clean_text if len(t)>2 and not t.isdigit()]

	frase_tratada = ' '.join(tokens)
	return frase_tratada


reclamacoes = pd.read_csv('arquivo_tratado_classificado.csv', encoding='utf-8')
titulos = reclamacoes['titulo']
tipo = reclamacoes['sentimento']


msg_train, msg_test, class_train, class_test = train_test_split(titulos, tipo, test_size=0.2)

#pipeline de transformação com estimador. sequencialmente aplica uma lista de transformações
pipeline = Pipeline([
   ('bow',CountVectorizer(analyzer=processa_texto)), #a primeira converte documentos de texto em uma matriz com contagem de tokens, ou seja, conta a ocorrência de cada palavra no vocabulário
  ('tfidf',TfidfTransformer()), #a segunda normaliza a contagem de palavras de cada conjunto e escala para baixo o impacto de tokens que ocorrem frequentemente e que sejam menos informativos do que features que ocorrem em uma pequena fração do treinamento
  ('classifier',MultinomialNB()) #a última linha treina esses vetores no classificador naive bayes
])

pipeline.fit(msg_train,class_train)

#treina o modelo
pipeline.fit(msg_train,class_train)

#testa o modelo
predictions = pipeline.predict(msg_test)

#mostra os resultados
print(classification_report(class_test,predictions))
print(metrics.accuracy_score(class_test,predictions))

#nltk.download()


