from wtforms import Form, BooleanField, StringField, FloatField, DateField, SelectField, PasswordField, validators, SubmitField
from wtforms.validators import InputRequired

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25), InputRequired()], render_kw={"placeholder": "Pick a Username"})
    email = StringField('Email Address', [validators.Length(min=6, max=35), InputRequired()], render_kw={"placeholder": "email"})
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ], render_kw={"placeholder": "Password"})
    confirm = PasswordField('Repeat Password', render_kw={"placeholder": "Password"})

    submit = SubmitField('Submit')

class InputSpendings(Form):
    amount = FloatField("Amount", [InputRequired()], render_kw={"placeholder": "How much?"})
    date_ref = DateField("Month Ref", format='%m/%Y', validators=[InputRequired()], render_kw={"placeholder": "format: 'mm/yyyy'"})
    payee = SelectField("Payee", validators=[InputRequired()], choices=[('Luz','Luz'), ('Aluguel','Aluguel'), ('NET','NET')])

    submit = SubmitField('Submit')
