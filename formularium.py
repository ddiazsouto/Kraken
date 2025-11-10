from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, SelectField
from user import ListForm




class login_form(FlaskForm):

    login = StringField('Username: ')
    passwd= StringField('Password: ')
    submit= SubmitField('Log in')



class body_composition(FlaskForm):

    weight = StringField('Weight')
    fat_percentage = StringField('Fat percentage')
    muscle_percentage = StringField('Muscle percentage')
    visceral_fat = StringField('Visceral fat')
    details = StringField('Introduce client details ')
    add_metrics = SubmitField('Add Metrics ')


class deleting(FlaskForm):

    many=[]
    pairing=dict()

    action = SelectField('Action ', choices=[(1, 'View'), (2, 'Delete')])
    selection = SelectField('select ', choices = many)
    confirm = SubmitField('Confirm')


class add_gym_data_selection(FlaskForm):

    selection = SelectField('select ', choices=[('body_composition', 'Add in body composition')])
    pressa = SubmitField('Confirm')


class updating(FlaskForm):

    many=[('a', 1,), ('b', 2)]

    pairing=dict()

    listing=[('company_name', 'Company'), ('contact_name', 'Contact'), ('contact_surname', 'Surname'), ('phone', 'Phone'), ('details', 'Details')]

    edit = StringField('Edit ')
    select = SelectField('What Client ', choices=many)
    narrow= SelectField('What field', choices=listing)
    press = SubmitField('Confirm')