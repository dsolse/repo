from flask import (
    Blueprint,
    redirect,
    request,
    send_file,
    session,
    render_template,
)
from forms.formUpdateDatos import FormUpdateDatos
from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, login_user, logout_user, current_user
from utils.excel_utils.photos_model import Photo, PhotoNext
from flask import Blueprint, send_file, session
from utils.excel_utils.make_excel import create_excel, delete_if_exist
from forms.form_updateInsc import FormUpdateInsc
from models.usuarios import Usuarios
from utils.db import db
from forms.form_addJD import FormAddJD
from forms.form_updateActivity import FormUpdateActivity
from forms.form_updateJD import FormUpdateJD
from forms.form_addActividad import FormAddActivity
from models.actividades import Actividades

# Vistas
from utils.excel_utils.sql_methods import get_view_registro_academico_per_act

# Models
from models.actividades import Actividades
from models.inscripciones import Inscripciones
from models.datos import Datos
from models.usuarios import Usuarios
from models.juntaDirectiva import JuntaDirectiva
from models.contactanos import Contactanos
from utils.cryptography import CryptographyToken
from utils.random_images import (
    STRING_SHARING,
    get_image_id_from_link,
    get_random_images_list,
)


admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/")
@login_required
def home():
    img_random = get_random_images_list()

    fotos_data = {
        i: Photo(
            url=STRING_SHARING + "=" + i,
            desc=f"",
        )
        for i in img_random
    }

    next_act = {
        i: PhotoNext(STRING_SHARING + "=" + i, f"No se {i}", 0) for i in img_random
    }
    actividadesActivas = Actividades.query.filter_by(estado=2).all()


    return render_template(
        "main/home.html",
        fotos_data=fotos_data,
        next_act=next_act,
        user=current_user,
        actividadesActivas=actividadesActivas,
    )


@admin.route("/about")
@login_required
def about():
    return render_template(
        "main/about.html",
        user=current_user,
    )


@admin.route("/activities")
@login_required
def activities():
    return render_template(
        "main/activities.html",
        user=current_user,
    )


@admin.route("/activities/inscripcion", methods=["GET", "POST"])
@login_required
def inscripcion(nombreAct):
    idVoluntario = current_user.idVoluntario  # type: ignore
    idActividad = nombreAct
    estadoAsistencia = 1
    estadoPago = 2
    cantidadKg = 0
    horastotales = 0
    evidencia = 1
    newIns = Inscripciones(
        idVoluntario,
        idActividad,
        estadoAsistencia,
        estadoPago,
        cantidadKg,
        horastotales,
        evidencia
    )
    db.session.add(newIns)
    db.session.commit()
    return redirect(url_for("main.activities", nombreAct=nombreAct))


@admin.route("/contact")
@login_required
def contact():
    return render_template(
        "main/contact.html",
        user=current_user,
    )


@admin.route("/dashboard")
@login_required
def dashboard():
    if current_user.cargo == "Admin":  # type: ignore
        currentDato = Datos.query.all()
        print(currentDato)
        MiembrosFull = Usuarios.query.filter_by(cargo="miembro").all()
        VoluntarioFull = Usuarios.query.filter_by(cargo="NA").all()
        JDFull = JuntaDirectiva.query.all()
        InscripcionesFull = Inscripciones.query.all()
        ActividadesFull = Actividades.query.all()
        MessagesFull = Contactanos.query.all()
        return render_template(
            "admin/dashboard.html",
            VoluntarioFull=VoluntarioFull,
            MiembrosFull=MiembrosFull,
            JDFull=JDFull,
            InscripcionesFull=InscripcionesFull,
            ActividadesFull=ActividadesFull,
            MessagesFull=MessagesFull,
            user=current_user,
            currentDato=currentDato
        )

    return redirect(url_for("main.home"))


