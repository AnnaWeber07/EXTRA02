import random
import string
import json
import time
import requests
from retry import retry

# Function to generate random user data
def generate_random_user():
    name = ''.join(random.choices(string.ascii_letters, k=8))
    email = f"{name}@example.com"
    return {"name": name, "email": email}

# Function to generate random content data
def generate_random_content():
    title = ''.join(random.choices(string.ascii_letters, k=10))
    content = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    return {"title": title, "content": content}

@retry(ConnectionError, delay=1, backoff=2, tries=5)
def send_create_user_request():
    url = "http://127.0.0.1:5000/users"
    data = generate_random_user()
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    try:
        print("Create User Response:", response.json())
    except json.JSONDecodeError:
        print("Create User Response (Failed to decode JSON):", response.content)

@retry(ConnectionError, delay=1, backoff=2, tries=5)
def send_create_content_request():
    url = "http://127.0.0.1:5000/content"
    data = generate_random_content()
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    try:
        print("Create Content Response:", response.json())
    except json.JSONDecodeError:
        print("Create Content Response (Failed to decode JSON):", response.content)

@retry(ConnectionError, delay=1, backoff=2, tries=5)
def send_update_user_request():
    url = "http://127.0.0.1:5000/users"
    data = generate_random_user()
    headers = {'Content-Type': 'application/json'}
    response = requests.put(url, headers=headers, data=json.dumps(data))
    try:
        print("Update User Response:", response.json())
    except json.JSONDecodeError:
        print("Update User Response (Failed to decode JSON):", response.content)

@retry(ConnectionError, delay=1, backoff=2, tries=5)
def send_update_content_request():
    url = "http://127.0.0.1:5000/content"
    data = generate_random_content()
    headers = {'Content-Type': 'application/json'}
    response = requests.put(url, headers=headers, data=json.dumps(data))
    try:
        print("Update Content Response:", response.json())
    except json.JSONDecodeError:
        print("Update Content Response (Failed to decode JSON):", response.content)

@retry(ConnectionError, delay=1, backoff=2, tries=5)
def send_two_phase_commit_request():
    url = "http://127.0.0.1:5000/two-phase-commit"
    response = requests.post(url)
    try:
        print("Two-Phase Commit Response:", response.json())
    except json.JSONDecodeError:
        print("Two-Phase Commit Response (Failed to decode JSON):", response.content)

if __name__ == "__main__":
    for _ in range(5):
        send_create_user_request()
        send_create_content_request()
        send_update_user_request()
        send_update_content_request()
        send_two_phase_commit_request()
        time.sleep(1)
