import requests
from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.utils import redirect
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap5(app)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Movie(db.Model):
    id = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float)
    ranking: Mapped[int] = mapped_column(Integer)
    review: Mapped[str] = mapped_column(String(250))
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.init_app(app)
    db.create_all()

class MovieForm(FlaskForm):
    rating = StringField('Rating', validators=[DataRequired()])
    review = StringField('Review', validators=[DataRequired()])
    submit = SubmitField('Update')

class AddMovie(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')

API_KEY = ("Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlYTZlNjhjNDlmYWZiNGUwNmY4Mjk0ZDg1ZmRiODcxZSIsIm"
           "5iZiI6MTczNzAyNDk1My40NDMsInN1YiI6IjY3ODhlNWI5MTQwMzcwMWM5OTFkNDZhMyIsInNjb3BlcyI6WyJhc"
           "GlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.JexIcvnrXFn9oBFl0j89FUGwnsecHZjhCOx151FGEQU")

headers = {
    "accept": "application/json",
    "Authorization": API_KEY
}

@app.route("/")
def home():
    movies = list(db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars())

    for index, movie in enumerate(reversed(movies), start=1):
        movie.ranking = index

    db.session.commit()

    return render_template("index.html", movies=movies)

@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddMovie()
    if form.validate_on_submit():
        query = form.title.data
        url = f"https://api.themoviedb.org/3/search/movie?query={query}&include_adult=false&language=en-US&page=1"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            movie_data = response.json()["results"]
            return render_template("select.html", movies=movie_data)
    return render_template("add.html", form=form)

@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"https://api.themoviedb.org/3/movie/{movie_api_id}"
        response = requests.get(movie_api_url, params={"api_key": 'ea6e68c49fafb4e06f8294d85fdb871e', "language": "en-US"})
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            img_url=f"https://image.tmdb.org/t/p/w500{data['poster_path']}",
            description=data["overview"],
            rating=0,
            ranking="None",
            review="None"
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("edit", movie_id=new_movie.id))

@app.route("/edit", methods=["GET", "POST"])
def edit():
    movie_id = request.args.get("movie_id")

    movie_to_update = db.get_or_404(Movie, movie_id)
    form = MovieForm()

    if request.method == "POST" and form.validate_on_submit():
        movie_to_update.rating = form.rating.data
        movie_to_update.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", form=form, movie=movie_to_update)

@app.route("/delete")
def delete():
    movie_id = request.args.get('id')
    book_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)