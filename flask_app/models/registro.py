
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.modelo_base import ModeloBase
from flask_app.utils.regex import REGEX_CORREO_VALIDO

class Registro(ModeloBase):

    modelo = 'registros'
    campos = ['usuarios_id', 'registro']

    def __init__(self, data):
        self.id_registros = data['id_registros']
        self.usuarios_id = data['usuarios_id']
        self.registro = data['registro']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def buscar_registro(cls, dato):
        query = f"SELECT * FROM {cls.modelo} WHERE usuarios_id = %(dato)s"
        data = { 'dato' : dato }
        results = connectToMySQL("db_transcripcion").query_db(query, data)
        print('buscar_registro: ',results)
        if len(results) > 0:
            return results
        else:
            return None 

    @classmethod
    def save(cls, data ):

        query = f"INSERT INTO {cls.modelo} (usuarios_id, registro, created_at, updated_at ) VALUES (%(usuarios_id)s, %(registro)s, NOW(),NOW());"
        resultado = connectToMySQL("db_transcripcion").query_db( query, data ) 
        print('resultado save base', resultado)
        return resultado
    
    @classmethod
    def get_by_id(cls, id):
        query = f"SELECT * FROM {cls.modelo} where usuarios_id = %(id)s;"
        data = { 'id' : id }
        results = connectToMySQL("db_transcripcion").query_db(query, data)
        if len(results) > 0:
            return results
        else:
            return None 
    
    
    @classmethod
    def primera (cls, id):
        query = f"SELECT * FROM registros where usuarios_id = %(id)s ORDER by id_registros DESC LIMIT 1;"
        data = { 'id' : id }
        results = connectToMySQL("db_transcripcion").query_db(query, data)
        print(results)
        if len(results) > 0:
            return results
        else:
            return None 