import requests                                                                  # Модуль для обработки URL
from bs4 import BeautifulSoup                                                    # Модуль для работы с HTML
                                                        
Dol_Rub = 'https://www.google.com/search?sxsrf=ALeKk01NWm6viYijAo3HXYOEQUyDEDtFEw%3A1584716087546&source=hp&ei=N9l0XtDXHs716QTcuaXoAg&q=доллар+к+рублю&oq=доллар+&gs_l=psy-ab.3.0.35i39i70i258j0i131l4j0j0i131l4.3044.4178..5294...1.0..0.83.544.7......0....1..gws-wiz.......35i39.5QL6Ev1Kfk4'    #ссылка
Eur_Rub = 'https://www.google.com/search?q=евро+к+рублю&ei=rlZ6YpLQD833qwHV4avICQ&ved=0ahUKEwiS35Hp89T3AhXN-yoKHdXwCpkQ4dUDCA4&uact=5&oq=евро+к+рублю&gs_lcp=Cgdnd3Mtd2l6EAMyDQgAEIAEELEDEEYQggIyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BwgAEEcQsAM6CggAEEcQsAMQyQM6BwgAELADEEM6BggAEAcQHjoHCAAQsQMQQzoICAAQBxAKEB46BAgAEA1KBAhBGABKBAhGGABQngJY_w9guBNoAXABeACAAYoBiAHeBpIBAzguMpgBAKABAcgBCsABAQ&sclient=gws-wiz'
headers = {'Users-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 Safari/537.36'}                      #заголовки, описывающие пользователя

def check_dollar():
    full_page = requests.get(Dol_Rub, headers=headers)                           #запарсили всю htlm-страницу в данную переменную
    soup = BeautifulSoup(full_page.content, 'html.parser')                       #разбираем страницу с помощью библиотеки(нужны только необходимые цифирки)
    convert = soup.findAll('div', {'class': 'BNeawe', 'class': 'iBp4i', 'class': 'AP7Wnd'}) #прописываем выборку элементов по нужным тегу и классам
    return convert[0].text                                                       #берем первый элемент из списка и возвращаем его содержимое

def check_euro():                                                                #разбираемся теперь с евро
    full_page = requests.get(Eur_Rub, headers=headers)                           #запарсили всю htlm-страницу в данную переменную
    soup = BeautifulSoup(full_page.content, 'html.parser')                       #разбираем страницу с помощью библиотеки(нужны только необходимые цифирки)
    convert = soup.findAll('div', {'class': 'BNeawe', 'class': 'iBp4i', 'class': 'AP7Wnd'}) #прописываем выборку элементов по нужным тегу и классам
    return convert[0].text     