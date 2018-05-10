from typing import Set, Tuple, Iterable
from itertools import chain
from tabulate import tabulate
from math import isnan
import csv
import os
import subprocess
import pandas as pd

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CSV_DIR = os.path.join(BASE_DIR, 'anime-recommendations-csv')
FILE_BATCH_SIZE = 4


def line_count(path_to_file: str) -> int:
    return int(subprocess.check_output(f'wc -l < {path_to_file}', shell=True))


def split_file(path_to_file: str, num_lines: int) -> int:
    proc = subprocess.run(['split', '-l', f'{num_lines}', path_to_file])
    return int(proc.returncode)


def write_to_csv(csv_file: str,
                 heading: Tuple[str, ...],
                 rows: Iterable[Tuple[str, ...]]) -> None:
    with open(os.path.join(CSV_DIR, csv_file), 'w') as file:
        writer = csv.writer(file)
        writer.writerow(heading)

        for row in rows:
            writer.writerow(row)


def clean(string) -> str:
    # Handle NaN values returned by pandas
    if isinstance(string, float) and isnan(float(string)):
        return ''
    return str(string).strip()


def get_unique_genres(genre_df: pd.DataFrame) -> Set:
    return {
        clean(genre)
        for row in genre_df
        for genre in clean(row).split(',')
    }


def split_anime_genre(anime_id: str, genre: str) -> Iterable:
    genre_list = map(lambda g: clean(g), clean(genre).split(','))
    return map(lambda genre: (anime_id, genre), genre_list)


def prep_user_data(user_df: pd.DataFrame) -> None:
    unique_users = {user_id for user_id in user_df}

    user_ids = map(lambda id: (id, 'anonymous'), unique_users)

    write_to_csv('user.csv', ('user_id', 'name'), user_ids)


def prep_genre_data(genre_df: pd.DataFrame) -> None:
    # Remove empty string (nan) values
    genre_df.dropna(how='all', inplace=True)
    rows_of_genres = map(lambda genre: (genre,), get_unique_genres(genre_df))
    write_to_csv('genre.csv', ('name',), rows_of_genres)


def prep_anime_genre_data(anime_id_df: pd.DataFrame, genre_df: pd.DataFrame) -> None:
    zipped_df = zip(anime_id_df, genre_df)

    anime_id_genre = [
        split_anime_genre(anime_id, genre)
        for anime_id, genre in zipped_df
    ]

    write_to_csv('anime_genre.csv', ('anime_id', 'genre'), chain.from_iterable(anime_id_genre))


if __name__ == '__main__':
    anime_df = pd.read_csv(os.path.join(CSV_DIR, 'anime.csv'))
    user_rating_df = pd.read_csv(os.path.join(CSV_DIR, 'rating.csv'))

    prep_genre_data(anime_df['genre'])
    prep_anime_genre_data(anime_df['anime_id'], anime_df['genre'])
    prep_user_data(user_rating_df['user_id'])

    num_of_lines = int(round(line_count(os.path.join(CSV_DIR, 'rating.csv'))) / FILE_BATCH_SIZE)
    split_file(os.path.join(CSV_DIR, 'rating.csv'), num_of_lines)
