from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated cache with a dictionary
clients_cache = {}

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/client', methods=['POST'])
def add_client():
	data = request.json
	if not data or 'name' not in data or 'phone' not in data:
		return jsonify({'error': 'The fields name and phone are required'}), 400
	phone = data['phone']
	clients_cache[phone] = {'name': data['name'], 'phone': phone}
	return jsonify({'message': 'Client added successfully'}), 201

@app.route('/client/<phone>', methods=['GET'])
def consult_client(phone):
	client = clients_cache.get(phone)
	if client:
		return jsonify(client), 200
	else:
		return jsonify({'error': 'Client not found'}), 404


@app.route('/clients/<initials>', methods=['GET'])
def consult_clients_by_initials(initials):
	filtered_clients = [
		client for client in clients_cache.values()
		if client['name'].lower().startswith(initials.lower())
	]
	if filtered_clients:
		return jsonify(filtered_clients), 200
	else:
		return jsonify({'message': 'No clients found with these initials'}), 404

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
