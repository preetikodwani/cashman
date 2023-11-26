from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the data model
class UserData(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, id, name):
        self.id = id
        self.name = name

# Create tables
with app.app_context():
    db.create_all()

@app.route('/api/retrieve/<string:user_id>', methods=['GET'])
def retrieve_data(user_id):
    user_data = UserData.query.get(user_id)
    if user_data:
        return jsonify({"message": f"Welcome back, {user_data.name}!"})
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/api/store', methods=['POST'])
def store_data():
    data = request.get_json()
    user_id = generate_unique_id(data['name'])

    new_user = UserData(id=user_id, name=data['name'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"Welcome, {data['name']}! Data stored successfully.", "user_id": user_id})

@app.route('/api/edit/<string:user_id>', methods=['PUT'])
def edit_data(user_id):
    user_data = UserData.query.get(user_id)
    if user_data:
        data = request.get_json()
        user_data.name = data['name']
        db.session.commit()
        return jsonify({"message": f"User data updated successfully for {user_id}"})
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/api/delete/<string:user_id>', methods=['DELETE'])
def delete_data(user_id):
    user_data = UserData.query.get(user_id)
    if user_data:
        db.session.delete(user_data)
        db.session.commit()
        return jsonify({"message": f"User data deleted successfully for {user_id}"})
    else:
        return jsonify({"message": "User not found"}), 404

def generate_unique_id(name):
    # Generate a unique ID based on the user's name (you might want to use a more sophisticated method)
    return name.lower().replace(" ", "_")

if __name__ == '__main__':
    app.run(debug=True)