import requests
import string
import os
from bs4 import BeautifulSoup

print("How many pages of 'Nature' should I scrape?")
pages = int(input("> "))
print("What type of articles do you want to save?")
art_type = input("> ")
print()

for n in range(1, pages + 1):
    folder = 'Page_' + str(n)
    os.mkdir(folder)
    url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=' + str(n)

    response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(response.content, 'html.parser')

    all_articles = soup.find_all('article')
    news_articles = []

    for art in all_articles:
        if art.find('span', {'class': 'c-meta__type'}).text == art_type:
            news_articles.append({'title': art.find('h3').text,
                                  'link': 'https://www.nature.com' +
                                          art.find('a').get('href')})

    for art in news_articles:
        strip_title = art['title'].strip('\n')
        filename = ""
        for letter in strip_title:
            if letter in string.whitespace:
                filename += "_"
            elif letter not in string.punctuation:
                filename += letter
        art['filename'] = filename + ".txt"

    for art in news_articles:
        file = open(os.path.join(folder, art['filename']), 'wt', encoding='utf-8')
        response2 = requests.get(art['link'])
        soup2 = BeautifulSoup(response2.content, 'html.parser')

        file.write(soup2.find('div', {'class': 'c-article-body main-content'}).get_text().strip())
        file.close()
        print("Saved an article to '" + folder + "\\" + art['filename'] + "'")
