from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from modelos import db, Apuesta, ApuestaSchema, Usuario, UsuarioSchema, Carrera, CarreraSchema, CompetidorSchema, \
Competidor, ReporteSchema, Transaccion, TransaccionSchema

apuesta_schema = ApuestaSchema()
carrera_schema = CarreraSchema()
competidor_schema = CompetidorSchema()
usuario_schema = UsuarioSchema()
reporte_schema = ReporteSchema()
transaccion_schema = TransaccionSchema()

class VistaSignIn(Resource):

    def post(self):
        
        validacion = self.validarUsuario(request)
        
        if validacion is not None:
            return "Ya existe un usuario registrado con ese " + validacion, 400
        
        nuevo_usuario = Usuario(usuario=request.json["usuario"], 
                                contrasena=request.json["contrasena"], 
                                nombre=request.json["nombre"],
                                correo=request.json["correo"],
                                tarjeta=request.json["tarjeta"],
                                saldo_promocional=10000,
                                saldo=0,
                                role="GAMBLER")
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity=nuevo_usuario.id,additional_claims={"role": nuevo_usuario.role, "user": nuevo_usuario.usuario, "username": nuevo_usuario.nombre})
        #create_access_token(identity= {"name":"Hello", "age":35} )
        return {"mensaje": "usuario creado exitosamente", "token": token_de_acceso, "id": nuevo_usuario.id}

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena", usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204
    
    def validarUsuario(self, request):
        usuario = db.session.query(Usuario).filter(Usuario.usuario.like(request.json["usuario"])).first()
        if usuario is not None:
            return "identificador"
    
        usuario_correo = db.session.query(Usuario).filter(Usuario.correo.like(request.json["correo"])).first()
        if usuario_correo is not None:
            return "correo"
        
        usuario_nombre = db.session.query(Usuario).filter(Usuario.nombre.like(request.json["nombre"])).first()
        if usuario_nombre is not None:
            return "nombre"      
        


class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                       Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id, additional_claims={"role": usuario.role, "user": usuario.usuario, "username": usuario.nombre})
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}


class VistaCarrerasUsuario(Resource):

    @jwt_required()
    def post(self, id_usuario):
        nueva_carrera = Carrera(nombre_carrera=request.json["nombre"])
        for item in request.json["competidores"]:
            cuota = round((item["probabilidad"] / (1 - item["probabilidad"])), 2)
            competidor = Competidor(nombre_competidor=item["competidor"],
                                    probabilidad=item["probabilidad"],
                                    cuota=cuota,
                                    id_carrera=nueva_carrera.id)
            nueva_carrera.competidores.append(competidor)
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.carreras.append(nueva_carrera)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un carrera con dicho nombre', 409

        return carrera_schema.dump(nueva_carrera)

    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        if "ADMIN" == usuario.role:
            return [carrera_schema.dump(carrera) for carrera in usuario.carreras]
        else:            
            return [carrera_schema.dump(ca) for ca in Carrera.query.filter(Carrera.abierta == 1).all()]


class VistaCarrera(Resource):

    @jwt_required()
    def get(self, id_carrera):
        return carrera_schema.dump(Carrera.query.get_or_404(id_carrera))

    @jwt_required()
    def put(self, id_carrera):
        carrera = Carrera.query.get_or_404(id_carrera)
        carrera.nombre_carrera = request.json.get("nombre", carrera.nombre_carrera)
        carrera.competidores = []

        for item in request.json["competidores"]:
            probabilidad = float(item["probabilidad"])
            cuota = round((probabilidad / (1 - probabilidad)), 2)
            competidor = Competidor(nombre_competidor=item["competidor"],
                                    probabilidad=probabilidad,
                                    cuota=cuota,
                                    id_carrera=carrera.id)
            carrera.competidores.append(competidor)

        db.session.commit()
        return carrera_schema.dump(carrera)

    @jwt_required()
    def delete(self, id_carrera):
        carrera = Carrera.query.get_or_404(id_carrera)
        db.session.delete(carrera)
        db.session.commit()
        return '', 204


