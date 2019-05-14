from flask_restful import Resource, reqparse
from sql_alchemy import bd
from models.hotel import HotelModel

# extende o recurso Resource que tem GET, POST, PUT E DELETE pré estabelecidos
class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="'nome' can't be empty")
    atributos.add_argument('estrelas', type=float, required=True, help="'estrlas' can't be empty")
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json(), 200
        return {'message': 'Hotel id {} not found.'.format(hotel_id)}, 404

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

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete()
            except:
                return {'message': 'An internal error ocurred, please try again later.'}, 500
            return {'message': 'Hotel {} deleted.'.format(hotel.nome)}, 200
        return {'message': 'Hotel id {} not found'.format(hotel_id)}, 404
        