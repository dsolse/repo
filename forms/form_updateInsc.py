from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length
from wtforms.fields import StringField, SubmitField, SelectField, PasswordField, IntegerField, DateField


evidencias=[
    ("1", "Enviada"),
    ("2", "No enviada"),
    ("3", "NA"),
]

asistencias=[
    ("1", "Asistió"),
    ("2", "No asistió"),
    ("3", "Canceló"),
]

pagos=[
    ("1", "Pagado"),
    ("2", "No pagado"),
    ("3", "NA"),
]

class FormUpdateInsc(FlaskForm):
    asistencia = SelectField(
        "Estado asistencia",
        validators=[InputRequired()],
        choices= asistencias,
        render_kw={"placeholder": "Ingresa estado asistencia"},
    )

    pago = SelectField(
        "Estado pago",
        validators=[InputRequired()],
        choices= pagos,
        render_kw={"placeholder": "Ingresa estado pago"},
    )

    cantidadKg = IntegerField(
        label="Cantidad kg",
        validators=[InputRequired()],
        render_kw={"placeholder":"Ingresa cantidad"}
    )

    evidencia = SelectField(
        "Evidencia",
        validators=[InputRequired()],
        choices= evidencias,
        render_kw={"placeholder": "Ingresa estado evidencia"},
    )

    submit = SubmitField("Modificar")
