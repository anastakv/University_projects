# -*- coding: utf-8 -*-
"""Коротецкая_ТОБД.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pFtlfFdbzCxnraeFuMSysfr4AnJO0xIL

### Загружаем необходимые библиотеки и данные
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from matplotlib import pyplot as plt
import seaborn as sns
import datetime as dt

data=pd.read_csv('/content/drive/MyDrive/banki_all_responses.csv')

data

## Количество строк и столбцов
print('Размер выборки:', data.shape)  
data.head()

## Посмотрим типы столбцов
data.dtypes

# Посмотрим наличие пустых строк
data.isnull().sum()

#Посмотрим количество неуникальных значений
data.nunique()

"""## Единственный столбец имеет числительные значения и можем посмотреть данные по нему"""

data.describe()

## Сгруппируем по столбцу responses_status  и посмотрим медианное значение
print(data.groupby('responses_status').median())

print('в наборе данных ' + str(round(data.shape[0]/680000*100, 1)) + '% отзывов на сайте')

#Банки-лидеры
banks=pd.DataFrame({'bank':data.bank.value_counts().index, 'freq': data.bank.value_counts().values})
banks=banks[:20]
fig = px.bar(banks, x='freq', y='bank', title= 'Топ 20 банков по отзывам',
             orientation='h')
fig.show()

#Банки-лидеры в процентах
banks=pd.DataFrame({'bank':data.bank.value_counts().index, 'freq': data.bank.value_counts().values})
banks=banks[:20]
fig = px.pie(banks, values='freq', names='bank', title= 'Банки-лидеры по отзывам, %')
fig.show()

data['year']=data['responses_datetime'].apply(lambda x: str(x)[6:10])
years=pd.DataFrame({'year':data.year.value_counts().index, 'freq': data.year.value_counts().values})
fig = px.bar(years, x='year', y='freq', 
            title= 'Отзывы в разрезе по годам')
fig.show()

ind=list(data.responses_status.value_counts().index)
ind.append('Нет данных')
v=list(data.responses_status.value_counts().values)
v.append(data.responses_status.isna().sum())
fig = go.Figure(data=[go.Pie(labels=ind,
                             values=v)])

fig.update_layout(
    title='Распределение заявок по статусам ')


fig.show()

sns.countplot(x='responses_status',data=data);

data['responses_rating_grade'].fillna((data['responses_rating_grade'].mean()))
data.head()

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
import time

sns.boxplot(data.responses_rating_grade)
outliers = data[(data['responses_rating_grade'] > 6)] 
outliers

"""## Обработка текста и очистка"""

import nltk
from nltk.corpus import stopwords
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import re
from wordcloud import WordCloud

nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

russian_stopwords = stopwords.words("russian")
def preprocess_text(text):
    text=re.sub(r'[^а-яА-Я ]', ' ', text.lower())
    tokens = text.split()
    tokens = [token for token in tokens if token not in russian_stopwords\
              and token != " "]
    
    text = " ".join(tokens)
    
    return text

data=data[pd.isnull(data.responses_message)==False]
data=data[(data['responses_status']=='Не засчитана') | (data['responses_status']=='Проблема решена')]
data['responses_message_clean'] = data['responses_message'].apply(lambda x: preprocess_text(x))

"""##  Облако слов с наиболее распространенными в использовании словами"""

from wordcloud import WordCloud
def get_whole_text(data):
    s = ''
    for sentence in data:
        for word in sentence.split():
            s += word +  ' '
    return s

def get_wordCloud(whole_text):
    wordCloud = WordCloud(background_color='white',
                              stopwords=russian_stopwords,
                              width=3000,
                              height=2500,
                              max_words=200,
                              random_state=42).generate(whole_text)
    return wordCloud

# Commented out IPython magic to ensure Python compatibility.
word_list = get_whole_text(data['responses_message_clean'])
l=len(word_list)
procWordCloud = get_wordCloud(word_list[:l//7])
from matplotlib import pyplot as plt
# %matplotlib inline

fig = plt.figure(figsize=(50, 20))
plt.imshow(procWordCloud)
plt.axis('off')
plt.show()

"""## Построим модели

"""

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import ComplementNB
from sklearn.linear_model import LogisticRegression


from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer

from sklearn.metrics import classification_report, accuracy_score, roc_curve, auc
import seaborn as sns

X_train, X_test, y_train, y_test = train_test_split(data['responses_message_clean'], data['responses_status'], test_size=0.3)

log_reg = Pipeline([('tfidf', TfidfVectorizer()), ('Log Reg', LogisticRegression(max_iter=400))])

log_reg.fit(X_train, y_train)
predicted_log_reg = log_reg.predict(X_test)

print(metrics.classification_report(predicted_log_reg, y_test))
print(metrics.accuracy_score(predicted_log_reg, y_test))

fig, ax = plt.subplots(figsize=(7,5))
plt.xticks([],data['responses_status'].unique())
plt.yticks([],data['responses_status'].unique())

sns.heatmap(pd.DataFrame(
    metrics.confusion_matrix(y_test,list(predicted_log_reg))),
    annot=True)
plt.ylabel('Точные')
plt.xlabel('Предсказанные')
plt.show()

