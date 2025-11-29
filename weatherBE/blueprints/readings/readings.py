
# READINGS BLUEPRINT — Handles Recording and Management of Historical Weather Data

from flask import Blueprint, jsonify, request
from bson import ObjectId
from globals import weather_collection
from decorators import jwt_required
import datetime

# Initialize the blueprint for all reading-related routes
readings_bp = Blueprint("readings_bp", __name__)


# HELPER FUNCTION: _to_objectid()
# Safely converts a string ID to a MongoDB ObjectId.
# Returns None if the ID is invalid.

def _to_objectid(id_str):
    try:
        return ObjectId(id_str)
    except Exception:
        return None

# ROUTE: POST /weather/<id>/readings
# Allows authenticated users to add a new weather reading to a specific station.
# Each reading records temperature, humidity, wind speed, and pressure at a given time.

@readings_bp.route("/weather/<string:station_id>/readings", methods=["POST"])
@jwt_required
def add_reading(station_id):
    # Validate and convert station ID
    oid = _to_objectid(station_id)
    if not oid:
        return jsonify({"error": "Invalid station id"}), 400

    # To accept form or JSON data
    data = request.form or request.get_json(silent=True) or {}
    if not data:
        return jsonify({"error": "Missing reading data"}), 400

    try:
        # Create a new reading object with automatic ID and timestamp
        reading = {
            "_id": str(ObjectId()),  # Unique identifier for the reading
            "ts": data.get("ts") or datetime.datetime.utcnow().isoformat(),
            "temp_c": float(data.get("temp_c", 0)),
            "humidity": float(data.get("humidity", 0)),
            "wind_kmh": float(data.get("wind_kmh", 0)),
            "pressure_kpa": float(data.get("pressure_kpa", 0))
        }

        # Push the new reading into the target weather record
        result = weather_collection.update_one(
            {"_id": oid},
            {"$push": {"readings": reading}}
        )

        # Confirm if insertion was successful
        if result.modified_count == 1:
            return jsonify({
                "message": "Reading added successfully",
                "reading": reading
            }), 201
        else:
            return jsonify({"error": "Weather station not found"}), 404

    # Handle invalid data formats or conversion errors
    except ValueError as ve:
        return jsonify({"error": f"Invalid numeric value: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# ROUTE: GET /weather/<id>/readings
# Public endpoint that retrieves all readings for a specific weather station.

@readings_bp.route("/weather/<string:station_id>/readings", methods=["GET"])
def get_readings(station_id):
    oid = _to_objectid(station_id)
    if not oid:
        return jsonify({"error": "Invalid station id"}), 400

    # Retrieve the document for the specified station
    doc = weather_collection.find_one({"_id": oid}, {"readings": 1, "station_name": 1})
    if not doc:
        return jsonify({"error": "Station not found"}), 404

    readings = doc.get("readings", [])
    if not readings:
        return jsonify({"message": "No readings available for this station"}), 200

    # Apply optional date filters (if provided)
    from_date = request.args.get("from")
    to_date = request.args.get("to")

    if from_date:
        readings = [r for r in readings if r.get("ts") and r["ts"] >= from_date]
    if to_date:
        readings = [r for r in readings if r.get("ts") and r["ts"] <= to_date]

    # Return filtered readings with count
    return jsonify({
        "station": doc.get("station_name"),
        "count": len(readings),
        "readings": readings
    }), 200


# ROUTE: PUT /weather/<station_id>/readings/<reading_id>
# Allows authenticated users to update a specific reading by its ID.
# Users can modify temperature, humidity, wind speed, pressure, or timestamp.
@readings_bp.route("/weather/<string:station_id>/readings/<string:reading_id>", methods=["PUT"])
@jwt_required
def update_reading(station_id, reading_id):
    # Validate and convert station ID
    oid = _to_objectid(station_id)
    if not oid:
        return jsonify({"error": "Invalid station id"}), 400

    # Retrieve updated data
    data = request.form or request.get_json(silent=True) or {}
    if not data:
        return jsonify({"error": "Missing update data"}), 400

    update_fields = {}

    # Process possible numeric updates
    for field in ["temp_c", "humidity", "wind_kmh", "pressure_kpa"]:
        if field in data:
            try:
                update_fields[f"readings.$.{field}"] = float(data[field])
            except ValueError:
                return jsonify({"error": f"Invalid numeric value for {field}"}), 400

    # Allow updating timestamp if provided
    if "ts" in data:
        update_fields["readings.$.ts"] = data["ts"]

    # If no valid data was sent, return an error
    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400

    # Perform the update on the matching reading record
    result = weather_collection.update_one(
        {"_id": oid, "readings._id": reading_id},
        {"$set": update_fields}
    )

    # Confirm successful modification
    if result.modified_count == 1:
        return jsonify({"message": "Reading updated successfully"}), 200
    else:
        return jsonify({"error": "Reading not found"}), 404


# ROUTE: DELETE /weather/<station_id>/readings/<reading_id>
# Allows authenticated users to delete a specific reading from a weather station.

@readings_bp.route("/weather/<string:station_id>/readings/<string:reading_id>", methods=["DELETE"])
@jwt_required
def delete_reading(station_id, reading_id):
    oid = _to_objectid(station_id)
    if not oid:
        return jsonify({"error": "Invalid station id"}), 400

    # Remove the reading with the specified ID
    result = weather_collection.update_one(
        {"_id": oid},
        {"$pull": {"readings": {"_id": reading_id}}}
    )

    # Confirm deletion success
    if result.modified_count == 1:
        return jsonify({"message": "Reading deleted successfully"}), 200
    else:
        return jsonify({"error": "Reading not found"}), 404
