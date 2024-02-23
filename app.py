from flask import Flask, request, jsonify
import psycopg2
from pymongo import MongoClient
import redis

app = Flask(__name__)

# PostgreSQL master and slave connections
postgres_master_conn = psycopg2.connect(
    dbname="master_db",
    user="master_user",
    password="master_password",
    host="postgres_master"
)

postgres_slave_conn = psycopg2.connect(
    dbname="slave_db",
    user="slave_user",
    password="slave_password",
    host="postgres_slave1"
)

# MongoDB connection
mongo_client = MongoClient('mongo_primary:27017')
mongo_db = mongo_client['content']
mongo_collection = mongo_db['content_collection']

# Redis cluster connection
redis_cluster = redis.StrictRedisCluster(
    startup_nodes=[{'host': 'redis', 'port': 6379}],
    decode_responses=True
)

@app.route('/users', methods=['GET'])
def get_users():
    cursor = postgres_slave_conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    cursor = postgres_master_conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (data['name'], data['email']))
    postgres_master_conn.commit()
    cursor.close()
    return jsonify({"message": "User created successfully"})

@app.route('/users', methods=['PUT'])
def update_user():
    data = request.json
    cursor = postgres_master_conn.cursor()
    cursor.execute("UPDATE users SET email = %s WHERE name = %s", (data['email'], data['name']))
    postgres_master_conn.commit()
    cursor.close()
    return jsonify({"message": "User updated successfully"})

@app.route('/content', methods=['GET'])
def get_content():
    content = mongo_collection.find()
    return jsonify(list(content))

@app.route('/content', methods=['POST'])
def create_content():
    data = request.json
    mongo_collection.insert_one(data)
    return jsonify({"message": "Content created successfully"})

@app.route('/content', methods=['PUT'])
def update_content():
    data = request.json
    query = {"title": data['title']}
    new_values = {"$set": {"content": data['content']}}
    mongo_collection.update_one(query, new_values)
    return jsonify({"message": "Content updated successfully"})

# Coordinator endpoint (placeholder)
@app.route('/two-phase-commit', methods=['POST'])
def two_phase_commit():
    # Implement your two-phase commit logic here
    return jsonify({"message": "Two-phase commit logic executed successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
