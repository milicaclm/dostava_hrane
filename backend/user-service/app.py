#servis za upravljanje nalozima

import uuid
from flask import Flask, jsonify, request
from neo4j import GraphDatabase
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
# configure JWT
app.config['JWT_SECRET_KEY'] = 'dev-secret-key'
JWTManager(app)



driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "password"))
try:
    with driver.session() as _session:
        # ensure unique id constraint exists
        _session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE")
except Exception:
    # if Neo4j isn't ready yet, ignore — it will be created later
    pass




@app.route('/')
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
                "is_active": user_node["is_active"],
                "password": user_node["password"]
            })
    return jsonify(users)

@app.route('/<user_id>')
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
        


@app.route('/<user_id>', methods=['PUT'])
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

@app.route('/<user_id>', methods=['DELETE'])
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


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    with driver.session() as session:
        result = session.run("MATCH (u:User {email: $email, password: $password}) RETURN u", email=email, password=password)
        record = result.single()
        if record:
            user_node = record["u"]
            access_token = create_access_token(identity=user_node["id"])
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
        
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    with driver.session() as session:
        # generate UUID if client didn't provide an id
        user_id = data.get("id") if data.get("id") else str(uuid.uuid4())
        session.run(
            "CREATE (u:User {id: $id, name: $name, surname: $surname, email: $email, phone_number: $phone_number, account_type: $account_type, is_active: $is_active, password: $password})",
            id=user_id,
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            phone_number=data["phone_number"],
            account_type=data["account_type"],
            is_active=data["is_active"],
            password=data["password"]
        )
    return jsonify({"message": "User created successfully", "id": user_id}), 201