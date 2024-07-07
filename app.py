from flask import Flask, request, jsonify

app = Flask(__name__)

# Cache simulado com um dicionário
clientes_cache = {}

@app.route('/')
def hello_world():
	return 'Olá, Mundo!'

@app.route('/cliente', methods=['POST'])
def adicionar_cliente():
	dados = request.json
	if not dados or 'nome' not in dados or 'telefone' not in dados:
		return jsonify({'erro': 'Os campos nome e telefone são obrigatórios'}), 400
	telefone = dados['telefone']
	clientes_cache[telefone] = {'nome': dados['nome'], 'telefone': telefone}
	return jsonify({'mensagem': 'Cliente adicionado com sucesso'}), 201

@app.route('/cliente/<telefone>', methods=['GET'])
def consultar_cliente(telefone):
	cliente = clientes_cache.get(telefone)
	if cliente:
		return jsonify(cliente), 200
	else:
		return jsonify({'erro': 'Cliente não encontrado'}), 404


@app.route('/clientes/<iniciais>', methods=['GET'])
def consultar_clientes_por_iniciais(iniciais):
	clientes_filtrados = [
		cliente for cliente in clientes_cache.values()
		if cliente['nome'].lower().startswith(iniciais.lower())
	]
	if clientes_filtrados:
		return jsonify(clientes_filtrados), 200
	else:
		return jsonify({'mensagem': 'Nenhum cliente encontrado com essas iniciais'}), 404

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
