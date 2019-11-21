import requests
import json
from bs4 import BeautifulSoup

if __name__ == '__main__':
    movies = []
    successful = 0
    MAIN_URL = 'https://www.imdb.com'

    # TODO: Retrieve 11100 movies
    for i in range(1, 11002, 100):
        URL = f'https://www.imdb.com/search/title/?title_type=feature,tv_series&count=100&start={i}&ref_=adv_nxt'
        page = requests.get(URL).text
        soup = BeautifulSoup(page, features='lxml')
        soup.prettify()

        all_movies = soup.find_all('div', 'lister-item mode-advanced')
        # j = 0

        for movie in all_movies:
            item_content = movie.find('div', 'lister-item-content')
            item_header = item_content.find('h3', 'lister-item-header').text
            item_header_split = list(filter(None, item_header.split('\n')))
            item_subtitle = [item.text.strip() for item in item_content.find_all('p')]
            item_subtitle = [item.split('|') for item in item_subtitle]

            # TODO: 257. After we Collided without movie year
            item_header_split_len = len(item_header_split)
            movie_id = None
            movie_title = None
            movie_year = None

            if item_header_split_len == 3:
                movie_id = item_header_split[0]
                movie_title = item_header_split[1]
                movie_year = item_header_split[2]
            elif item_header_split_len == 2:
                movie_id = item_header_split[0]
                movie_title = item_header_split[1]

            # Movie part is in year
            if movie_year is not None and ') (' in movie_year:
                movie_title += ' ' + item_header_split[2].split(' ')[0]
                movie_year = item_header_split[2].split(' ')[1]

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
            elif item_subtitle_len == 3:
                duration_and_genre = [item.strip() for item in item_subtitle[0]]
                bio = item_subtitle[1][0].strip()
                director_and_stars = [item.strip() for item in item_subtitle[2]]

            if votes is not None:
                votes = votes[0].replace('Votes:', '').strip()

            duration_and_genre_len = len(duration_and_genre)
            certificate = None
            duration = None
            genre = None

            if duration_and_genre_len == 3 or duration_and_genre_len == 4:
                # Post production
                if duration_and_genre[0][0].isdigit():
                    duration = duration_and_genre[0]
                    genre = duration_and_genre[1]
                else:
                    certificate = duration_and_genre[0]
                    duration = duration_and_genre[1]
                    genre = duration_and_genre[2]
            elif duration_and_genre_len == 2:
                # Movie number 8th - post production
                if duration_and_genre[0][0].isdigit():
                    duration = duration_and_genre[0]
                    genre = duration_and_genre[1]
                else:
                    genre = duration_and_genre[0]
            elif duration_and_genre_len == 1:
                genre = duration_and_genre[0]

            director_and_stars_len = len(director_and_stars)
            director = None
            stars = None

            if director_and_stars_len == 2:
                director = director_and_stars[0]
                stars = director_and_stars[1]
            elif director_and_stars_len == 1:
                stars = director_and_stars[0]

            # TODO cleanup
            if director is not None:
                director = director.replace('Director:', '').replace('\n', '').strip()

            if stars is not None:
                stars = stars.replace('Stars:', '').replace('\n', '')
                stars = [item.strip() for item in stars.split(',')]

            rating = item_content.find('div', 'ratings-imdb-rating')

            if rating is not None:
                rating = rating.text.strip()

            movie = {
                # 'header': item_header_split,
                'movie_id': movie_id,
                'movie_title': movie_title,
                'movie_year': movie_year,
                # 'item_subtitle': item_subtitle,
                # 'duration_and_genre': duration_and_genre,
                'rating': rating,
                'bio': bio,
                # 'director_and_stars': director_and_stars,
                'director': director,
                'stars': stars,
                'votes': votes,
                'certificate': certificate,
                'duration': duration,
                'genre': genre
            }

            movies.append(movie)
            successful += 1
            # print(json.dumps(movie, default=str, indent=4))

            # if j == 2:
            #     break

            # j += 1

    print('Successfully found:', successful)

    with open('data.json', 'w+', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)
