
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.modelo_base import ModeloBase
from flask_app.utils.regex import REGEX_CORREO_VALIDO

class Usuario(ModeloBase):

    modelo = 'usuarios'
    campos = ['first_name','last_name','email','password']

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def buscar(cls, dato):
        query = "SELECT * FROM usuarios WHERE email = %(dato)s"
        data = { 'dato' : dato }
        results = connectToMySQL("db_transcripcion").query_db(query, data)
        print(results)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def update(cls,data):
        query = """UPDATE usuarios 
                        SET first_name = %(first_name)s,
                        last_name = %(last_name)s,
                        email = %(email)s,
                        password = %(password)s,
                        updated_at=NOW() 
                    WHERE id = %(id)s"""
        resultado = connectToMySQL("db_transcripcion").query_db(query, data)
        print("RESULTADO: ", resultado)
        return resultado

    @staticmethod
    def validar_largo(data, campo, largo):
        is_valid = True
        if len(data[campo]) <= largo:
            flash(f'El largo del {campo} no puede ser menor o igual {largo}', 'error')
            is_valid = False
        return is_valid

    @classmethod
    def validar(cls, data):

        is_valid = True

        is_valid = cls.validar_largo(data, 'first_name', 2)
        is_valid = cls.validar_largo(data, 'last_name', 2)

        if not REGEX_CORREO_VALIDO.match(data['email']):
            flash('El correo no es válido', 'error')
            is_valid = False

        if data['password'] != data['cpassword']:
            flash('las contraseñas no son iguales', 'error')
            is_valid = False

        if cls.validar_existe('email', data['email']):
            flash('el correo ya fue ingresado', 'error')
            is_valid = False

        return is_valid

    @classmethod
    def get_all_comments(cls):
        query = f"SELECT * FROM {cls.modelo} RIGHT JOIN pensamientos ON pensamientos.user_id = users.id;"
        results = connectToMySQL("db_transcripcion").query_db(query)

        all_likes = []
        all_data = []
        for data in results:
            
            user_data={
                'id': data['id'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'pensamiento': data['pensamiento'],
                'like': data['like']
            }
            all_likes.append(user_data)
            all_data.append(user_data)


        Usuario.pensamiento = all_data
            
            
        return all_data
        