from utils.db import db
from datetime import datetime


class Actividades(db.Model):  # type: ignore
    """
    Table model de las actividades
    Campos:
        nombreActividad : str
        descripcion :str
        fechaInicio : datetime
        fechaFinal : datetime
        horasSociales : int
        horasKg : int
        tipoActividad: int
        cuposTotales: int
        estado : int
    """

    # Campos tabla
    idActividad = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(500), nullable=False)
    nombreActividad = db.Column(db.String(50), nullable=False)
    tipoActividad = db.Column(db.Integer, nullable=False)
    lugarActividad = db.Column(db.String(200), nullable=False)
    tipoHoras = db.Column(db.Integer, nullable=False)
    fechaInicio = db.Column(db.DateTime, nullable=False)
    fechaFinal = db.Column(db.DateTime, nullable=False)
    horasSociales = db.Column(db.Integer, nullable=True)
    cuposTotales = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.Integer, nullable=False)

    def __init__(
        self,
        descripcion: str,
        nombreActividad: str,
        tipoActividad: int,
        lugarActividad: str,
        tipoHoras: int,
        fechaInicio: datetime,
        fechaFinal: datetime,
        horasSociales: int,
        cuposTotales: int,
        estado : int
    ) -> None:

        self.descripcion = descripcion
        self.nombreActividad = nombreActividad
        self.tipoActividad = tipoActividad
        self.lugarActividad = lugarActividad
        self.tipoHoras = tipoHoras
        self.fechaInicio = fechaInicio
        self.fechaFinal = fechaFinal
        self.horasSociales = horasSociales
        self.cuposTotales = cuposTotales
        self.estado = estado

    def __repr__(self) -> str:

        return f"""
        Actividad(
        {self.descripcion},
        {self.idActividad},
        {self.nombreActividad},
        {self.tipoActividad},
        {self.lugarActividad}
        {self.tipoHoras},
        {self.fechaInicio},
        {self.fechaFinal},
        {self.horasSociales},
        {self.cuposTotales},
        {self.estado},
        )
        """.strip()

    @classmethod
    def get_activity(cls, id: int) -> int:
        result = cls.query.get(id)
        return result.tipoActividad
