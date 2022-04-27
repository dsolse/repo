from __future__ import annotations

class VistaRegistro:
    """
    Model de la vista para registro academico:
        Campos:
            carnet : str,
            nombre_apellido : str,
            lugar : str,
            activiadd : str
            tipo_actividad : str
            tipo_horas : str,
            fecha_inicio : str,
            fecha_final : str
    """

    def __init__(
        self,
        carnet: str,
        nombre_apellido: str,
        lugar,
        tipo_horas : str, 
        actividad: str,
        tipo_actividad : str,
        fecha_inicio,
        fecha_final,
        total_horas: int,
    ) -> None:
        self.carnet = carnet
        self.actividad = actividad
        self.nombre_apellido = nombre_apellido
        self.total_horas = tipo_horas
        self.total_horas = total_horas
        self.fecha_inicio = fecha_inicio
        self.fecha_final = fecha_final
        self.lugar = lugar
        self.tipo_actividad = tipo_actividad

    @classmethod
    def clean_query(cls, query):
        vols = []
        tiposActs = {1 : "Limpieza", 2 : "Reciclaje", 3 : "Charlas", 4 : "Otros"}
        for row in query:
            if row.estado == 1 and row.estadoAsistencia == 1:
                carnet = VistaRegistro.get_carnet(row.correo)
                actividad = row.nombreActividad
                fechaInicio = row.fechaInicio
                fechaFinal = row.fechaFinal
                lugar = row.lugarActividad
                tipo_horas = "Ambientales" if row.tipoHoras == 1 else "Administrativas"
                tipoActividad = tiposActs[row.tipoActividad]

                total_horas = row.cantidadKg * row.horasSociales  if row.tipoActividad == 1 or  row.tipoActividad == 2 else row.horasSociales
                nombre_apellido = row.nombre + " " + row.apellido

                if not row.estadoPago == 2:
                    if not row.evidencia == 2:
                        vols.append(cls(carnet,nombre_apellido, lugar, tipo_horas, actividad, tipoActividad, fechaInicio, fechaFinal, total_horas))

        return vols

    @staticmethod
    def get_carnet(correo_: str) -> str:
        carnet = "NA"
        if correo_.endswith("@esen.edu.sv"):
            carnet = correo_.removesuffix("@esen.edu.sv")
        return carnet

    def __repr__(self) -> str:
        return f"""
        VistaReistro(
            {self.carnet},
            {self.actividad},
            {self.nombre_apellido},
            {self.total_horas}
        )
        """.strip()
