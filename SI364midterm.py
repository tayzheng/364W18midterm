###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
import json
import requests
import app_key_id

# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required # Here, too
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell

## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

## All app.config values
app.config['SECRET_KEY'] = 'hardtoguessstringfromsi364thisisnotsupersecurebutitsok'
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/songs_db_2"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:siyi1126@localhost/si364midterm"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up Flask debug stuff
manager = Manager(app)

## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)


######################################
######## HELPER FXNS (If any) ########
######################################

# API_KEY = app_key_id.API_KEY
# APP_ID = app_key_id.APP_ID

def get_or_create_user(user):

    user = Names.query.filter_by(name = user).first()

    if user:
        flash('Sorry this user already exists.')
        return user

    else:
        user = Names(name = user)
        db.session.add(user)
        db.session.commit()
        flash('User successfully addd!')
        return user

#movie title
def get_or_create_titles(db_session, movie_name):

    title = db.session.query(Title).filter_by(title=title_name).first()

    if title:
        flash('Sorry this title already exists.')
        return redirect(url_for('all_titles'))
        
    else:
        title = Title(title=title_name)
        db.session.add(title)
        db.session.commit()
        flash('Title successfuly added!')
        return redirect(url_for('index'))
        

##################
##### MODELS #####
##################

class Name(db.Model):
    __tablename__ = "names"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})".format(self.name, self.id)

class Title(db.Model):
    __tablename__ = "titles"
    title = db.Column(db.String(64))
    id = db.Column(db.String(64), primary_key = True) #series of letters and numbers

    def __repr__(self):
        return "{} (ID: {})".format(self.title, self.id)

class Review(db.Model):
    __tablename__ = "review"
    id = db.Column(db.String(64), primary_key = True)
    review = db.Column(db.String(280))
    rating = db.Column(db.Integer)

    def __repr__(self):
        return "Review: {} | (ID: {})".format(self.review, self.id)


###################
###### FORMS ######
###################

class NameForm(FlaskForm):
    name = StringField("Please enter your name.",validators=[Required()])
    submit = SubmitField()

    def validate_name(self, field):
        if len(field.data.split()) < 1:
            raise ValidationError('Name was not entered. Please try again.')

class MovieForm(FlaskForm)::
    movie = StringField('Please enter a movie title.', validators=[Required(), Length(min = 1, max = 280)])
    review = StringField('Please write a reivew for the movie. What did you think!', validators=[Required()])
    submit = SubmitField('Submit')


#######################
###### VIEW FXNS ######
#######################

@app.route('/')
def index():
    form = NameForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET
    if form.validate_on_submit():
        name = form.name.data
        newname = Name(name)
        db.session.add(newname)
        db.session.commit()
        return redirect(url_for('all_names'))
    return render_template('index.html',form=form)

@app.route('/names')
def all_names():
    names = Name.query.all()
    return render_template('index.html',names=names)


##error handlers ---------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

##custom view functions --------------------------
@app.route('/all_movies', methods = ['GET'])
def all_titles():
    # form = TitleForm()
    # if request.method == 'GET':
    #     result = request.args['title']
    #     url = request.get('http://www.omdbapi.com/?i=tt3896198&apikey=e8f22500'+result).json
    # return render_template('all_movies.html', titles = Title.query.all())
    response = requests.get('http://www.omdbapi.com/?i=tt3896198&apikey=e8f22500')
    return response.text

@app.route('/movie_form', methods=['GET', 'POST'])
def movie_form():
    form = MovieForm(request.form)
    if form.validate_on_submit():
    movie = form.movie.data
        review = form.review.data
        m = Movie.query.filter_by(movieName=movie).first()
        if m:
            print("Breed exists")
        else:
            m = Movie(breedName=movie)
            db.session.add(m)
            db.session.commit()

        r = Review.query.filter_by(review=review,movie_id=b.ID).first()
        if r:
            print("Review exsits")
            return redirect(url_for('see_all_reviews'))
        else:
            r = Tweet(review=review,breed_id=b.ID)
            db.session.add(r)
            db.session.commit()
            return redirect(url_for('index'))
    
    return render_template("index.html", form = form)

@app.route('/favorite_movie', methods = ['GET', 'POST'])
def movies():
    form = MovieForm(request.form)
    if request.args:
        fav = request.args.get('movie').title()
        review = request.args.get('review')
        m = Title(movie = fav, review = review)
        db.session.add()
        db.session.commit()
        return render_template('movie_reviews.html', fav = fav, review = review)
    flask(form.errors)
    return redirect(url_for(movie_form))

@app.route('/all_reviews')
def all_reviews():
    reviews = Review.query.all()
    Review = [(r, Review.query,filter_by(ID.r.id).first()) for r in reviews]
    return render_template('all_reviews.html', reviews = reviews)


## Code to run the application...
if __name__ == '__main__':
    db.create_all()
    app.run(use_reloader=True, debug=True)

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
