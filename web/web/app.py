from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# In-memory key-value store
store = {}

# Error handler for 404 Not Found
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify(error=str(error)), 404

# Error handler for 400 Bad Request
@app.errorhandler(400)
def bad_request(error):
    return jsonify(error=str(error)), 400

# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify(error="An internal error occurred"), 500

# Create a new key-value pair
@app.route('/api/v1/store', methods=['POST'])
def create_key_value():
    data = request.get_json()

    if not data or 'key' not in data or 'value' not in data:
        abort(400, description="Invalid input. 'key' and 'value' are required.")
    
    key = data['key']
    value = data['value']

    if key in store:
        abort(400, description="Key already exists")

    store[key] = value
    return jsonify(message="Key-value pair created successfully", key=key, value=value), 201

# Retrieve a value by key
@app.route('/api/v1/store/<string:key>', methods=['GET'])
def get_value(key):
    if key not in store:
        abort(404, description="Key not found")
    
    return jsonify(key=key, value=store[key]), 200

# Update an existing key-value pair
@app.route('/api/v1/store/<string:key>', methods=['PUT'])
def update_value(key):
    if key not in store:
        abort(404, description="Key not found")
    
    data = request.get_json()
    if 'value' not in data:
        abort(400, description="Invalid input. 'value' is required.")
    
    store[key] = data['value']
    return jsonify(message="Key-value pair updated successfully", key=key, value=data['value']), 200

# Delete a key-value pair
@app.route('/api/v1/store/<string:key>', methods=['DELETE'])
def delete_key_value(key):
    if key not in store:
        abort(404, description="Key not found")

    del store[key]
    return jsonify(message="Key-value pair deleted successfully", key=key), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)