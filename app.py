from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample in-memory data store
data_store = {}

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data_store)

@app.route('/api/data', methods=['POST'])
def add_data():
    data = request.json
    unique_id = data.get('id')

    if unique_id:
        data_store[unique_id] = data
        return jsonify({"message": f"Data stored successfully for ID: {unique_id}"})
    else:
        return jsonify({"error": "Missing 'id' in the payload"}), 400

@app.route('/api/data/<string:data_id>', methods=['PUT'])
def update_data(data_id):
    if data_id in data_store:
        data = request.json
        data_store[data_id] = data
        return jsonify({"message": f"Data updated successfully for ID: {data_id}"})
    else:
        return jsonify({"error": f"Data not found for ID: {data_id}"}), 404

@app.route('/api/data/<string:data_id>', methods=['DELETE'])
def delete_data(data_id):
    if data_id in data_store:
        del data_store[data_id]
        return jsonify({"message": f"Data deleted successfully for ID: {data_id}"})
    else:
        return jsonify({"error": f"Data not found for ID: {data_id}"}), 404

if __name__ == '__main__':
    app.run(debug=True)