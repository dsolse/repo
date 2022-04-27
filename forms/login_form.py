from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    correo = StringField(
        label="Correo",
        validators=[
            InputRequired(),
            Length(min=15, max=25)
        ],
        render_kw={"placeholder":"Ingresa tu correo institucional"}
    )

    contrasenna = PasswordField(
        label="Contraseña",
        validators=[
            InputRequired(),
            Length(min=2, max=15)
        ],
        render_kw={"placeholder":"Ingresa tu contraseña"}
    )

    submit = SubmitField(label="Iniciar sesión")