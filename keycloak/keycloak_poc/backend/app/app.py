from flask import Flask, jsonify, request
from keycloak.keycloak_poc.backend.app.auth import require_auth

app = Flask(__name__)

@app.route('/api/public', methods=['GET'])
def public():
    return jsonify({'message': 'This is a public endpoint.'})

@app.route('/api/private', methods=['GET'])
@require_auth()
def private():
    return jsonify({'message': 'This is a private endpoint.'})

if __name__ == "__main__":
    app.run(debug=True)
