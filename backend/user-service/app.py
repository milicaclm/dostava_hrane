#servis za upravljanje nalozima

from flask import Flask, jsonify, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from neo4j import GraphDatabase

app = Flask(__name__)



driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "password"))


@app.route('/')
def hello():
    return "Hello, User Service!"

@app.route('/users')
def get_users():
    with driver.session() as session:
        result = session.run("MATCH (u:User) RETURN u")
        users = []
        for record in result:
            user_node = record["u"]
            users.append({
                "id": user_node["id"],
                "name": user_node["name"],
                "surname": user_node["surname"],
                "email": user_node["email"],
                "phone_number": user_node["phone_number"],
                "account_type": user_node["account_type"],
                "is_active": user_node["is_active"]
            })
    return jsonify(users)

@app.route('/users/<user_id>')
def get_user(user_id):
    with driver.session() as session:
        result = session.run("MATCH (u:User {id: $user_id}) RETURN u", user_id=user_id)
        record = result.single()
        if record:
            user_node = record["u"]
            user = {
                "id": user_node["id"],
                "name": user_node["name"],
                "surname": user_node["surname"],
                "email": user_node["email"],
                "phone_number": user_node["phone_number"],
                "account_type": user_node["account_type"],
                "is_active": user_node["is_active"]
            }
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404
        
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    with driver.session() as session:
        session.run(
            "CREATE (u:User {id: $id, name: $name, surname: $surname, email: $email, phone_number: $phone_number, account_type: $account_type, is_active: $is_active, password: $password})",
            id=data["id"],
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            phone_number=data["phone_number"],
            account_type=data["account_type"],
            is_active=data["is_active"],
            password=data["password"]
        )
    return jsonify({"message": "User created successfully"}), 201

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User {id: $user_id}) SET u.name = $name, u.surname = $surname, u.email = $email, u.phone_number = $phone_number, u.account_type = $account_type, u.is_active = $is_active, u.password = $password RETURN u",
            user_id=user_id,
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            phone_number=data["phone_number"],
            account_type=data["account_type"],
            is_active=data["is_active"],
            password=data["password"]
        )
        record = result.single()
        if record:
            user_node = record["u"]
            user = {
                "id": user_node["id"],
                "name": user_node["name"],
                "surname": user_node["surname"],
                "email": user_node["email"],
                "phone_number": user_node["phone_number"],
                "account_type": user_node["account_type"],
                "is_active": user_node["is_active"]
            }
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    with driver.session() as session:
        result = session.run("MATCH (u:User {id: $user_id}) DELETE u RETURN COUNT(u) AS deleted_count", user_id=user_id)
        record = result.single()
        if record["deleted_count"] > 0:
            return jsonify({"message": "User deleted successfully"})
        else:
            return jsonify({"error": "User not found"}), 404
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
