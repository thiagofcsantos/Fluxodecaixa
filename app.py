from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
app = Flask(__name__)

# Configuração do banco de dados SQLite
database_path = os.path.join(os.getcwd(), 'movimentacoes.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da Tabela Movimentacao
class Movimentacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)  # 'entrada' ou 'saida'
    valor = db.Column(db.Float, nullable=False)  # Valor da movimentação
    data_inclusao = db.Column(db.DateTime, default=datetime.utcnow)

# Criar a tabela no banco de dados
with app.app_context():
    db.create_all()

# Rota para adicionar uma movimentação
@app.route('/movimentacao', methods=['POST'])
def adicionar_movimentacao():
    dados = request.get_json()
    tipo = dados.get('tipo')
    valor = dados.get('valor')


    if tipo not in ['entrada', 'saida']:
        return jsonify({'erro': 'Tipo de movimentação inválido. Use "entrada" ou "saida".'}), 400

    if not isinstance(valor, (int, float)) or valor <= 0:
        return jsonify({'erro': 'O valor deve ser um número positivo.'}), 400

    try:
        nova_movimentacao = Movimentacao(tipo=tipo, valor=valor)

       #print(nova_movimentacao)
        db.session.add(nova_movimentacao)
        db.session.commit()  # Commit para salvar a movimentação no banco de dados
        return jsonify({'mensagem': 'Movimentação registrada com sucesso!'}), 201
    except Exception as e:
        db.session.rollback()  # Rollback em caso de erro
        return jsonify({'erro': str(e)}), 500  # Exibe o erro no servidor

# Iniciar o servidor Flask
if __name__ == '__main__':
    # Criar o banco de dados e tabelas se não existirem
    with app.app_context():
        db.create_all()  # Cria as tabelas se não existirem

    app.run(debug=True)
