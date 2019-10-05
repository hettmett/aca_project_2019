from flask import Flask, render_template, request
from db import db
import math

PAGE_SIZE = 10

app = Flask(__name__)


@app.route('/')
@app.route('/home', methods=["GET", "POST"])
def home():
    # get paging parameter from GET string
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    # set detault to 1 if page is less than 1
    if page < 1:
        page = 1

    cursor = db().cursor()

    sql = ("SELECT DISTINCT movie_imdb_rating.movie_id, COUNT(*) max_count "
           "FROM poster INNER JOIN movie_imdb_rating "
           "ON movie_imdb_rating.movie_id=poster.movie_id "
           "ORDER BY rating_wa DESC ")

    cursor.execute(sql)
    max_count = cursor.fetchone()['max_count']

    cursor.execute(
        "SELECT DISTINCT movie_imdb_rating.movie_id, poster.poster, "
        "poster.title, movie_imdb_rating.rating_wa "
        "FROM poster INNER JOIN movie_imdb_rating "
        "ON movie_imdb_rating.movie_id=poster.movie_id "
        "ORDER BY rating_wa DESC "
        "LIMIT {}, {}".format(
            (page - 1) * PAGE_SIZE, PAGE_SIZE)
    )

    page_count = math.ceil(max_count / PAGE_SIZE)

    return render_template('movie.html', movies=cursor, page_count=page_count,
                           page=page, page_size=PAGE_SIZE)


@app.route('/celebs')
def celebs():
    return render_template('celebs.html')


@app.route('/ratings')
def ratings():
    return render_template('ratings.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run('127.0.0.1', 8080, True)
