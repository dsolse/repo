from utils.db import db


class encargadoActividad(db.Model):  # type: ignore
    """
    Table model de inscripciones:
    Campos:
        idVoluntario : int
        idActividad : int
        cargo : int
        horas: int
    """

    # Campos tabla
    idEncargado = db.Column(db.Integer, primary_key=True)
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
    cargo = db.Column(db.String(30), nullable=False)
    horas = db.Column(db.Integer, nullable=False)

    def __init__(
        self,
        idVoluntario: int,
        idActividad: int,
        cargo: str,
        horas: int,
    ) -> None:

        self.idActividad = idActividad
        self.idVoluntario = idVoluntario
        self.cargo = cargo
        self.horas = horas
        
    def __repr__(self) -> str:
        return f"""
    encargadoActividad(
        {self.idInscripcion},
        {self.idActividad},
        {self.idVoluntario},
        {self.cargo},
        {self.horas},
    """.strip()
