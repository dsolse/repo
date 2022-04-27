from typing import Union
from utils.db import db
from datetime import datetime
from flask_login import UserMixin


class Usuarios(db.Model, UserMixin):  # type: ignore
    """
    Table model de los Usuarios
    Campos:
        carnet : str
        nombre : str
        contrasenna : str
        apellido : str
        anno : int
        telefono : str
        cargo: str
        correo : str
        carrera: str
    """

    # Campos tabla
    idVoluntario = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(100), nullable=False)
    contrasenna = db.Column(db.String(100), nullable= False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    cargo = db.Column(db.String(50), nullable=False)
    departamento = db.Column(db.String(50), nullable=False)
    carrera = db.Column(db.String(50), nullable=False)
    anno = db.Column(db.Integer, nullable=False)
    

    def __init__(
        self,
        correo: str,
        contrasenna: Union[str, bytes],
        nombre: str,
        apellido: str,
        telefono: str,
        cargo: str,
        departamento: str,
        carrera: str,
        anno: int,
    ) -> None:

        self.correo = correo
        self.contrasenna = contrasenna
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.cargo = cargo
        self.departamento = departamento
        self.carrera = carrera
        self.anno = anno

    def __repr__(self) -> str:
        return f"""Usuario(
            {self.idVoluntario}, 
            {self.contrasenna},
            {self.nombre}, 
            {self.apellido}, 
            {self.telefono}, 
            {self.cargo},
            {self.departamento},
            {self.correo}
            {self.carrera}
            {self.anno})""".strip()


    def get_carnet(self, carnet_: Union[str, None]):
        carnet: str
        if bool(carnet_) and not self.correo.endswith("@esen.edu.sv"):
            carnet = carnet_
        else:
            try:
                carnet = self.correo[:7]
            except Exception:
                carnet = "None"
        return carnet

    # Necesario para el login
    def get_id(self):
        return (self.idVoluntario)