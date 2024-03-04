import pymongo
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from flask_swagger_ui import get_swaggerui_blueprint
from pymongo import MongoClient
from bson import json_util
import json
import redis
import uuid

app = Flask(__name__)
CORS(app)

# PostgreSQL master connection
postgres_master_conn = psycopg2.connect(
    dbname="master_db",
    user="master_user",
    password="master_password",
    host="postgres_master"
)

# Check if users table exists, if not create it
def create_postgres_table():
    try:
        cursor = postgres_master_conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")
        postgres_master_conn.commit()
        cursor.close()
        print("PostgreSQL users table created successfully")
    except Exception as e:
        print("Error creating PostgreSQL users table:", str(e))

create_postgres_table()

# MongoDB connection
mongo_client = MongoClient('mongo_primary:27017')
mongo_db = mongo_client['content']
mongo_collection = mongo_db['content_collection']

# Check if content_collection exists, if not create it
def create_mongo_collection():
    try:
        mongo_collection.create_index([("title", 1)], unique=True)
        print("MongoDB content_collection created successfully")
    except Exception as e:
        print("Error creating MongoDB content_collection:", str(e))

create_mongo_collection()

# Redis connection
redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

# Check if Redis is available
def check_redis():
    try:
        redis_client.ping()
        return True
    except Exception as e:
        print("Error connecting to Redis:", str(e))
        return False

# Check if PostgreSQL is available
def check_postgres():
    try:
        cursor = postgres_master_conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        return True
    except Exception as e:
        print("Error connecting to PostgreSQL:", str(e))
        return False

# Check if MongoDB is available
def check_mongo():
    try:
        mongo_db.command('ping')
        return True
    except Exception as e:
        print("Error connecting to MongoDB:", str(e))
        return False

# Replicate data to PostgreSQL slave after each request
def replicate_postgres_data():
    try:
        conn = psycopg2.connect(
            dbname="master_db",
            user="replication_user",
            password="replication_password",
            host="postgres_slave1"
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        cursor.execute("INSERT INTO users SELECT * FROM master_db.public.users")
        conn.commit()
        cursor.close()
        conn.close()
        print("PostgreSQL data replicated successfully")
    except Exception as e:
        print("Error replicating PostgreSQL data:", str(e))

# Routes for Users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        cursor = postgres_master_conn.cursor()
        cursor.execute("SELECT * FROM users")
        users_pg = cursor.fetchall()
        cursor.close()

        # Get users from MongoDB
        content = mongo_collection.find()
        users_mongo = [json.loads(json_util.dumps(doc)) for doc in content]

        # Get users from Redis (just an example)
        users_redis = []
        redis_keys = redis_client.keys("*")
        for key in redis_keys:
            user_data = redis_client.hgetall(key)
            users_redis.append(user_data)

        return jsonify({
            "PostgreSQL Users": users_pg,
            "MongoDB Users": users_mongo,
            "Redis Users": users_redis
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        cursor = postgres_master_conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (data['name'], data['email']))
        postgres_master_conn.commit()
        cursor.close()
        replicate_postgres_data()  # Replicate data after inserting
        return jsonify({"message": "User created successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['PUT'])
def update_user():
    try:
        data = request.json
        cursor = postgres_master_conn.cursor()
        cursor.execute("UPDATE users SET email = %s WHERE name = %s", (data['email'], data['name']))
        postgres_master_conn.commit()
        cursor.close()
        replicate_postgres_data()  # Replicate data after updating
        return jsonify({"message": "User updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Routes for Content
@app.route('/content', methods=['GET'])
def get_content():
    try:
        content = mongo_collection.find()
        content_serializable = [json.loads(json_util.dumps(doc)) for doc in content]
        return jsonify(content_serializable)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mongo-data', methods=['POST'])
def create_mongo_data():
    try:
        data = request.json
        # Generate a random UUID as the initial title
        data['title'] = str(uuid.uuid4())

        # Check if the generated title already exists in the collection
        while mongo_collection.find_one({'title': data['title']}):
            data['title'] = str(uuid.uuid4())  # Regenerate a new title

        # Insert the document with the unique title
        mongo_collection.insert_one(data)

        return jsonify({"message": "Data inserted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/content', methods=['PUT'])
def update_content():
    try:
        data = request.json
        query = {"title": data['title']}
        new_values = {"$set": {"content": data['content']}}
        mongo_collection.update_one(query, new_values)
        return jsonify({"message": "Content updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Coordinator endpoint
@app.route('/two-phase-commit', methods=['POST'])
def two_phase_commit():
    # Implement your two-phase commit logic here
    return jsonify({"message": "Two-phase commit logic executed successfully"})

# Swagger UI Blueprint
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Swagger JSON Endpoint
@app.route('/static/swagger.json')
def swagger_json():
    return app.send_static_file('swagger.json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
