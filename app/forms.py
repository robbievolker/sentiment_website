from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError

class ScreenplayAnalyserForm(FlaskForm):
    document = FileField('Screenplay To Analyse', validators=[FileAllowed(['docx', 'doc', 'otd'])])
    character = StringField('Character To Analyse', validators=[DataRequired()])
    submit = SubmitField('Submit')