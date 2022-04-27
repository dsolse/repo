from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length
from wtforms.fields import StringField, SubmitField, SelectField, PasswordField, IntegerField, DateField, DateTimeField


# Estados=[
#     ("1", "En progreso"),
#     ("2", "Terminada"),
#     ("3", "Cancelada"),
# ]

class FormAddActivity(FlaskForm):
    descripcion = StringField(
        "Descripción",
        validators=[InputRequired(), Length(min=2, max=2000)],
        render_kw={"placeholder": "Ingresa la descripción de la actividad"},
    )

    nombre = StringField(
        "Nombre",
        validators=[InputRequired(), Length(min=3, max=20)],
        render_kw={"placeholder": "Ingresa el nombre de la actividad"},
    )

    tipoActividad = IntegerField(
        label="Tipo de actividad",
        validators=[InputRequired()],
        render_kw={"placeholder":"Ingresa el tipo de actividad"}
    )

    lugarActividad = StringField(
        "Lugar",
        validators=[InputRequired(), Length(min=3, max=100)],
        render_kw={"placeholder": "Ingresa el lugar de realización de la actividad"},
    )
    
    tipoHoras = IntegerField(
        label="Tipo de horas",
        validators=[InputRequired()],
        render_kw={"placeholder":"Ingresa el tipo de horas de la actividad"}
    )
    
    
    fechaInicio = DateField(
        label= "Fecha de inicio",
        validators=[InputRequired()],
        render_kw={"placeholder": "Ingresa la fecha de inicio"},
    )

    fechaFinal = DateField(
        label= "Fecha de fin",
        validators=[InputRequired()],
        render_kw={"placeholder": "Ingresa la fecha de finalización"},
    )
    
    horasSociales = IntegerField(
        "Horas sociales",
        validators=[InputRequired()],
        render_kw={"placeholder": "Ingresa las horas sociales asistencia o por kilo, según aplique"},
    )
    
    cuposTotales = IntegerField(
        "Cupos totales",
        validators=[InputRequired()],
        render_kw={"placeholder": "Ingresa los cupos totales para la actividad"},
    )

    submit = SubmitField("Agregar")
