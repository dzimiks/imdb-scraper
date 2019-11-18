import requests
import json
import re
from bs4 import BeautifulSoup

if __name__ == '__main__':
    movies = []
    successful = 0
    MAIN_URL = 'https://www.imdb.com'

    for i in range(1, 2, 100):
        URL = f'https://www.imdb.com/search/title/?title_type=feature,tv_series&count=100&start={i}&ref_=adv_nxt'
        page = requests.get(URL).text
        soup = BeautifulSoup(page, features='lxml')
        soup.prettify()

        test = [re.sub(r'<[^>]*>', '', item[0]).strip() for item in re.findall(r'Stars:((.|\n)*?)</a>', page)]
        test2 = re.findall(r'Stars:((.|\n)*?)</a>', page)
        print(test)
        print(test2)

        all_movies = soup.find_all('div', 'lister-item mode-advanced')

        for movie in all_movies:
            item_content = movie.find('div', 'lister-item-content')
            item_header = item_content.find('h3', 'lister-item-header').text
            item_header_split = list(filter(None, item_header.split('\n')))
            item_subtitle = [item.text for item in item_content.find_all('p')]

            url = MAIN_URL + item_content.find('h3', 'lister-item-header').find('a').get('href')
            # print('url:', url)

            item_content_trimmed = re.sub(r'\n+', r'\n', item_content.text)
            item_content_trimmed = re.sub(r' +', ' ', item_content_trimmed)

            # certificate = item_subtitle[0].find('span', 'certificate')
            # duration = item_subtitle[0].find('span', 'runtime')
            # genre = item_subtitle[0].find('span', 'genre')

            # rating = item_content.find('div', 'ratings-imdb-rating')
            # bio = item_subtitle[1].text.strip()
            # director = item_subtitle[2].text.strip()
            # stars = item_subtitle[2].text.strip()
            # votes = item_subtitle

            movie = {
                'header': item_header,
                'item_subtitle': item_subtitle,
                'len': len(item_subtitle),
                'item_content_trimmed': item_content_trimmed
                # 'bio': bio,
                # 'director': director,
                # 'stars': stars,
                # 'votes': votes
            }

            movies.append(movie)
            successful += 1
            # print(json.dumps(movie, default=str, indent=4))

    print('Successfully found:', successful)
    # with open('data.json', 'w', encoding='utf-8') as f:
    #     json.dump(movies, f, ensure_ascii=False, indent=4)
