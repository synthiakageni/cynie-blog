from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import InputRequired

class BlogForm(FlaskForm):

    title = StringField('blog title',validators=[InputRequired()])
    text = TextAreaField('Text',validators=[InputRequired()])
    category = SelectField('Type',choices=[('science','Science blog'),('anaconda','Anaconda blog'),('alien','Alien blog'), ('birds', 'Birds blog'), ('culture', 'poetry')],validators=[InputRequired()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Bio.',validators = [InputRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    text = TextAreaField('Leave a comment:',validators=[InputRequired()])
    submit = SubmitField('Submit')
