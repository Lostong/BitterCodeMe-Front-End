"""
Форма реєстрації та входу 
"""

from flask_wtf import (
    FlaskForm,
)

from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    EmailField,
    SelectField
)

from wtforms.validators import (
    Email,
    Length,
    DataRequired,
    EqualTo,
)

class Registration(FlaskForm):
    """
    Клас форми реєстрації
    """
    name = StringField(label="Name:", 
                       validators=[DataRequired(),
                            Length(min=3, max=32)])
   
    email = EmailField(label='Email:', 
                        validators=[DataRequired(),
                            Email()])

    password = PasswordField(label='Password:',
                            validators=[Length(min=8, max=32),
                            DataRequired()])

    confirm = PasswordField(label='Confirm password:',
                            validators=[
                                DataRequired(),
                                EqualTo('password')])
    
    role = SelectField(label='Your role:', choices=[('1','Employer'), ('2', 'Candidate')], 
                            validators=[
                                 DataRequired()])

    submit = SubmitField(label='Log in')


class Login(FlaskForm):
    """
    Форма для входу
    """
    email = EmailField(label='Email:', 
                        validators=[DataRequired(),
                            Email()])

    password = PasswordField(label='Password:',
                            validators=[Length(min=8, max=32),
                            DataRequired()])

    submit = SubmitField(label='Log in')
