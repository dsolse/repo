from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length


class FormContactanos(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[InputRequired(), Length(min=2, max=10)],
        render_kw={"placeholder": "Ingresa tu nombre"},
    )

    apellido = StringField(
        "Apellido",
        validators=[InputRequired(), Length(min=3, max=20)],
        render_kw={"placeholder": "Ingresa tu apellido"},
    )

    telefono = StringField(
        "Teléfono",
        validators=[InputRequired(), Length(min=2, max=10)],
        render_kw={"placeholder": "Ingresa tu teléfono"},
    )

    text_area = TextAreaField(
        "",
        validators=[InputRequired(), Length(min=2, max=200)],
        render_kw={"placeholder": "Déjanos un mensaje"},
    )

    submit = SubmitField("Enviar")
