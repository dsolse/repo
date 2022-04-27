from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length
from wtforms.fields import StringField, SubmitField, SelectField, PasswordField, IntegerField, DateField


TipoActividad=[
    ("2", "Reciclaje"),
    ("1", "Limpieza"),
    ("3", "Capacitaciones"),
    ("4", "Otro"), 
]

TipoHoras=[
    ("1", "Medioambientales"),
    ("2", "Normales"),
    ("3", "Administrativas"),
]

Estados=[
    ("2", "En progreso"),
    ("1", "Terminada"),
    ("0", "Cancelada"),
]

class FormUpdateActivity(FlaskForm):
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

    tipoActividad = SelectField(
        label="Tipo de Actividad",
        validators=[InputRequired()],
        choices= TipoActividad,
        render_kw={"placeholder":"Ingresa el tipo de actividad"}
    )

    lugarActividad = StringField(
        "Lugar",
        validators=[InputRequired(), Length(min=3, max=100)],
        render_kw={"placeholder": "Ingresa el lugar de realización de la actividad"},
    )
    
    tipoHoras = SelectField(
        label="Tipo de Horas",
        validators=[InputRequired()],
        choices= TipoHoras,
        render_kw={"placeholder":"Ingresa el tipo de horas de la actividad"}
    )
    
    fechaInicio = DateField(
        "Fecha de inicio",
         format='%Y-%m-%d',
        validators=[InputRequired()],
        render_kw={"placeholder": "Ingresa la fecha de inicio"},
    )

# En las fechas podemos implementar un datepicker en el html para evitar que pongan la fecha con mal formato
    fechaFinal = DateField(
        "Fecha de finalización",
         format='%Y-%m-%d',
        validators=[InputRequired()],
        render_kw={"placeholder": "Ingresa la fecha de finalización"},
    )
    
    horasSociales = IntegerField(
        "Horas Sociales",
        validators=[InputRequired()],
        render_kw={"placeholder": "Ingresa las horas sociales asistencia o por kilo, según aplique"},
    )
    
    cuposTotales = IntegerField(
        "Cupos totales",
        validators=[InputRequired()],
        render_kw={"placeholder": "Ingresa los cupos totales para la actividad"},
    )
    
    Estado = SelectField(
        label="Estado",
        validators=[InputRequired()],
        choices= Estados,
        render_kw={"placeholder":"Ingresa el estado de la actividad"}
    )

    submit = SubmitField("Modificar")
