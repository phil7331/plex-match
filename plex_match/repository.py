import os
import bcrypt
from pymongo import MongoClient


def init_admin_user():
    username = "admin"
    password = "123"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client['plex-match']
    users_collection = db['users']
    user_data = {
        "username": username,
        "password": hashed_password.decode('utf-8')  # Decode to store as string
    }

    # Check if the user already exists to prevent duplication
    x = users_collection.find_one({"username": username})
    if x:
        print("Admin user already exists")
    else:
        users_collection.insert_one(user_data)
        print("Admin user created successfully")


def find_user_in_db(username: str, password: str):
    # MongoDB connection setup
    client = MongoClient(os.getenv('MONGO_URI'))  # MongoDB URI from environment variable
    db = client['plex-match']  # Replace with your database name
    users_collection = db['users']

    # Find user by username
    user = users_collection.find_one({"username": username})

    # If user is found, check the password
    if user:
        hashed_password = user['password'].encode('utf-8')  # Convert stored password to bytes

        # Compare provided password with stored hashed password
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            print("User authenticated successfully")
            return user
        else:
            print("Invalid password")
            return False
    else:
        print("User not found")
        return False
