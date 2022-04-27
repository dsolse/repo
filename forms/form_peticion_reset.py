from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError


class FormPeticionContrasenna(FlaskForm):
    correo = EmailField(
        "Escribe tu mail",
        validators=[InputRequired()],
        render_kw={"placeholder": "Ingresa tu correo"},
    )
    
    submit = SubmitField("Enviar")
