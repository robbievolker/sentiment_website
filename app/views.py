from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import (ScreenplayAnalyserForm)
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from uuid import uuid4
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
import subprocess
from app.lines import *

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    form = ScreenplayAnalyserForm()
    if form.validate_on_submit():
        unique_str = str(uuid4())
        filename = secure_filename(f'{unique_str}-{form.document.data.filename}')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.document.data.save(filepath)
        file = form.document.data
        character = form.character.data.strip().upper()
        try:
            capture_dialogue(file, character, app)
            script_path = os.path.join(os.path.dirname(__file__), "sentiment_analysis_2.R")
            subprocess.run(["Rscript", script_path])
            flash(f"Character lines created!", "success")
        except Exception as error:
            print("An error has occurred, please try again.", error)
            flash(f"There was a problem with your file. Please ensure it is in the correct format", "danger")
    return render_template('index.html', form=form, title="Screenplay Sentiment Analyser")

# Handler for 413 Error: "RequestEntityTooLarge". This error is caused by a file upload
# exceeding its permitted Capacity
# Note, you should add handlers for:
# 403 Forbidden
# 404 Not Found
# 500 Internal Server Error
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html'), 413
