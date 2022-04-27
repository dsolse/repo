from utils.db import db
from models.actividades import Actividades


class Inscripciones(db.Model):  # type: ignore
    """
    Table model de inscripciones:
    Campos:
        idVoluntario : int
        idActividad : int
        estadoInicial : int
        estadoFinal: int
        pago : int
        cantidadKg : float
        evidencia: int
    """

    # Campos tabla
    idInscripcion = db.Column(db.Integer, primary_key=True)
    idVoluntario = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.idVoluntario"),
        nullable=False,
    )
    idActividad = db.Column(
        db.Integer,
        db.ForeignKey("actividades.idActividad"),
        nullable=False,
    )
    estadoAsistencia = db.Column(db.Integer, nullable=False)
    estadoPago = db.Column(db.Integer, nullable=False)
    cantidadKg = db.Column(db.Float, nullable=True)
    horasTotales = db.Column(db.Integer, nullable=False)
    evidencia = db.Column(db.Integer, nullable=False)

    def __init__(
        self,
        idVoluntario: int,
        idActividad: int,
        estadoAsistencia: int,
        estadoPago: int,
        horasTotales: int,
        cantidadKg: float,
        evidencia: int
    ) -> None:

        self.idActividad = idActividad
        self.idVoluntario = idVoluntario
        self.estadoAsistencia = estadoAsistencia
        self.estadoPago = estadoPago
        self.horasTotales = horasTotales
        self.cantidadKg = cantidadKg
        self.evidencia = evidencia

    def __repr__(self) -> str:
        return f"""
    Inscripciones(
        {self.idInscripcion},
        {self.idActividad},
        {self.idVoluntario},
        {self.estadoAsistencia},
        {self.estadoPago},
        {self.cantidadKg},
        {self.horasTotales},
        {self.evidencia}
    )
    """.strip()

    def get_horas_sociales(self):
        """Retorna horas sociales + (horasKg por cantidad recogida)"""
        actitivdad: Actividades = Actividades.query.get(self.idActividad)
        return actitivdad.horasSociales + (
            actitivdad.horasKg or 0 * self.cantidadKg or 0
        )

    @classmethod
    def get_cupos_restantes(cls, idActividad, cuposTotales) -> int:
        """Retorna los cupos restantes de una actividad"""
        cupos_llenos = len(cls.query.filter_by(idActividad=idActividad).all())
        return cuposTotales - cupos_llenos
