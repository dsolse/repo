from utils.db import db


class JuntaDirectiva(db.Model):  # type: ignore
    """
    Table model de la junta Directiva
    Campos:
        idPersona : int
        nombre : str
        apellido : str
        cargo : str
        correo : str
        link: str
    """

    # Campos tabla
    idPersona = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    cargo = db.Column(db.String(30), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    link=db.Column(db.String(1000), nullable=False)

    def __init__(
        self,
        correo: str,
        nombre: str,
        apellido: str,
        cargo: str,
        link: str
    ) -> None:

        self.nombre = nombre
        self.correo = correo
        self.apellido = apellido
        self.cargo = cargo
        self.link=link

    def __repr__(self) -> str:
        return f"""Junta Directiva(
            {self.idPersona}, 
            {self.nombre}, 
            {self.apellido}, 
            {self.cargo}, 
            {self.correo},
            {self.link})""".strip()

