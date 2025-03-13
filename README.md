# Top Movies (Made with Flask)

This repository contains a movie review web application built with Flask. The app allows users to:

- View a list of movies with their ratings and reviews.
- Add a movie to the database by searching for it via The Movie Database (TMDb) API.
- Edit a movie's rating and review.
- Delete movies from the list.

## Features

- **Home Page**: Displays a list of movies, sorted by rating.
- **Add Movie**: Search for movies by title using The Movie Database API.
- **Edit Movie**: Update a movie's rating and review.
- **Delete Movie**: Remove a movie from the list.

## Tech Stack

- **Backend**: Flask
- **Database**: SQLite with SQLAlchemy
- **Form Handling**: Flask-WTF
- **API**: The Movie Database (TMDb) API
- **Bootstrap**: Bootstrap5 for front-end styling

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/top-movies.git
   cd top-movies
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**: The database is initialized automatically when you run the app for the first time. No manual setup is required.

## Running the App

To run the Flask app locally, use the following command:

```bash
python main.py
```

Once the app is running, visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser to start interacting with it.

## Requirements

- Python 3.x
- Flask
- Flask-WTF
- Flask-SQLAlchemy
- requests
- werkzeug
- flask-bootstrap

You can install all required dependencies using the following:

```bash
pip install -r requirements.txt
```

## Routes

- **`/`**: Home page displaying the list of movies.
- **`/add`**: Search and add a new movie to the list.
- **`/find`**: Fetch a movie by its ID from The Movie Database API.
- **`/edit`**: Edit a movie's rating and review.
- **`/delete`**: Delete a movie from the list.

## License

This project is licensed under the MIT License.

## Requirements.txt

```txt
Flask==2.2.2
Flask-SQLAlchemy==2.5.1
Flask-WTF==1.0.1
Flask-Bootstrap==3.3.7.1
requests==2.28.1
werkzeug==2.2.2
```
---

Feel free to contribute, suggest improvements, or ask questions by opening an issue in this repository.
```
