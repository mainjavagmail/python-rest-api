from flask_restful import Resource, reqparse
from models.usuario import UsuarioModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
from werkzeug import generate_password_hash, check_password_hash

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True,
                       help="'login' can't be empty")
atributos.add_argument('senha', type=str, required=True,
                       help="'senha' can't be empty")


class Usuario(Resource):

    def get(self, usuario_id):
        usuario = UsuarioModel.find_usuario(usuario_id)
        if usuario:
            return usuario.json(), 200
        return {'message': 'User {} not found'.format(usuario_id)}, 404

    @jwt_required
    def delete(self, usuario_id):
        usuario = UsuarioModel.find_usuario(usuario_id)
        if usuario:
            try:
                usuario.delete()
                return {'message': 'User {} deleted.'.format(usuario.login)}, 200
            except:
                return {'message': 'Impossible to delete user {} try again later.'.format(usuario.usuario_id)}, 400


class UsuarioCadastro(Resource):
    def post(self):
        dados = atributos.parse_args()
        if UsuarioModel.find_usuario_by_login(dados['login']):
            return {'message': 'login {} already exists!'.format(dados['login'])}, 400

        usuario = UsuarioModel(**dados)
        try:
            usuario.senha = generate_password_hash(usuario.senha)
            print(usuario.senha)
            usuario.save()
            return {'message': 'User {} created.'.format(usuario.usuario_id)}, 201
        except Exception as e:
            print(e)
            return {'message': 'Impossible to save user {}. {}'.format(usuario.login, e)}, 400


class UsuarioLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        usuario = UsuarioModel.find_usuario_by_login(dados['login'])
        if usuario and check_password_hash(usuario.senha, dados.senha):
            token = create_access_token(identity=usuario.usuario_id)
            return {'token': token}, 200
        return {'message': 'username or password incorrect'}, 401


class UsuarioLogout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully.'}, 200
