from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import (ScreenplayAnalyserForm)
from uuid import uuid4
from werkzeug.utils import secure_filename
import subprocess
import requests
from app.lines import *
from app.visualiser import create_plots
import time



@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    form = ScreenplayAnalyserForm()
    plot_path1 = None
    plot_path2 = None
    poster = None
    title = None
    year = None
    released = None
    runtime = None
    box_office = None
    imdbRating = None
    imdbVotes = None
    OMDB_API_KEY = os.environ.get('OMDB_API_KEY')
    box_colour = "#d6d6d6"
    text_colour = "#000000"
    if form.validate_on_submit():
        unique_str = str(uuid4())
        filename = secure_filename(f'{unique_str}-{form.document.data.filename}')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.document.data.save(filepath)
        file = form.document.data
        character = form.character.data.strip().upper()
        api_data = get_movie_data(form.title.data, OMDB_API_KEY)
        if api_data:
            title = api_data.get('Title')
            year = api_data.get('Year')
            released = api_data.get('Released')
            runtime = api_data.get('Rumtime')
            poster = api_data.get('Poster')
            box_office = api_data.get('BoxOffice')
            imdbRating = api_data.get('imdbRating')
            imdbVotes = api_data.get('imdbVotes')
            box_colour, text_colour = genre_colour(api_data.get('Genre').split(",")[0])
        try:
            capture_dialogue(file, character, app)
            script_path = os.path.join(app.root_path, "sentiment_analysis.R")
            print(script_path)
            subprocess.run(["Rscript", script_path])
            plot_path1 = create_plots()
            data_folder = os.path.join(app.root_path, 'static', 'images')
            plot_path2 = os.path.join(data_folder, 'sentiment_valence_plot.png')
            flash(f"Sentiment analysis complete! Find your plots and facts about the movie below! Click on "
                  f"the plots to enlarge them in a new tab!","success")
        except Exception as error:
            print("An error has occurred, please try again.", error)
            flash(f"There was a problem with your file. Please ensure it is in the correct format", "danger")
        finally:
            os.remove(os.path.join(app.config['DATA_FOLDER'], "sentiment_analysis.csv"))
            os.remove(os.path.join(app.config['DATA_FOLDER'], "cleaned_lines.txt"))
            os.remove(filepath)
    return render_template('index.html', form=form, title="Screenplay Sentiment Analyser", plot1 = plot_path1, plot2 = plot_path2,
                           mtitle=title, year=year, released=released, runtime=runtime, poster=poster, box_office=box_office,
                           imdbRating=imdbRating, imdbVotes=imdbVotes, box_colour=box_colour,text_colour=text_colour)

def genre_colour(genre):
    genre = genre.lower()
    genre_colors = {
        "action": ("#E0E8F3", "#333333"),
        "sci-fi": ("#F5F5F5", "#1A237E"),
        "horror": ("#FFF9C4", "#2E7D32"),
        "drama": ("#FCE4EC", "#3E2723"),
        "comedy": ("#C8E6C9", "#004D40"),
        "western": ("#E1BEE7", "#4A148C"),
        "biography": ("#FFFDE7", "#4E342E"),
        "crime": ("#607D8B", "#333333")
    }
    return genre_colors.get(genre, ("#d6d6d6", "#000000"))  # Default colors

def get_movie_data(movie_name, api_key):
    api_url = f'http://www.omdbapi.com/?apikey={api_key}&t={movie_name}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html'), 413

@app.errorhandler(400)
def error_400(error):
    return render_template('errors/400.html'), 400

@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404