class VistaApuestas(Resource):

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()#d
        apostador = Usuario.query.get_or_404(request.json["id_apostador"])
        admin = Usuario.query.get_or_404(1)
        valor_apostado = request.json["valor_apostado"]
        total_apostador = apostador.saldo + apostador.saldo_promocional
        if valor_apostado>=5000: 
            if total_apostador >= valor_apostado:
                nueva_apuesta = Apuesta(valor_apostado=request.json["valor_apostado"],
                                    id_apostador=request.json["id_apostador"], 
                                    id_competidor=request.json["id_competidor"], 
                                    id_carrera=request.json["id_carrera"])
                db.session.add(nueva_apuesta)
                db.session.commit()
                if apostador.saldo_promocional > 0:
                    if apostador.saldo_promocional >= valor_apostado:
                        apostador.saldo_promocional = apostador.saldo_promocional - valor_apostado
                    else:
                        restante = valor_apostado - apostador.saldo_promocional
                        apostador.saldo = apostador.saldo - restante
                        apostador.saldo_promocional = 0
                else:
                    apostador.saldo = apostador.saldo - valor_apostado
                admin.saldo = admin.saldo + valor_apostado
                db.session.commit()
                newapuesta = apuesta_schema.dump(nueva_apuesta)
                self.guardarTransaccion("APUESTA", request, user_id, newapuesta['id'])
                return newapuesta
            else:
                return 'El saldo actual es menor al valor apostado',400
        else:
            return 'El valor a apostar no puede ser menor a $5000',400
   
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        usuario = Usuario.query.filter(Usuario.id == user_id).first()
        if "ADMIN" == usuario.role:
            return [apuesta_schema.dump(ca) for ca in Apuesta.query.all()]
        else:            
            return [apuesta_schema.dump(ca) for ca in Apuesta.query.filter(Apuesta.id_apostador == user_id).all()]

    @jwt_required()
    def patch(self):
        user_id = get_jwt_identity()
        usuario = Usuario.query.get_or_404(user_id)
        usuario.saldo += request.json.get("saldo")
        usuario.saldo_promocional += request.json.get("saldo_promo")
        db.session.commit()
        return usuario_schema.dump(usuario)

    def guardarTransaccion(self, tipotran, request, idusuario, idapuesta):
        nueva_transaccion = Transaccion(tipo_transaccion=tipotran,
                                    valor=request.json["valor_apostado"], 
                                    id_dueno=request.json["id_apostador"], 
                                    id_creador=idusuario,
                                    id_apuesta = idapuesta)
        db.session.add(nueva_transaccion)
        db.session.commit()       

class VistaApuesta(Resource):

    @jwt_required()
    def get(self, id_apuesta):
        return apuesta_schema.dump(Apuesta.query.get_or_404(id_apuesta))

    @jwt_required()
    def put(self, id_apuesta):
        apuesta = Apuesta.query.get_or_404(id_apuesta)
        apuesta.valor_apostado = request.json.get("valor_apostado", apuesta.valor_apostado)
        apuesta.id_apostador = request.json.get("id_apostador", apuesta.id_apostador)
        apuesta.id_competidor = request.json.get("id_competidor", apuesta.id_competidor)
        apuesta.id_carrera = request.json.get("id_carrera", apuesta.id_carrera)
        db.session.commit()
        return apuesta_schema.dump(apuesta)

    @jwt_required()
    def delete(self, id_apuesta):
        apuesta = Apuesta.query.get_or_404(id_apuesta)
        db.session.delete(apuesta)
        db.session.commit()
        return '', 204


