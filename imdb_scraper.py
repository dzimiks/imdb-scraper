import requests
import json
import re
from bs4 import BeautifulSoup

if __name__ == '__main__':
    movies = []
    successful = 0

    for i in range(1, 300, 100):
        URL = f'https://www.imdb.com/search/title/?title_type=feature,tv_series&count=100&start={i}&ref_=adv_nxt'
        page = requests.get(URL).text
        soup = BeautifulSoup(page, features='lxml')
        soup.prettify()

        all_movies = soup.find_all('div', 'lister-item mode-advanced')

        for movie in all_movies:
            try:
                item_content = movie.find('div', 'lister-item-content')
                item_header = item_content.find('h3', 'lister-item-header').text
                item_header_split = list(filter(None, item_header.split('\n')))
                p_tags = item_content.find_all('p')
                certificate = p_tags[0].find('span', 'certificate')
                duration = p_tags[0].find('span', 'runtime')
                genre = p_tags[0].find('span', 'genre')
                rating = item_content.find('div', 'ratings-imdb-rating').get('data-value')
                bio = p_tags[1].text.strip()
                director = p_tags[2].text.strip().replace('\n', '').split('|')[0].split(':')[1]
                stars = p_tags[2].text.strip().replace('\n', '').split('|')[1].split(':')[1]
                votes = re.findall('\d+', p_tags[3].text.replace('\n', '').split(':')[1].replace(',', ''))[0]

                movie = {
                    'header': {
                        'index': item_header_split[0],
                        'title': item_header_split[1],
                        'year': item_header_split[2]
                    },
                    'item_subtitle': {
                        'certificate': certificate,
                        'duration': duration,
                        'genre': genre
                    },
                    'rating': rating,
                    'bio': bio,
                    'director': director,
                    'stars': stars,
                    'votes': votes
                }

                movies.append(movie)
                successful += 1
                # print(json.dumps(movie, default=str, indent=4))
            except (AttributeError, IndexError) as e:
                print('>>> ERROR:', e)

    print('Successfully found:', successful)
    # with open('data.json', 'w', encoding='utf-8') as f:
    #     json.dump(movies, f, ensure_ascii=False, indent=4)