@admin.route("/delete/user/<int:idVoluntario>")
@login_required
def deleteVoluntario(idVoluntario):
    if current_user.cargo == "Admin":
        selectedUser = Usuarios.query.filter_by(idVoluntario=idVoluntario).first()
        correo = selectedUser.correo
        contrasenna = selectedUser.contrasenna
        nombre = selectedUser.nombre
        apellido = selectedUser.apellido
        telefono = selectedUser.telefono
        carrera = selectedUser.carrera
        anno = selectedUser.anno
        departamento = "Baja"

        selectedUser.correo = correo
        selectedUser.contrasenna = contrasenna
        selectedUser.nombre = nombre
        selectedUser.apellido = apellido
        selectedUser.telefono = telefono
        selectedUser.carrera = carrera
        selectedUser.anno = anno
        selectedUser.departamento = departamento
        db.session.add(selectedUser)
        db.session.commit()
        return redirect(url_for("admin.dashboard", idVoluntario=idVoluntario))
    return redirect(url_for("main.home"))


@admin.route("/Upgrade/user/<int:idVoluntario>", methods=["POST", "GET"])
@login_required
def hacerMiembro(idVoluntario):
    if current_user.cargo == "Admin":
        if request.method == "POST":
            selectedUser = Usuarios.query.filter_by(idVoluntario=idVoluntario).first()
            correo = selectedUser.correo
            contrasenna = selectedUser.contrasenna
            nombre = selectedUser.nombre
            apellido = selectedUser.apellido
            telefono = selectedUser.telefono
            carrera = selectedUser.carrera
            anno = selectedUser.anno
            departamento = request.form.get("position")
            cargo = "miembro"

            selectedUser.correo = correo
            selectedUser.contrasenna = contrasenna
            selectedUser.nombre = nombre
            selectedUser.apellido = apellido
            selectedUser.telefono = telefono
            selectedUser.carrera = carrera
            selectedUser.anno = anno
            selectedUser.departamento = departamento
            selectedUser.cargo = cargo
            db.session.add(selectedUser)
            db.session.commit()
            return redirect(url_for("admin.dashboard", idVoluntario=idVoluntario))
        else:
            return redirect(url_for("admin.dashboard", idVoluntario=idVoluntario))
    return redirect(url_for("main.home"))


@admin.route("/NewActivity", methods=["POST", "GET"])
@login_required
def addActivity():
    if current_user.cargo == "Admin":
        user = current_user
        form = FormAddActivity()
        if form.validate_on_submit():
            descripcion = form.descripcion.data
            nombre = form.nombre.data
            tipoActividad = form.tipoActividad.data
            lugarActividad = form.lugarActividad.data
            tipoHoras = form.tipoHoras.data
            fechaInicio = form.fechaInicio.data
            fechaFinal = form.fechaFinal.data
            horasSociales = form.horasSociales.data
            cuposTotales = form.cuposTotales.data
            estado = 1
            newAct = Actividades(
                descripcion,
                nombre,
                tipoActividad,
                lugarActividad,
                tipoHoras,
                fechaInicio,
                fechaFinal,
                horasSociales,
                cuposTotales,
                estado,
            )
            db.session.add(newAct)
            db.session.commit()
            return redirect(url_for("admin.dashboard"))
        return render_template("admin/activities/newActivity.html", form=form, user=user)
    return redirect(url_for("main.home"))


@admin.route("/updateActivity/<int:idActividad>", methods=["POST", "GET"])
@login_required
def updateActivity(idActividad):
    if current_user.cargo == "Admin":
        user = current_user
        currentActividad = Actividades.query.get(idActividad)
        form = FormUpdateActivity()
        if form.validate_on_submit():
            descripcion = form.descripcion.data
            nombre = form.nombre.data
            tipoActividad = int(form.tipoActividad.data)
            lugarActividad = form.lugarActividad.data
            tipoHoras = form.tipoHoras.data
            fechaInicio = form.fechaInicio.data
            fechaFinal = form.fechaFinal.data
            horasSociales = form.horasSociales.data
            cuposTotales = form.cuposTotales.data
            Estado = int(form.Estado.data)

            currentActividad.descripcion = descripcion
            currentActividad.nombre = nombre
            currentActividad.tipoActividad = tipoActividad
            currentActividad.lugarActividad = lugarActividad
            currentActividad.tipoHoras = tipoHoras
            currentActividad.fechaInicio = fechaInicio
            currentActividad.fechaFinal = fechaFinal
            currentActividad.horasSociales = horasSociales
            currentActividad.cuposTotales = cuposTotales
            currentActividad.estado = Estado
            db.session.add(currentActividad)
            db.session.commit()
            return redirect(
                url_for(
                    "admin.dashboard",
                    form=form,
                    user=user,
                    currentActividad=currentActividad,
                    idActividad=idActividad,
                )
            )
        form.fechaInicio.data = currentActividad.fechaInicio
        form.fechaFinal.data = currentActividad.fechaFinal

        return render_template(
            "admin/activities/updateActivity.html",
            form=form,
            user=user,
            currentActividad=currentActividad,
            idActividad=idActividad,
        )
    return redirect(url_for("main.home"))


