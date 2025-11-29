# COMMENTS BLUEPRINT

from flask import Blueprint, jsonify, request, make_response
from bson import ObjectId
from globals import weather_collection
from decorators import jwt_required
import uuid
import datetime

comments_bp = Blueprint("comments_bp", __name__)


# POST /weather/<id>/comments
# USERS - Add a comment to a weather record

@comments_bp.route('/weather/<string:record_id>/comments', methods=['POST'])
@jwt_required
def addComment(record_id):
    # Try to accept both form-data and JSON
    data = request.form.to_dict() if request.form else request.get_json(silent=True) or {}

    # Debug check 
    print(" Received comment data:", data)

    username = data.get("username")
    comment = data.get("comment")
    rating = data.get("rating", 0)

    if not username or not comment:
        return make_response(jsonify({
            "Error": "Missing required field",
            "Received": data  # <-- helpful to debug what Flask actually got
        }), 400)

    new_comment = {
        "_id": str(uuid.uuid4()),
        "username": username,
        "comment": comment,
        "rating": int(rating),
        "created_at": datetime.datetime.utcnow()
    }

    result = weather_collection.update_one(
        {"_id": ObjectId(record_id)},
        {"$push": {"comments": new_comment}}
    )

    if result.modified_count == 1:
        new_comment_link = f"http://127.0.0.1:5000/weather/{record_id}/comments/{new_comment['_id']}"
        return make_response(jsonify({
            "Message": "Comment added successfully",
            "URL": new_comment_link,
            "Comment": new_comment
        }), 201)
    else:
        return make_response(jsonify({"Error": "Weather record not found"}), 404)


# GET /weather/<id>/comments
# PUBLIC - Get all comments for a record

@comments_bp.route('/weather/<string:record_id>/comments', methods=['GET'])
def getComments(record_id):
    try:
        record = weather_collection.find_one({"_id": ObjectId(record_id)})
        if record:
            return make_response(jsonify({
                "station": record.get("station_name"),
                "comments": record.get("comments", [])
            }), 200)
        else:
            return make_response(jsonify({"Error": "Record not found"}), 404)
    except Exception as e:
        return make_response(jsonify({
            "Error": "Failed to load comments",
            "Details": str(e)
        }), 500)


# PUT /weather/<id>/comments/<comment_id>
# USERS - Update a comment

@comments_bp.route('/weather/<string:record_id>/comments/<string:comment_id>', methods=['PUT'])
@jwt_required
def updateComment(record_id, comment_id):
    data = request.form if request.form else request.get_json()
    update_field = {}

    if data.get("comment"):
        update_field["comments.$.comment"] = data.get("comment")
    if data.get("rating"):
        update_field["comments.$.rating"] = int(data.get("rating"))

    if not update_field:
        return make_response(jsonify({"Error": "No valid data provided"}), 400)

    try:
        result = weather_collection.update_one(
            {"_id": ObjectId(record_id), "comments._id": comment_id},
            {"$set": update_field}
        )

        if result.modified_count == 1:
            return make_response(jsonify({
                "Message": "Comment updated successfully"
            }), 200)
        else:
            return make_response(jsonify({"Error": "Comment not found"}), 404)
    except Exception as e:
        return make_response(jsonify({
            "Error": "Failed to update comment",
            "Details": str(e)
        }), 500)


# DELETE /weather/<id>/comments/<comment_id>
# USERS - Delete a comment

@comments_bp.route('/weather/<string:record_id>/comments/<string:comment_id>', methods=['DELETE'])
@jwt_required
def deleteComment(record_id, comment_id):
    try:
        result = weather_collection.update_one(
            {"_id": ObjectId(record_id)},
            {"$pull": {"comments": {"_id": comment_id}}}
        )

        if result.modified_count == 1:
            return make_response(jsonify({
                "Message": "Comment deleted successfully"
            }), 200)
        else:
            return make_response(jsonify({"Error": "Comment not found"}), 404)
    except Exception as e:
        return make_response(jsonify({
            "Error": "Failed to delete comment",
            "Details": str(e)
        }), 500)
