from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length
from wtforms.fields import StringField, SubmitField, SelectField, PasswordField, IntegerField, DateField


class FormUpdateDatos(FlaskForm):
    numArboles = IntegerField(
        "Numero de Arboles",
        validators=[InputRequired()],
        render_kw={"placeholder": "Ingresa el Numero de Arboles"},
    )

    cantRec = IntegerField(
        "Numero de kilogramos recogidos",
        validators=[InputRequired()],
        render_kw={"placeholder": "Ingresa la cantidad de kilogramos recogidos"},
    )
    
    numVoluntarios = IntegerField(
        "Numero de Voluntarios",
        validators=[InputRequired()],
        render_kw={"placeholder": "Ingresa el Numero de Voluntarios"},
    )
    
    numCharlas = IntegerField(
        "Numero de charlas",
        validators=[InputRequired()],
        render_kw={"placeholder": "Ingresa el Numero de charlas"},
    )
    
    submit = SubmitField("Modificar")