class VistaTerminacionCarrera(Resource):

    def put(self, id_competidor):
        competidor = Competidor.query.get_or_404(id_competidor)
        competidor.es_ganador = True
        carrera = Carrera.query.get_or_404(competidor.id_carrera)
        carrera.abierta = False

        for apuesta in carrera.apuestas:
            if apuesta.id_competidor == competidor.id:
                apuesta.ganancia = apuesta.valor_apostado + (apuesta.valor_apostado/competidor.cuota)
            else:
                apuesta.ganancia = 0

        db.session.commit()
        return competidor_schema.dump(competidor)


class VistaReporte(Resource):

    @jwt_required()
    def get(self, id_carrera):
        carreraReporte = Carrera.query.get_or_404(id_carrera)
        ganancia_casa_final = 0

        for apuesta in carreraReporte.apuestas:
            ganancia_casa_final = ganancia_casa_final + apuesta.valor_apostado - apuesta.ganancia

        reporte = dict(carrera=carreraReporte, ganancia_casa=ganancia_casa_final)
        schema = ReporteSchema()
        return schema.dump(reporte)


class VistaUsuarios(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        if user_id == 1:
            return [usuario_schema.dump(ca) for ca in Usuario.query.filter(Usuario.role == "GAMBLER")]
        else:
            return [usuario_schema.dump(ca) for ca in Usuario.query.filter(Usuario.id == user_id)]

class VistaUsuario(Resource):

    @jwt_required()
    def get(self, id_usuario):
        return usuario_schema.dump(Usuario.query.get_or_404(id_usuario))  

class VistaApostador(Resource):

    @jwt_required()
    def get(self, id_apuesta):
        apuesta = Apuesta.query.get_or_404(id_apuesta)
        usuario = Usuario.query.get_or_404(apuesta.id_apostador)
        #return {"nombre": usuario.nombre, "saldo": usuario.saldo + usuario.saldo_promocional
        return usuario_schema.dump(usuario)


class VistaTransacciones(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        #usuario = Usuario.query.filter(Usuario.id == user_id).first()
        usuario = Usuario.query.get_or_404(user_id)
        #return usuario_schema.dump(usuario)
        transacciones = [transaccion_schema.dump(tr) for tr in Transaccion.query.filter(Transaccion.id_dueno == user_id)]
        return {"saldo": usuario.saldo + usuario.saldo_promocional, "tx": transacciones}

    @jwt_required()
    def patch(self):
        user_id = get_jwt_identity()
        usuario = Usuario.query.get_or_404(user_id)
        usuario.saldo += request.json.get("saldo")
        usuario.saldo_promocional += request.json.get("saldo_promo")
        db.session.commit()
        return usuario_schema.dump(usuario)

# class VistaTransacciones(Resource):

#     @jwt_required()
#     def post(self):
#         tipo_transaccion = request.json["tipo_transaccion"]
#         id_dueno = request.json["id_dueno"]
#         usuario_dueno = Usuario.query.get_or_404(id_dueno)
#         if usuario_dueno:
#             role = usuario_dueno.role
        
#         # Apostadores no pueden registrar transacciones tipo GANANCIA o SALDO_PROMO
#         if role == "GAMBLER" and (tipo_transaccion == "GANANCIA" or tipo_transaccion == "SALDO_PROMO"):
#             return "No cuenta con los permisos para registrar transacciones de tipo {}".format(tipo_transaccion), 403

#         nueva_transaccion = Transaccion(tipo_transaccion=tipo_transaccion,
#                                         valor=request.json["valor"],
#                                         id_dueno=id_dueno,
#                                         id_creador=request.json["id_creador"],
#                                         id_apuesta=request.json["id_apuesta"])
#         db.session.add(nueva_transaccion)
#         db.session.commit()
#         return transaccion_schema.dump(nueva_transaccion)

# class VistaTransaccion(Resource):

#     @jwt_required()
#     def get(self, id_dueno):
#         return [transaccion_schema.dump(tr) for tr in Transaccion.query.filter(Transaccion.id_dueno == id_dueno)]

