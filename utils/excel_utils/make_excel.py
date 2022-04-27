import os
from typing import Union
from utils.excel_utils.view_models import VistaRegistro
from flask import session
import pandas as pd
import os


def create_excel(
    data_vista: list[VistaRegistro],
    filename="horas_sociales",
    sheet_name="Horas sociales",
) -> Union[str, None]:

    """Crear un archivo excel a partir de una lista de models de VistaRegistro"""
    data = [
        [
            record.carnet,
            record.nombre_apellido,
            record.actividad,
            record.lugar,
            record.total_horas,
            record.fecha_inicio,
            record.fecha_final,
            record.total_horas
        ]
        for record in data_vista
    ]
    df = pd.DataFrame(
        data,
        columns=[
            "Carnet",
            "Nombre alumno",
            "Actividad",
            "Lugar",
            "Tipo horas",
            "Fecha de inicio",
            "Fecha final",
            "Horas totales",
        ],
    )
    path = os.getcwd() + "/" + filename + ".xlsx"
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    return path


def delete_if_exist(path: str):
    """Borra archivo excel del almacenamiento de la app flask"""
    if os.path.exists(path):
        session.pop("path_excel")
        os.remove(path)
