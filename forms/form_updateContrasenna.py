from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError


class FormContrasenna(FlaskForm):
    correo = EmailField(
        "Escribe tu correo",
        validators=[InputRequired()],
        render_kw={"placeholder": "Ingresa tu correo"},
    )
    contrasenna = PasswordField(
        label="Contraseña",
        validators=[InputRequired(), Length(min=2, max=15)],
        render_kw={"placeholder": "Ingresa tu contraseña"},
    )

    contrasenna_2 = PasswordField(
        label="Contraseña",
        validators=[
            InputRequired(),
            Length(min=2, max=15),
            EqualTo("contrasenna", message="Las contraseñas son distintas"),
        ],
        render_kw={"placeholder": "Ingresa de nuevo tu contraseña"},
    )

    submit = SubmitField("Modificar")