@admin.route("/NewJD", methods=["POST", "GET"])
@login_required
def addJD():
    if current_user.cargo == "Admin":
        user = current_user
        form = FormAddJD()
        if form.validate_on_submit():
            nombre = form.nombre.data
            apellido = form.apellido.data
            cargo = form.cargo.data
            correo = form.correo.data
            link = STRING_SHARING + "=" + get_image_id_from_link(form.link.data)
            newJD = JuntaDirectiva(
                correo,
                nombre,
                apellido,
                cargo,
                link,
            )
            db.session.add(newJD)
            db.session.commit()
            return redirect(url_for("admin.dashboard"))
        return render_template("admin/JD/newJD.html", form=form, user=user)
    return redirect(url_for("main.home"))


@admin.route("/updateJD/<int:idPersona>", methods=["POST", "GET"])
@login_required
def updateJD(idPersona):
    if current_user.cargo == "Admin":
        user = current_user
        currentJD = JuntaDirectiva.query.filter_by(idPersona=idPersona).first()
        form = FormUpdateJD(juntadirectiva=currentJD)
        if form.validate_on_submit():
            nombre = form.nombre.data
            apellido = form.apellido.data
            cargo = form.cargo.data
            correo = form.correo.data
            link = STRING_SHARING + "=" + get_image_id_from_link(form.link.data)
            currentJD.nombre = nombre
            currentJD.apellido = apellido
            currentJD.cargo = cargo
            currentJD.correo = correo
            currentJD.link = link
            db.session.add(currentJD)
            db.session.commit()
            return redirect(
                url_for(
                    "admin.dashboard",
                    form=form,
                    user=user,
                    idPersona=idPersona,
                    currentJD=currentJD,
                )
            )
        return render_template(
            "admin/JD/updateJD.html",
            form=form,
            user=user,
            idPersona=idPersona,
            currentJD=currentJD,
        )

    return redirect(url_for("main.home"))

@admin.route("/updateDatos/<int:idDatos>", methods=["POST", "GET"])
@login_required
def updateDatos(idDatos):
    if current_user.cargo == "Admin":
        user = current_user
        currentDato = Datos.query.filter_by(idDatos=idDatos).first()
        form = FormUpdateDatos(datos=currentDato)
        if form.validate_on_submit():
            numArboles= form.numArboles.data
            cantRec = form.cantRec.data
            numVoluntarios = form.numVoluntarios.data
            numCharlas = form.numCharlas.data
            currentDato.numArboles = numArboles
            currentDato.cantRec = cantRec
            currentDato.numVoluntarios = numVoluntarios
            currentDato.numCharlas = numCharlas
            db.session.add(currentDato)
            db.session.commit()
            return redirect(
                url_for(
                    "admin.dashboard",
                    form=form,
                    user=user,
                    idDatos=idDatos,
                    currentDato=currentDato
                )
            )
        return render_template(
            "admin/updateDatos.html",
            form=form,
            user=user,
            idDatos=idDatos,
            currentDato=currentDato
        )
    return redirect(url_for("main.home"))


@admin.route("/downgrade/user/<int:idVoluntario>")
@login_required
def hacerVoluntario(idVoluntario):
    if current_user.cargo == "Admin":
        selectedUser = Usuarios.query.filter_by(idVoluntario=idVoluntario).first()
        correo = selectedUser.correo
        contrasenna = selectedUser.contrasenna
        nombre = selectedUser.nombre
        apellido = selectedUser.apellido
        telefono = selectedUser.telefono
        carrera = selectedUser.carrera
        anno = selectedUser.anno
        departamento = "NA"
        cargo = "NA"

        selectedUser.correo = correo
        selectedUser.contrasenna = contrasenna
        selectedUser.nombre = nombre
        selectedUser.apellido = apellido
        selectedUser.telefono = telefono
        selectedUser.carrera = carrera
        selectedUser.anno = anno
        selectedUser.departamento = departamento
        selectedUser.cargo = cargo
        db.session.add(selectedUser)
        db.session.commit()
        return redirect(url_for("admin.dashboard", idVoluntario=idVoluntario))
    return redirect(url_for("main.home"))


