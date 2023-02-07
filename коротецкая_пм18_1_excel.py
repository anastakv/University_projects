# -*- coding: utf-8 -*-
"""Коротецкая_ПМ18_1_excel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ep_wYRm4hfJQtTtztqfRtAgJ3GXRp8rz

# Работа с Excel

v 0.1

Датасет: себестоимостьА_в1.xlsx

Используя xlwings:

1.1 На листе "Рецептура" для области "Пшеничный хлеб" рассчитать себестоимость всех видов продукции.

1.2 Результаты рассчетов 1.1 сохранить в отдельном столбце области "Пшеничный хлеб"

1.3 Максимально приблизить форматирование столбца, добавленного в 1.2 к оформлению всей области.

1.4 Заменить значения добавленные в 1.2 на формулы. 

1.5 Выполнить 1.4 с помощью "протягиваемых" формул.

1.6 Сдлеать так, чтобы решение 1.5 и 1.3 автоматически применилось ко всем аналогичным областям на листе "Рецептура"
"""

import xlwings as xw
import numpy as np
import pandas as pd
from xlwings import constants 
from xlwings.constants import AutoFillType

wb = xw.Book('себестоимостьА_в1.xlsx')
recipies = wb.sheets['Рецептура']

#1
consumption = recipies.range('G7:O10').options(np.array).value
consumption = np.nan_to_num(consumption)
unit_prices = recipies.range('G14:O14').options(np.array).value
cost = consumption @ unit_prices
cost

#1
recipe1 = recipies.range('рцп_пшеничный_хлеб').value
prices = [item for item in recipe1 if item[0] == 'Цена ресурсов, руб.'][0]
prices = [item for item in prices if not isinstance(item, str)]
pricesNP = np.array(prices)
pricesNP = np.where(pricesNP==None, 0, pricesNP) 
for hlebushek in recipe1[3:-6]:
    temp = np.array(hlebushek[1:])
    temp = np.where(temp==None, 0, temp) 
    answer = pricesNP * temp
    print(sum(answer[1:]))

#2    
recipies.range('T6').value = 'Себестоимость'
recipies.range('T7').options(transpose=True).value = cost

#3
recipies.range('T7:T10').options(transpose=True).value = cost
xw.Range('T7:T10').number_format = '0,00'
xw.Range('T7:T10').color = (255, 255, 167)
recipies.range('T4:T6').api.merge()
recipies.range('T6').value = 'Себестоимость'
xw.Range('T4:T6').color = (255, 192, 0)
xw.Range('T4:T6').autofit()

#4
xw.Range('U7').formula = '=SUMPRODUCT(G7:O7,$G$14:$O$14)'

#5
xw.Range('U7').formula = '=SUMPRODUCT(G7:O7,$G$14:$O$14)' 
xw.Range('U7').api.autofill(destination=recipies.range("U7:U10").api, type=AutoFillType.xlFillDefault)

#6
xw.Range('S23').formula = '=SUMPRODUCT(G23:N23,$G$31:$N$31)' 
xw.Range('S23').api.autofill(destination=recipies.range("S23:S25").api, type=AutoFillType.xlFillDefault)
recipies.range('S22').value = 'Себестоимость'
xw.Range('AC40').formula = '=SUMPRODUCT(G40:X40,$G$52:$X$52)' 
xw.Range('AC40').api.autofill(destination=recipies.range("AC40:AC46").api, type=AutoFillType.xlFillDefault)
recipies.range('AC39').value = 'Себестоимость'
xw.Range('AD61').formula = '=SUMPRODUCT(G61:Y61,$G$73:$Y$73)' 
xw.Range('AD61').api.autofill(destination=recipies.range("AD61:AD69").api, type=AutoFillType.xlFillDefault)
recipies.range('AD60').value = 'Себестоимость'

"""Используя xlwings:

2.1 Собрать цены всех ресурсов, используемые на листе "Рецептура". Проверить, что нет расхождений между ценами совпадающих ресурсов.

2.2 Вынести цены ресурсов в новую таблицу на новом листе "Цена ресурсов". 

2.3 Заменить фиксированные цены ресурсов на листе "Рецептура" на ссылки на лист "Цена ресурсов"

2.4 Сделать так, чтобы цены ресурсов на листе "Рецептура" подтягивались с листа "Цена ресурсов" по наименованию (подсказка: использовать ВПР, рекомендуется использовать именованные области)
"""

#1
ph = dict(zip(recipies.range('G5:O5').options(np.array).value, recipies.range('G14:O14').options(np.array).value))
rh = dict(zip(recipies.range('G21:N21').options(np.array).value, recipies.range('G31:N31').options(np.array).value))
hsr = dict(zip(recipies.range('G38:X38').options(np.array).value, recipies.range('G52:X52').options(np.array).value))
sv = dict(zip(recipies.range('G59:Y59').options(np.array).value, recipies.range('G73:Y73').options(np.array).value))


def check_eq(i, j):
    pr = no1[i][j]
    for k in range(i):
        if j in no1[k].keys():
            if pr != no1[k][j]:
                print('Цены не сходятся')

