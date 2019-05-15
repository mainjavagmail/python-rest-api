from flask_restful import Resource, reqparse
from sql_alchemy import bd
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import pymysql


def normalize_path_params(cidade=None, estrelas_min=0, estrelas_max=5, diaria_min=0, diaria_max=10000, limit=50, offset=0, **dados):
    if cidade:
        return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset
        }
    return {
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset
    }


path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=int)
path_params.add_argument('offset', type=int)


class Hoteis(Resource):  # extende o recurso Resource que tem GET, POST, PUT E DELETE pré estabelecidos
    def get(self):
        connection = pymysql.connect(host='localhost',
                                     user='vitor',
                                     password='a',
                                     db='banco',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave]
                         for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('cidade'):
            consulta = "select * from hoteis where estrelas between %s and %s and diaria between %s and %s limit %s offset %s;"
        else:
            consulta = "select * from hoteis where estrelas between %s and %s and diaria between %s and %s and cidade = %s limit %s offset %s;"

        tupla = tuple([parametros[chave] for chave in parametros])
        cursor.execute(consulta, tupla)
        resultado = cursor.fetchall()

        connection.commit()
        cursor.close()
        connection.close()

        if not resultado:
            return {'message': 'No results to show'}, 200

        hoteis = []
        for linha in resultado:
            hoteis.append(linha)

        return {'hoteis': hoteis}


class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True,
                           help="'nome' can't be empty")
    atributos.add_argument('estrelas', type=float,
                           required=True, help="'estrlas' can't be empty")
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json(), 200
        return {'message': 'Hotel id {} not found.'.format(hotel_id)}, 404

    @jwt_required
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': 'Hotel id {} already exists.'.format(hotel_id)}, 400

        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save()
        except:
            return {'message': 'An internal error ocurred, please try again later.'}, 500
        return hotel.json(), 200

    @jwt_required
    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update(**dados)
            hotel_encontrado.save()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save()
        except:
            return {'message': 'An internal error ocurred, please try again later.'}, 500
        return hotel.json(), 201

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete()
            except:
                return {'message': 'An internal error ocurred, please try again later.'}, 500
            return {'message': 'Hotel {} deleted.'.format(hotel.nome)}, 200
        return {'message': 'Hotel id {} not found'.format(hotel_id)}, 404
