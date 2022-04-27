import datetime
from random import choices
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models.usuarios import Usuarios

YEARS_UNI = [
    ("1", "Primer año"),
    ("2", "Segundo año"),
    ("3", "Tercer año"),
    ("4", "Cuarto año"),
    ("5", "Quinto año"),
]
CARRERAS=[
    ("1", "Ingeniería de Negocios"),
    ("2", "Licenciatura en Economía"),
    ("3", "Licenciatura en Ciencias Jurídicas"),
    
]

class RegisterForm(FlaskForm):
    correo = StringField(
        label="Correo",
        validators=[
            InputRequired(),
            Length(min=15, max=25)
        ],
        render_kw={"placeholder":"Ingresa tu correo institucional"}
    )

    nombre = StringField(
        label="Nombre",
        validators=[
            InputRequired(),
            Length(max=100),
        ],
        render_kw={"placeholder":"Ingresa tu nombre"}
    )

    apellido = StringField(
        label="Apellido",
        validators=[
            InputRequired(),
            Length(max=100),
        ],
        render_kw={"placeholder":"Ingresa tu apellido"}
    )

    telefono = StringField(
        label="Telefono (+503)",
        validators=[
            InputRequired(),
            Length(max=9),
        ],
        render_kw={"placeholder":"Ingresa tu teléfono: 0000-0000"}
    )
    
    carrera = SelectField(
        label="Carrera Universitaria",
        validators=[InputRequired()],
        choices= CARRERAS,
        render_kw={"placeholder":"Ingresa la carrera que cursas"}
    )

    contrasenna = PasswordField(
        label="Contraseña",
        validators=[
            InputRequired(),
            Length(min=2, max=15)
        ],
        render_kw={"placeholder":"Ingresa tu contraseña"}
    )

    contrasenna_2 = PasswordField(
        label="Contraseña",
        validators=[
            InputRequired(),
            Length(min=2, max=15),
            EqualTo("contrasenna", message='Las contraseñas deben ser iguales')

        ],
        render_kw={"placeholder":"Ingresa de nuevo tu contraseña"}
    )

    submit = SubmitField(label="Registrarse")

    def validate_correo(self, correo):
        correo_typed : str = correo.data
        current_mail = Usuarios.query.filter_by(correo=correo_typed).first()
        if not correo_typed.endswith("@esen.edu.sv"):
            raise ValidationError("El correo ingresado no es institucional")
        elif current_mail:
            raise ValidationError("El correo ingresado ya ha sido utilizado")
        elif 1998 > int(correo_typed[:4]) or int(datetime.date.today().year) < int(correo_typed[:4]):
            print(correo_typed[:4])
            raise ValidationError("El año del correo es inválido")