no1 = [ph, rh, hsr, sv]
ingr = []
for i in range(len(no1)):
    for j in no1[i].keys():
        if j not in ingr:
            ingr.append(j)
        else:
            check_eq(i, j)

#2
no2 = {}
for i in ingr:
    for j in range(len(no1)):
        if i in no1[j].keys():
            no2[i] = no1[j][i]
wb.sheets.add('Цена ресурсов')
ingred = wb.sheets['Цена ресурсов']
ingred.range('A1').options(transpose=True).value = list(no2.keys())
ingred.range('B1').options(transpose=True).value = list(no2.values())

#3, 4
recipies.range('G14').formula = "=VLOOKUP(G5;'Цена ресурсов'!$A$1:$B$32;2;0)"
recipies.range('G14').api.autofill(destination=recipies.range("G14:O14").api, type=AutoFillType.xlFillDefault)

recipies.range('G31').formula = "=VLOOKUP(G21;'Цена ресурсов'!$A$1:$B$32;2;0)"
recipies.range('G31').api.autofill(destination=recipies.range("G31:N31").api, type=AutoFillType.xlFillDefault)

recipies.range('G52').formula = "=VLOOKUP(G38;'Цена ресурсов'!$A$1:$B$32;2;0)"
recipies.range('G52').api.autofill(destination=recipies.range("G52:X52").api, type=AutoFillType.xlFillDefault)

recipies.range('G73').formula = "=VLOOKUP(G59;'Цена ресурсов'!$A$1:$B$32;2;0)"
recipies.range('G73').api.autofill(destination=recipies.range("G73:Y73").api, type=AutoFillType.xlFillDefault)

"""3.1 Создать нормализованную (не ниже 3й нормальной формы) базу данных sqlite для хранения информации из себестоимостьА_в1.xlsx .

Используя xlwings:

3.2 Информацию из себестоимостьА_в1.xlsx внести в БД на sqlite.

3.3 По базе данных sqlite сгенерирвать книгу эксель, по структуре аналогичную себестоимостьА_в1.xlsx

3.4 При помощи макроса на xlwings сделать в Excel кнопку, по которой все изменения на листе вносятся в БД, а цвет ячеек, в которых были найдены изменения, меняслся на зеленый.

3.5 Реализовать UDF, которая позволяет по имени ресурса вернуть количество видов в продукции в которых используется данный ресурс

3.6 Реализовать UDF, которая позволяет по имени ресурса вернуть массив наименований продуктов, в которых используется данный ресурс

3.7 Реазливать UDF 3.5 и 3.6 которые для получения ответа использую не книгу Excel а БД на sqlite.
"""

from sqlalchemy import create_engine

#1
hleb = pd.DataFrame(np.concatenate((recipies.range('C7:F10').options(np.array).value, 
                recipies.range('C23:F25').options(np.array).value, 
                recipies.range('C40:F46').options(np.array).value, 
                recipies.range('C61:F69').options(np.array).value)), 
                   columns = list(recipies.range('C4:F4').options(np.array).value))

hleb['Тип продукта'] = [1] * 4 + [2] * 3 + [3] * 7 + [4] * 9

hleb

a = recipies.range('B3').value + '.'+ recipies.range('B19').value+'.'  + recipies.range('B36').value + '.'+ recipies.range('B57').value
tip_prod = pd.DataFrame()
tip_prod['Тип продукта'] = list(range(1, 5))
tip_prod['Название типа продукта'] = a.split('.')

tip_prod

ingredients = pd.DataFrame(ingred.range('A1:B32').options(np.array).value, 
                          columns = ['Ингридиент', 'Цена'])
ingredients['ID_ing'] = list(range(1, len(ingredients)+1))
# ingredients['Средний физический расход ресурсов'] = recipies.range('G7:O7').options(np.array).value
# ingredients['Размерность физических единиц'] = recipies.range('G7:O7').options(np.array).value

ingredients

recipies.range('G7:O7').options(np.array).value

recept = pd.DataFrame(np.concatenate((recipies.range('G7:O7').options(np.array).value, 
                                    recipies.range('G8:O8').options(np.array).value,
                                    recipies.range('G9:O9').options(np.array).value,
                                    recipies.range('G10:O10').options(np.array).value,
                                    recipies.range('G23:N23').options(np.array).value, 
                                    recipies.range('G24:N24').options(np.array).value,
                                    recipies.range('G25:N25').options(np.array).value,
                                    recipies.range('G40:X40').options(np.array).value,
                                    recipies.range('G41:X41').options(np.array).value,
                                    recipies.range('G42:X42').options(np.array).value,
                                    recipies.range('G43:X43').options(np.array).value,
                                    recipies.range('G44:X44').options(np.array).value,
                                    recipies.range('G45:X45').options(np.array).value,
                                    recipies.range('G46:X46').options(np.array).value,
                                    recipies.range('G61:Y61').options(np.array).value, 
                                   recipies.range('G62:Y62').options(np.array).value,
                                   recipies.range('G63:Y63').options(np.array).value,
                                   recipies.range('G64:Y64').options(np.array).value,
                                   recipies.range('G65:Y65').options(np.array).value,
                                   recipies.range('G66:Y66').options(np.array).value,
                                   recipies.range('G67:Y67').options(np.array).value,
                                   recipies.range('G68:Y68').options(np.array).value,
                                   recipies.range('G69:Y69').options(np.array).value)), 
                   columns = ['Количество ингридиента'])

