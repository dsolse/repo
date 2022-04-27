from utils.db import db

class Datos(db.Model):  # type: ignore
    """
    Table model de las actividades
    Campos:
        numArboles: int
        cantRec: int
        numVoluntariuos: int
        numCharlas: int
        
    """

    # Campos tabla
    idDatos = db.Column(db.Integer, primary_key = True)
    numArboles = db.Column(db.Integer, nullable = False)
    cantRec = db.Column(db.Integer, nullable = False)
    numVoluntarios = db.Column(db.Integer, nullable = False)
    numCharlas = db.Column(db.Integer, nullable = False)
    
    def __init__(
        self,
        numArboles: int,
        cantRec: int,
        numVoluntarios : int,
        numCharlas: int
    ) -> None:

        self.numArboles = numArboles
        self.cantRec = cantRec
        self.numVoluntarios = numVoluntarios
        self.numCharlas = numCharlas

    def __repr__(self) -> str:
        return f"""Datos(
        {self.idDatos},
        {self.numArboles},
        {self.cantRec},
        {self.numVoluntarios},
        {self.numCharlas},
        )
        """.strip()

