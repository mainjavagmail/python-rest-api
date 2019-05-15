from sql_alchemy import bd


class UsuarioModel(bd.Model):
    __tablename__ = 'usuarios'

    usuario_id = bd.Column(bd.Integer, primary_key=True)
    login = bd.Column(bd.String(40))
    senha = bd.Column(bd.String(95))

    def __init__(self, login, senha):
        self.login = login
        self.senha = senha

    def json(self):
        return {
            'usuario_id': self.usuario_id,
            'login': self.login
        }

    @classmethod
    def find_usuario(cls, usuario_id):
        usuario = cls.query.filter_by(usuario_id=usuario_id).first()
        if usuario:
            return usuario
        return None

    @classmethod
    def find_usuario_by_login(cls, login):
        usuario = cls.query.filter_by(login=login).first()
        if usuario:
            return usuario
        return None

    def save(self):
        bd.session.add(self)
        bd.session.commit()

    def delete(self):
        bd.session.delete(self)
        bd.session.commit()