x = []
for i in list(np.concatenate((recipies.range('G5:O5').options(np.array).value, 
                recipies.range('G21:N21').options(np.array).value, 
                recipies.range('G38:X38').options(np.array).value, 
                recipies.range('G59:Y59').options(np.array).value))):
    q = ingredients[ingredients['Ингридиент'] == i]['ID_ing'].reset_index(drop = True)
    x.append(q[0])
recept['Хлеб'] = [1] * 9 + [2] * 9 + [3] * 9 + [4] * 9 + [5] * 8 + [6] * 8 + [7] * 8 + [8] * 18 + [9] * 18 + [10] * 18 + [11] * 18 + [12] * 18 + [13] * 18 + [14] * 18 + [15] * 19 + [16] * 19 + [17] * 19 + [18] * 19 + [19] * 19 + [20] * 19 + [21] * 19 + [22] * 19 + [23] * 19 
recept['ID_ing'] = x[:9] * 4 + x[9:17] * 3 + x[17:35] * 7 + x[35:54] * 9

recept.fillna(0)

#2
engine = create_engine("sqlite://")

hleb.to_sql("Хлеб", con = engine)
tip_prod.to_sql("Тип_продукта", con = engine)
ingredients.to_sql("Ингридиенты", con = engine)
recept.to_sql("Рецепты", con = engine)

pd.read_sql_table("Хлеб", engine)

"""#1.	Библиотека XLWings. Основные возможности.

XLWings – это библиотека языка Python для работы с файлами xlsx. Её отличие от простого чтения эксель файлов в том, что она позволяет вносить формулы, читать данные из конкретных диапазонов, изменять формат и разметку файла, добавлять макросы и много другое.

# 2.	Соединение с книгой Excel

import xlwings as xw
sheet = wb.sheets['Sheet1']

# 3.	Синтаксис XLWings. Active Objects. Full qualification. App context manager.

Active Objects: 
wb.sheets.active

Full qualification:
Суть полной квалификации в том, что можно использовать разные скобки, и это соответствует стандартам как Excel, так и Python:
xw.apps[763].books[0].sheets[0].range('A1')
xw.apps(10559).books(1).sheets(1).range('A1')
xw.apps[763].books['Book1'].sheets['Sheet1'].range('A1')
xw.apps(10559).books('Book1').sheets('Sheet1').range('A1')

App context manager:
Данная функция позволяет открывать и автоматически закрывать файл, используя стандартный синтаксис Python:
with xw.App() as app:
    book = app.books['Book1']

# 4.	Синтаксис XLWings. Range indexing/slicing. Range Shortcuts. Object Hierarchy.Range indexing/slicing

Объекты Range поддерживают стандартный синтаксис Python для срезов:
rng = xw.Book().sheets[0].range('A1:D5')
rng[0, 0]
rng[:, 3:]

Range Shortcuts:
Но также для срезов возможно использовать и синтаксис близкий к таковому в Excel, иначе говоря выбирать ячейки из диапазонов:
sheet['A1:B5']

Object Hierarchy:
Для того чтобы попасть от объекта App к объекту Range необходимо обращаться к каждому объекту последовательно, в соответствии с иерархией:
rng = xw.apps[10559].books[0].sheets[0].range('A1')

# 5.	XLWings и Pandas.

Xlwings свободно взаимодействует с Pandas, т.к. можно считывать конкретные страницы из Excel файла, и их содержимое сразу же загружать в датафрейм, который намного более удобен и практичен в использовании. Xlwings позволяет свободно работать с Series, т.к. поддерживает все структуры данных Pandas.

sheet = xw.Book().sheets[0]
 df = pd.DataFrame([[1.1, 2.2], [3.3, None]], columns=['one', 'two'])
 df
 sheet.range('A1').value = df
 sheet.range('A1:C3').options(pd.DataFrame).value
'#options: work for reading and writing
sheet.range('A5').options(index=False).value = df
sheet.range('A9').options(index=False, header=False).value = df

# 6.	UDF.

UDF(User defined functions) – просто пользовательские функции, которые пользователь может создать при работе в xlwings. 

Настройки надстройки по умолчанию предполагают исходный файл Python в том виде, в котором он создается quickstart:
•	в том же каталоге, что и файл Excel
•	с тем же именем, что и файл Excel, но с .py окончанием вместо .xlsm.

Кроме того, можно указать на конкретный модуль через ленту xlwings.UDF Modules
Если есть рабочая книга myproject.xlsm, тогда необходимо написать следующий код myproject.py:
import xlwings as xw
@xw.func
def double_sum(x, y):
    '''Returns twice the sum of the two arguments'''
    return 2 * (x + y)
"""