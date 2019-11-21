import requests
import json
import re
from bs4 import BeautifulSoup

if __name__ == '__main__':
    movies = []
    successful = 0
    MAIN_URL = 'https://www.imdb.com'

    for i in range(1, 302, 100):
        URL = f'https://www.imdb.com/search/title/?title_type=feature,tv_series&count=100&start={i}&ref_=adv_nxt'
        page = requests.get(URL).text
        soup = BeautifulSoup(page, features='lxml')
        soup.prettify()

        all_movies = soup.find_all('div', 'lister-item mode-advanced')
        j = 0

        for movie in all_movies:
            item_content = movie.find('div', 'lister-item-content')
            item_header = item_content.find('h3', 'lister-item-header').text
            item_header_split = list(filter(None, item_header.split('\n')))
            item_subtitle = [item.text.strip() for item in item_content.find_all('p')]
            item_subtitle = [item.split('|') for item in item_subtitle]

            item_subtitle_len = len(item_subtitle)
            duration_and_genre = None
            bio = None
            director_and_stars = None
            votes = None

            if item_subtitle_len == 4:
                duration_and_genre = [item.strip() for item in item_subtitle[0]]
                bio = item_subtitle[1][0].strip()
                director_and_stars = [item.strip() for item in item_subtitle[2]]
                votes = [item.strip() for item in item_subtitle[3]]

            # certificate = item_subtitle[0].find('span', 'certificate')
            # duration = item_subtitle[0].find('span', 'runtime')
            # genre = item_subtitle[0].find('span', 'genre')

            # rating = item_content.find('div', 'ratings-imdb-rating')
            # bio = item_subtitle[1].text.strip()
            # director = item_subtitle[2].text.strip()
            # stars = item_subtitle[2].text.strip()
            # votes = item_subtitle

            movie = {
                'header': item_header_split,
                'item_subtitle': item_subtitle,
                'duration_and_genre': duration_and_genre,
                'bio': bio,
                'director_and_stars': director_and_stars,
                'votes': votes
            }

            movies.append(movie)
            successful += 1
            # print(json.dumps(movie, default=str, indent=4))

            # if j == 2:
            #     break

            j += 1

    print('Successfully found:', successful)

    with open('data.json', 'w+', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)
