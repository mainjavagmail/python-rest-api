from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import Usuario, UsuarioCadastro, UsuarioLogin, UsuarioLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def cria_bd():
    bd.create_all()

@jwt.token_in_blacklist_loader
def check_blacklist(token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def check_revoked():
    return jsonify({'message': 'You have been logged out.'}), 401

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(Usuario, '/usuarios/<int:usuario_id>')
api.add_resource(UsuarioCadastro, '/cadastro')
api.add_resource(UsuarioLogin, '/login')
api.add_resource(UsuarioLogout, '/logout')

if __name__ == '__main__':
    from sql_alchemy import bd
    bd.init_app(app)
    app.run(debug=True)