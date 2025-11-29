#------ AUTH BLUEPRINT (for Weather API Users)-------#


from flask import Blueprint, jsonify, request, make_response
from globals import users, blacklist, SECRET_KEY
from functools import wraps
import jwt
import datetime
import bcrypt

auth_bp = Blueprint("auth_bp", __name__)


#---------- Helper Decorator - Token Validation (Login Req)-------------#

def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Accept multiple header names for flexibility
        token = (
            request.headers.get('x-access-token')
            or request.headers.get('access-token')
            or request.headers.get('Authorization')
            or request.headers.get('authorization')
        )

        if not token:
            return make_response(jsonify({"message": "Token is missing"}), 401)

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({"message": "Token expired"}), 401)
        except Exception:
            return make_response(jsonify({"message": "Invalid token"}), 401)

#--------------------- Check blacklist (if user logged out)-------------------#
        if blacklist.find_one({'token': token}):
            return make_response(jsonify({"message": "Token has been cancelled"}), 401)

        # Attach decoded token data to request for later use
        request.user_data = data
        return func(*args, **kwargs)
    return wrapper



#-------------------Helper Decorator - Admin Only-------------------#

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = (
            request.headers.get('x-access-token')
            or request.headers.get('access-token')
            or request.headers.get('Authorization')
            or request.headers.get('authorization')
        )

        if not token:
            return make_response(jsonify({"message": "Token missing"}), 401)
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if not data.get('admin', False):
                return make_response(jsonify({"message": "Admin access required"}), 403)
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({"message": "Token expired"}), 401)
        except Exception:
            return make_response(jsonify({"message": "Invalid token"}), 401)

        return func(*args, **kwargs)
    return wrapper



# POST /register
# PUBLIC - Register a new weather user
@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.form
    if not data or not data.get("username") or not data.get("password"):
        return make_response(jsonify({"Error": "Missing username or password"}), 400)

    if users.find_one({"username": data["username"]}):
        return make_response(jsonify({"Error": "Username already exists"}), 400)

    hashed_pw = bcrypt.hashpw(bytes(data["password"], 'utf-8'), bcrypt.gensalt())
    new_user = {
        "username": data["username"],
        "password": hashed_pw,
        "admin": bool(data.get("admin", False))
    }

    users.insert_one(new_user)
    return make_response(jsonify({
        "message": "User registered successfully",
        "username": data["username"]
    }), 201)



# POST /login
# PUBLIC - Login and get JWT token
@auth_bp.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(jsonify({"message": "Missing login credentials"}), 401)

    user = users.find_one({"username": auth.username})
    if user is None:
        return make_response(jsonify({"message": "Invalid username"}), 401)

    if not bcrypt.checkpw(bytes(auth.password, 'utf-8'), user['password']):
        return make_response(jsonify({"message": "Invalid password"}), 401)

    token = jwt.encode({
        'user': auth.username,
        'admin': user.get('admin', False),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, SECRET_KEY, algorithm='HS256')

    return make_response(jsonify({'token': token}), 200)


# POST /logout
# USERS - Logout (Blacklist token)
@auth_bp.route('/logout', methods=['POST'])
@jwt_required
def logout_user():
    token = (
        request.headers.get('x-access-token')
        or request.headers.get('access-token')
        or request.headers.get('Authorization')
        or request.headers.get('authorization')
    )

    if token:
        blacklist.insert_one({'token': token})
        return make_response(jsonify({"message": "Logout successful"}), 200)
    else:
        return make_response(jsonify({"message": "Token missing"}), 401)


# POST /token/refresh
# USERS - Refresh token (get a new one)
@auth_bp.route('/token/refresh', methods=['POST'])
@jwt_required
def refresh_token():
    """
    Refresh the user's JWT token before it expires.
    Requires a valid, non-blacklisted token.
    """
#-------------Extract the current token from headers------------#
    token = (
        request.headers.get('x-access-token')
        or request.headers.get('access-token')
        or request.headers.get('Authorization')
        or request.headers.get('authorization')
    )

    try:
        # Decode existing token
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return make_response(jsonify({"message": "Token expired. Please log in again."}), 401)
    except Exception:
        return make_response(jsonify({"message": "Invalid token"}), 401)

#------------Create a new token with extended expiry-------------#
    new_token = jwt.encode({
        'user': data['user'],
        'admin': data.get('admin', False),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, SECRET_KEY, algorithm='HS256')

    return make_response(jsonify({
        "message": "Token refreshed successfully",
        "token": new_token
    }), 200)
