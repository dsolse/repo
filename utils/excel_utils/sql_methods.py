from utils.db import db
from utils.excel_utils.view_models import VistaRegistro
from models.usuarios import Usuarios
from models.actividades import Actividades
from models.inscripciones import Inscripciones

def get_view_registro_academico_per_act(idActividad: int):
    query = db.session.query(
            # Campos a ser seleccionados
            Usuarios.correo,
            Usuarios.nombre,
            Usuarios.apellido,
            # cosas de actividad
            Actividades.nombreActividad,
            Actividades.tipoHoras,
            Actividades.tipoActividad,
            Actividades.horasSociales,
            Actividades.lugarActividad,
            Actividades.fechaFinal,
            Actividades.fechaInicio,
            # Condicionales
            Actividades.estado,
            Inscripciones.cantidadKg,
            Inscripciones.evidencia,
            Inscripciones.estadoPago,
            Inscripciones.estadoAsistencia,
        ).filter(Actividades.idActividad == idActividad).all()   # type: ignore

    return VistaRegistro.clean_query(query)
    