@admin.route("/delete/junta/<int:idPersona>")
@login_required
def deleteJD(idPersona):
    JuntaDirectiva.query.filter_by(idPersona=idPersona).delete()
    db.session.commit()
    return redirect(url_for("admin.dashboard", idPersona=idPersona))


@admin.route("/delete/actividad/<int:idActividad>")
@login_required
def deleteActividad(idActividad):
    Inscripciones.query.filter_by(idActividad=idActividad).delete()

    Actividades.query.filter_by(idActividad=idActividad).delete()
    db.session.commit()
    return redirect(url_for("admin.dashboard", idActividad=idActividad))


@admin.route("/changeStatus/mensaje/<int:idContacto>")
@login_required
def changeStatusMessage(idContacto):
    selectedMessage = Contactanos.query.filter_by(idContacto=idContacto).first()
    # id = selectedMessage.idContacto
    nombre = selectedMessage.nombre
    apellido = selectedMessage.apellido
    telefono = selectedMessage.telefono
    mensaje = selectedMessage.mensaje
    if selectedMessage.estado == 0:
        newStatus = 1
    else:
        newStatus = 0

    selectedMessage.nombre = nombre
    selectedMessage.apellido = apellido
    selectedMessage.telefono = telefono
    selectedMessage.mensaje = mensaje
    selectedMessage.estado = newStatus
    db.session.add(selectedMessage)
    db.session.commit()
    return redirect(url_for("admin.dashboard", idContacto=idContacto))


@admin.route("/delete/mensaje/<int:idContacto>")
@login_required
def deleteMessage(idContacto):
    selectedMessage = Contactanos.query.get(idContacto)
    db.session.delete(selectedMessage)
    db.session.commit()
    return redirect(url_for("admin.dashboard", idContacto=idContacto))

@admin.route("/modificar/inscripciones/<int:idInsc>", methods=["POST", "GET"])
@login_required
def updateInscripcion(idInsc):
    selectedInsc = Inscripciones.query.get(idInsc)
    form = FormUpdateInsc()
    if form.validate_on_submit():
        selectedInsc.estadoAsistencia =  int(form.asistencia.data)
        selectedInsc.cantidadKg = form.cantidadKg.data
        selectedInsc.evidencia = int(form.evidencia.data)
        selectedInsc.estadoPago = int(form.pago.data)
        db.session.add(selectedInsc)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    form.asistencia.data =selectedInsc.estadoAsistencia
    form.cantidadKg.data =int(selectedInsc.cantidadKg)
    form.evidencia.data = selectedInsc.evidencia
    form.pago.data = int(selectedInsc.estadoPago)
    return render_template("admin/updateInsc.html", idInsc=idInsc, user=current_user, form=form)




@admin.route("/download/<int:idAct>", methods=["POST", "GET"])
@login_required
def download_excel(idAct):
    if current_user.cargo == "Admin":
        if "path_excel" in session:
            delete_if_exist(session["path_excel"])

        data = get_view_registro_academico_per_act(idAct)
        path = create_excel(data)
        
        if path:
            session["path_excel"] = path
            return send_file(path)
        else:
            return "Hubo un error procesando los datos"

    return redirect(url_for("main.home"))

def generate_link_reset_password(id, correo_init):
    cryptography_tool = CryptographyToken()
    return f"/reset/password/{cryptography_tool.encrypt_token(id)}/{cryptography_tool.encrypt_token(correo_init)}"


@admin.route(f"/reset/password/<id>/<correo>", methods=["POST", "GET"])
def generate_link(id, correo):
    if current_user.cargo == "Admin":
        link = generate_link_reset_password(id, correo)
        return render_template("admin/reset_link.html", user=current_user, link=link)
    return redirect(url_for("main.home"))
