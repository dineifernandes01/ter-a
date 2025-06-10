from flask import Blueprint, request, jsonify
from app import db
from models import User, Transacao

bp = Blueprint('routes', __name__)

@bp.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.json
    ref_id = data.get('ref_id')
    indicou = User.query.get(ref_id) if ref_id else None

    novo_usuario = User(
        nome=data['nome'],
        telefone=data['telefone'],
        email=data['email'],
        indicou_id=indicou.id if indicou else None
    )
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'msg': 'Usuário cadastrado com sucesso!', 'user_id': novo_usuario.id})

@bp.route('/depositar', methods=['POST'])
def depositar():
    data = request.json
    user = User.query.get(data['user_id'])
    valor = data['valor']

    if valor < 20:
        return jsonify({'erro': 'Depósito mínimo é de 20 dólares'}), 400

    user.saldo += valor
    transacao = Transacao(tipo='deposito', valor=valor, user_id=user.id)
    db.session.add(transacao)

    aplicar_comissao(user, valor)

    db.session.commit()
    return jsonify({'msg': 'Depósito registrado e comissões distribuídas com sucesso!'})

def aplicar_comissao(user, valor_depositado):
    niveis = [user.indicador]
    for _ in range(4):
        if niveis[-1] and niveis[-1].indicador:
            niveis.append(niveis[-1].indicador)
        else:
            niveis.append(None)

    porcentagens = [0.10, 0.02, 0.02, 0.02, 0.02]

    for i, indicado in enumerate(niveis):
        if indicado:
            comissao = valor_depositado * porcentagens[i]
            indicado.saldo += comissao
            db.session.add(Transacao(tipo='comissao', valor=comissao, user_id=indicado.id))

@bp.route('/sacar', methods=['POST'])
def sacar():
    data = request.json
    user = User.query.get(data['user_id'])
    valor = data['valor']

    if valor < 20:
        return jsonify({'erro': 'Saque mínimo é de 20 dólares'}), 400
    if valor > user.saldo:
        return jsonify({'erro': 'Saldo insuficiente'}), 400

    user.saldo -= valor
    transacao = Transacao(tipo='saque', valor=valor, user_id=user.id)
    db.session.add(transacao)
    db.session.commit()

    return jsonify({'msg': 'Saque solicitado com sucesso!'})

@bp.route('/aplicar_rendimento', methods=['POST'])
def aplicar_rendimento():
    data = request.json
    user = User.query.get(data['user_id'])
    percentual = data['percentual'] / 100
    rendimento = user.saldo * percentual
    user.saldo += rendimento
    transacao = Transacao(tipo='rendimento', valor=rendimento, user_id=user.id)
    db.session.add(transacao)
    db.session.commit()
    return jsonify({'msg': f'Rendimento de {data["percentual"]}% aplicado com sucesso!'})

@bp.route('/painel_usuario/<int:user_id>')
def painel_usuario(user_id):
    user = User.query.get(user_id)
    transacoes = [{
        'tipo': t.tipo,
        'valor': t.valor
    } for t in user.historico]
    return jsonify({
        'nome': user.nome,
        'saldo': user.saldo,
        'transacoes': transacoes
    })
