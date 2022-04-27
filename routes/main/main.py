from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from utils.excel_utils.sql_methods import get_view_registro_academico_per_act
from forms.form_contactanos import FormContactanos
from forms.form_peticion_reset import FormPeticionContrasenna
from forms.form_updateContrasenna import FormContrasenna
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from utils.excel_utils.photos_model import Photo, PhotoNext
from models.datos import Datos
from models.inscripciones import Inscripciones
from utils.bcrypt import bcrypt
from models.juntaDirectiva import JuntaDirectiva
from models.actividades import Actividades
from models.usuarios import Usuarios
from models.contactanos import Contactanos
from utils.db import db
from utils.cryptography import CryptographyToken
from utils.random_images import STRING_SHARING, get_random_images_list, randoString

main = Blueprint("main", __name__)


@main.route("/")
def home():

    if not Datos.query.all():
        datos = Datos(20, 20, 20, 20)
        db.session.add(datos)
        db.session.commit()

    img_random = get_random_images_list()

    fotos_data = [
        Photo(
            url=STRING_SHARING + "=" + i,
            desc=f"",
        )
        for i in img_random
    ]

    datosList = Datos.query.filter_by(idDatos=1)

    actividadesActivas = Actividades.query.filter_by(estado=2).all()
    return render_template(
        "main/home.html",
        fotos_data=fotos_data,
        user=current_user,
        actividadesActivas=actividadesActivas,
        datosList=datosList,
    )


@main.route("/about")
def about():
    print(get_view_registro_academico_per_act(3))
    JDList = JuntaDirectiva.query.all()
    return render_template("main/about.html", JDList=JDList, user=current_user)


@main.route("/activities")
def activities():
    activitiesList = Actividades.query.all()
    ins_act = db.session.query(Actividades.idActividad).join(Inscripciones).join(Usuarios).filter(Inscripciones.idVoluntario == current_user.idVoluntario).all() if current_user.is_authenticated else []  # type: ignore
    inscrip_acti = [act.idActividad for act in ins_act]
    return render_template(
        "main/activities.html",
        activitiesList=activitiesList,
        user=current_user,
        ins_act=inscrip_acti,
    )


@main.route("/activities/inscripcion/<string:idActividad>", methods=["GET", "POST"])
@login_required
def inscripcion(idActividad):
    idVoluntario = current_user.idVoluntario  # type: ignore
    estadoAsistencia = 1
    estadoPago = 2
    cantidadKg = 0
    horastotales = 0
    evidencia  = 1
    newIns = Inscripciones(
        idVoluntario,
        idActividad,
        estadoAsistencia,
        estadoPago,
        cantidadKg,
        horastotales,
        evidencia
    )
    print(newIns)
    db.session.add(newIns)
    db.session.commit()
    return redirect(url_for("main.activities", idActividad=idActividad))


@main.route("/contact", methods=["POST", "GET"])
def contact():
    form = FormContactanos()
    if form.validate_on_submit():
        nombre = form.nombre.data
        apellido = form.apellido.data
        telefono = form.telefono.data
        text_area = form.text_area.data
        "".startswith
        newMessage = Contactanos(
            nombre,
            apellido,
            telefono,
            text_area
            if not text_area.startswith("Reset password>>")
            else text_area.replace("Reset password>>", ""),
            False,
        )
        db.session.add(newMessage)
        db.session.commit()
        return redirect(url_for("main.contact", is_posted=True))

    is_posted = request.args.get("is_posted") if "is_posted" in request.args else False
    return render_template(
        "main/contact.html", form=form, user=current_user, is_posted=is_posted
    )


@main.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        correo = form.correo.data
        contra = form.contrasenna.data
        user = Usuarios.query.filter_by(correo=correo).first()
        if user:
            if bcrypt.check_password_hash(user.contrasenna, contra):
                login_user(user)

                return redirect(url_for("main.home"))
    return render_template("main/login.html", form=form, user=current_user)


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@main.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        correo = form.correo.data
        nombre = form.nombre.data
        apellido = form.apellido.data
        telefono = form.telefono.data
        password = form.contrasenna.data
        hashed_password = bcrypt.generate_password_hash(password)
        carrera = form.carrera.data
        departamento="Trips" if correo == "20204055@esen.edu.sv" else "NA"
        cargo = "Admin" if correo == "20204055@esen.edu.sv" else "NA"
        anno = [int(i) for i in list(correo)[0:4]]
        annoo = int("".join(map(str, anno)))
        print(type(annoo))

        newUser = Usuarios(
            correo,
            hashed_password,
            nombre,
            apellido,
            telefono,
            cargo,
            departamento,
            carrera,
            annoo,
        )
        db.session.add(newUser)
        db.session.commit()

        return redirect(url_for("main.login"))
    elif form.is_submitted():
        for field, error in form.errors.items():
            flash(f"{error[0]}")
    return render_template("main/register.html", form=form, user=current_user)


@main.route("/profile")
@login_required
def profile():
    actividades_dict = {}
    ins_act = []
    inscripciones = Inscripciones.query.filter_by(idVoluntario=current_user.idVoluntario).all()  # type: ignore
    for ins in inscripciones:
        if ins.idActividad not in actividades_dict:
            activity = Actividades.query.get(ins.idActividad)
            actividades_dict[ins.idActividad] = activity
        ins_act.append((ins, actividades_dict[ins.idActividad]))
    return render_template("main/profile.html", user=current_user, ins_act=ins_act)


@main.route("/desinscribirse/<int:insc>")
@login_required
def desinscribirse(insc):
    inscripcion = Inscripciones.query.get(insc)
    db.session.delete(inscripcion)
    db.session.commit()
    return redirect(url_for("main.profile"))


@main.route(f"/{randoString(20)}", methods=["POST", "GET"])
def password_refresh():
    form = FormPeticionContrasenna()
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(correo=form.correo.data).first()
        msg = Contactanos(
            user.nombre,
            user.apellido,
            user.telefono,
            f"Reset password>>{user.correo};{user.idVoluntario}",
            False,
        )
        db.session.add(msg)
        db.session.commit()
        return redirect(url_for("main.home"))
    return render_template("main/peticion_reset.html", form=form, user=current_user)


@main.route(f"/reset/password/<id>/<correo_init>", methods=["POST", "GET"])
def password_reset(id, correo_init):
    form = FormContrasenna()
    cryptography_tool = CryptographyToken()
    if form.validate_on_submit():
        correo = form.correo.data
        if int(id) in [
            user.idVoluntario for user in Usuarios.query.all()
        ] and correo.startswith(cryptography_tool.decrypt_token(correo_init)):
            newUser = Usuarios.query.filter_by(correo=correo, idVoluntario=id).first()
            newUser.contrasenna = bcrypt.generate_password_hash(form.contrasenna.data)
            db.session.add(newUser)
            print("updated")
            db.session.commit()
        return redirect(url_for("main.home"))
    id_user = cryptography_tool.decrypt_token(id)
    return render_template(
        "main/reset_password.html",
        form=form,
        user=current_user,
        id=id_user,
        correo_init=correo_init,
    )
