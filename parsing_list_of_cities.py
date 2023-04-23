import requests    # by Kirill Kasparov, 2022
from bs4 import BeautifulSoup
import pandas as pd

# requests нужен для копирования html кода
url = 'https://ru.wikipedia.org/wiki/Список_городов_России' # url страницы
r = requests.get(url)

# BeautifulSoup нужен для обработки полученной страницы
soup = BeautifulSoup(r.content, 'html.parser')    # передаем данные в BeautifulSoup, response.content - исходный код
title = soup.title    # получаем заголовок сайта


# собираем колонки
col_tab = soup.find_all('th', scope="col")    # ищем конкретные элементы с конкретным классом
colum_for_df = []
for col in col_tab:
    colum_for_df.append(col.text)

# собираем строки
tables = soup.find_all('table')    # Получаем таблицы
table_for_df = []
for table in tables:
    tr_tags = table.find_all('tr')
    for tr in tr_tags:
        tr_list = []    # наши строки
        td_tags = tr.find_all('td')
        for td in td_tags:
            tr_list.append(td.string)    # элементы строк
        if len(tr_list) == 9:    # фильтруем мусор, количество ячеек посчитали вручную
            table_for_df.append(tr_list)    # собираем вместе

# собираем DataFrame
df = pd.DataFrame(table_for_df, columns=colum_for_df[:9])

# сохраняем таблицу
data_export = 'list_of_cities.csv'
df.to_csv(data_export, sep=';', encoding='windows-1251', index=False, mode='w')

print('Список городов сохранен в файл list_of_cities.csv')