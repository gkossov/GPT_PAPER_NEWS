#from langchain.embeddings import HuggingFaceEmbeddings
#from langchain.retrievers import BM25Retriever, EnsembleRetriever
#from langchain.vectorstores.faiss import FAISS
#from langchain_core.documents import Document
#from langchain_community.document_loaders import WebBaseLoader
#from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
#from IPython.display import display, Markdown
import requests
import uuid
import json
import urllib.request
import time
#import feedparser
from datetime import datetime
import random
import json
import requests
import datetime
from fake_useragent import UserAgent

client_id = "2e9a46c7-cc72-4a36-9626-c3c6f0636b52"
secret = "cdfe542d-6089-490c-b6d6-6ed7a87fd43c"
auth = "MmU5YTQ2YzctY2M3Mi00YTM2LTk2MjYtYzNjNmYwNjM2YjUyOmNkZmU1NDJkLTYwODktNDkwYy1iNmQ2LTZlZDdhODdmZDQzYw=="
'''
def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    """
      Выполняет POST-запрос к эндпоинту, который выдает токен.

      Параметры:
      - auth_token (str): токен авторизации, необходимый для запроса.
      - область (str): область действия запроса API. По умолчанию — «GIGACHAT_API_PERS».

      Возвращает:
      - ответ API, где токен и срок его "годности".
      """
    # Создадим идентификатор UUID (36 знаков)
    rq_uid = str(uuid.uuid4())

    # API URL
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    # Заголовки
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }

    # Тело запроса
    payload = {
        'scope': scope
    }

    try:
        # Делаем POST запрос с отключенной SSL верификацией
        # (можно скачать сертификаты Минцифры, тогда отключать проверку не надо)
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1
    
response = get_token(auth)

if response != 1:
  #print(response.text)
  giga_token = response.json()['access_token']

def get_chat_completion(auth_token, user_message):
    """
    Отправляет POST-запрос к API чата для получения ответа от модели GigaChat.

    Параметры:
    - auth_token (str): Токен для авторизации в API.
    - user_message (str): Сообщение от пользователя, для которого нужно получить ответ.

    Возвращает:
    - str: Ответ от API в виде текстовой строки.
    """
    # URL API, к которому мы обращаемся
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    # Подготовка данных запроса в формате JSON
    payload = json.dumps({
        "model": "GigaChat",  # Используемая модель
        "messages": [
            {
                "role": "user",  # Роль отправителя (пользователь)
                "content": user_message  # Содержание сообщения
            }
        ],
        "temperature": 1,  # Температура генерации
        "top_p": 0.1,  # Параметр top_p для контроля разнообразия ответов
        "n": 1,  # Количество возвращаемых ответов
        "stream": False,  # Потоковая ли передача ответов
        "max_tokens": 512,  # Максимальное количество токенов в ответе
        "repetition_penalty": 1,  # Штраф за повторения
        "update_interval": 0  # Интервал обновления (для потоковой передачи)
    })

    # Заголовки запроса
    headers = {
        'Content-Type': 'application/json',  # Тип содержимого - JSON
        'Accept': 'application/json',  # Принимаем ответ в формате JSON
        'Authorization': f'Bearer {auth_token}'  # Токен авторизации
    }

    # Выполнение POST-запроса и возвращение ответа
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        # Обработка исключения в случае ошибки запроса
        print(f"Произошла ошибка: {str(e)}")
        return -1
    '''
def arxiv_parser(query, date):
    base_url = 'http://export.arxiv.org/api/query?'
    # Search parameters
    search_query = urllib.parse.quote(query)
    i = 0
    results_per_iteration = 1
    papers = []
    date_reach = date
    year = date_reach
    print('Searching arXiv for %s' % search_query)
    while (year >= date_reach): #stop requesting when papers date reach 2018
        #print("Results %i - %i" % (i,i+results_per_iteration))
        query = 'search_query=%s&start=%i&max_results=%i&sortBy=submittedDate&sortOrder=descending' % (search_query,
                                                             i,
                                                             results_per_iteration)
        # perform a GET request using the base_url and query
        response = urllib.request.urlopen(base_url+query).read()
        # parse the response using feedparser
        feed = feedparser.parse(response)
        # Run through each entry, and print out information
        for entry in feed.entries:
            #print('arxiv-id: %s' % entry.id.split('/abs/')[-1])
            #print('Title:  %s' % entry.title)
            #feedparser v4.1 only grabs the first author
            #print('First Author:  %s' % entry.author)
            year = datetime.strptime(entry.published.split('T')[0], "%Y-%m-%d")
            if year >= date_reach:
                paper = {}
                paper["date"] = entry.published
                paper["title"] = entry.title
                paper["first_author"] = entry.author
                for link in entry.links:
                    if link.rel == "alternate":
                        paper["pdf link"] =  link.href
                    elif link.title == "pdf":
                        paper["pdf link"] =  link.href
                paper["summary"] = entry.summary
                papers.append(paper)
        # Sleep a bit before calling the API again
        #print('Bulk: %i' % 1)
        i += results_per_iteration
        #time.sleep(wait_time)
    return papers


def habr_parser():
    ua = UserAgent()
    headers = {
        'accept': 'application/json, text/plain, */*',
        'user-Agent': ua.google,
    }

    article_dict = {}

    pages = ["page1", "page2", "page3", "page4", "page5", "page6", "page7", "page8", "page9", "page10", "page11", "page12", "page13"]

    for page in pages:
        url = f'https://habr.com/ru/top/daily/'+page

        req = requests.get(url, headers=headers).text

        soup = BeautifulSoup(req, 'lxml')
        all_hrefs_articles = soup.find_all('a', class_='tm-title__link') # получаем статьи

        for article in all_hrefs_articles: # проходимся по статьям
            article_name = article.find('span').text # собираем названия статей
            article_link = f'https://habr.com{article.get("href")}' # ссылки на статьи
            article_dict[article_name] = article_link

    print('Статьи были успешно получены')
    
    #with open(f"articles_{datetime.datetime.now().strftime('%d_%m_%Y')}.json", "w", encoding='utf-8') as f: 
    #    try:    
    #        json.dump(article_dict, f, indent=4, ensure_ascii=False)
    #    except:
    #        print('Статьи не удалось получить')
    return article_dict