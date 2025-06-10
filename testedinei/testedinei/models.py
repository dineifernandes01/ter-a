from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    saldo = db.Column(db.Float, default=0)
    indicou_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    indicados = db.relationship('User', backref=db.backref('indicador', remote_side=[id]))
    historico = db.relationship('Transacao', backref='user', lazy=True)

class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20))  # deposito, saque, rendimento, comissao
    valor = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
