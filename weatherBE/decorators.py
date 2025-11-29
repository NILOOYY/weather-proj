# DECORATORS MODULE — Authentication and Authorization for Weather API

from flask import request, jsonify, make_response
from functools import wraps
import jwt
from globals import SECRET_KEY, blacklist

# JWT REQUIRED - For any logged-in user
# This is used for all routes that require user authentication (both user and admin).
def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        token = None

        # Token from request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response(jsonify({"message": "Token is missing"}), 401)

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({"message": "Token expired"}), 401)
        except Exception:
            return make_response(jsonify({"message": "Invalid token"}), 401)

        # Check if token was blacklisted (user logged out)
        bl_token = blacklist.find_one({'token': token})
        if bl_token is not None:
            return make_response(jsonify({"message": "Token has been cancelled"}), 401)

        return func(*args, **kwargs)
    return jwt_required_wrapper


# ADMIN REQUIRED - For Admin-only
def admin_required(func):
    @wraps(func)
    def admin_required_wrapper(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({"message": "Token missing"}), 401)

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if not data.get('admin', False):
                return make_response(jsonify({"message": "Admin access required"}), 403)
        except Exception:
            return make_response(jsonify({"message": "Invalid token"}), 401)

        return func(*args, **kwargs)
    return admin_required_wrapper


