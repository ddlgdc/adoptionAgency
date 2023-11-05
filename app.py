from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adopt.db' 
app.config['SECRET_KEY'] = 'SECRETKEY'
db = SQLAlchemy(app)

class AddPetForm(FlaskForm):
    name = StringField('Pet Name', validators=[DataRequired()])
    species = StringField('Species', validators=[DataRequired()])
    photo_url = StringField('Photo URL', validators=[URL()])
    age = IntegerField('Age')
    notes = TextAreaField('Notes')
    available = BooleanField('Available')

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    species = db.Column(db.String(80), nullable=False)
    photo_url = db.Column(db.String(200))
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, default=True)

def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()

@app.route('/')
def index():
    pets = Pet.query.all()
    return render_template('index.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    form = AddPetForm()
    if form.validate_on_submit():
        new_pet = Pet(
            name=form.name.data,
            species=form.species.data,
            photo_url=form.photo_url.data,
            age=form.age.data,
            notes=form.notes.data,
            available=form.available.data 
        )
        db.session.add(new_pet)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_pet.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, port=0)