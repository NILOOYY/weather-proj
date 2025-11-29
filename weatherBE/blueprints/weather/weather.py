# WEATHER BLUEPRINT 

from flask import Blueprint, request, jsonify, make_response
from bson import ObjectId
from globals import weather_collection
from decorators import jwt_required, admin_required
import datetime

weather_bp = Blueprint("weather_bp", __name__)

# GET /weather
# PUBLIC - Show all weather data
@weather_bp.route('/weather', methods=['GET'])
def getAllWeather():
    data_to_return = []
    page_num = request.args.get('page', default=1, type=int)
    page_size = request.args.get('size', default=10, type=int)
    page_start = (page_num - 1) * page_size

    try:
        weather_cursor = weather_collection.find().skip(page_start).limit(page_size)
        for weather in weather_cursor:
            weather['_id'] = str(weather['_id'])
            data_to_return.append(weather)
        return make_response(jsonify({
            "count": len(data_to_return),
            "page": page_num,
            "data": data_to_return
        }), 200)
    except Exception as e:
        return make_response(jsonify({
            "error": "Failed to load weather data",
            "details": str(e)
        }), 500)



# GET /weather/<id>
# PUBLIC - Get single weather record

@weather_bp.route('/weather/<string:record_id>', methods=['GET'])
def getOneWeather(record_id):
    try:
        weather = weather_collection.find_one({"_id": ObjectId(record_id)})
        if weather is not None:
            weather["_id"] = str(weather["_id"])
            return make_response(jsonify(weather), 200)
        else:
            return make_response(jsonify({"Error": "Weather record not found"}), 404)
    except Exception as e:
        return make_response(jsonify({
            "Error": "Invalid ID",
            "Details": str(e)
        }), 400)



# POST /weather
# ADMIN - Add new weather record
@weather_bp.route('/weather', methods=['POST'])
@jwt_required
@admin_required
def addWeather():
    data = request.form

    if data and "station_name" in data and "city" in data and "country" in data:
        avg_temp = float(data.get("avg_temp_c", 0))
        wind_speed = float(data.get("max_wind_kmh", 0))

        # --- -----Automatic Alerts ---  ------#
        alerts = []
        if avg_temp > 40:
            alerts.append(" Heatwave Alert")
        if avg_temp < 0:
            alerts.append(" Frost Warning")
        if wind_speed > 100:
            alerts.append(" Storm Warning")

        new_weather = {
            "station_name": data.get("station_name"),
            "city": data.get("city"),
            "state": data.get("state", ""),          # Added
            "region": data.get("region", ""),        # Added
            "place": data.get("place", ""),          # Added
            "country": data.get("country"),
            "avg_temp_c": avg_temp,
            "max_wind_kmh": wind_speed,
            "overall_condition": data.get("overall_condition", "Unknown"),
            "air_quality_index": int(data.get("air_quality_index", 0)),
            "alerts": alerts,
            "views": int(data.get("views", 0)),
            "created_at": datetime.datetime.utcnow(),
            "comments": []
        }

        result = weather_collection.insert_one(new_weather)
        new_weather_id = str(result.inserted_id)
        new_weather_link = f"http://127.0.0.1:5000/weather/{new_weather_id}"

        return make_response(jsonify({"URL": new_weather_link}), 201)
    else:
        return make_response(jsonify({"Error": "Missing required data"}), 400)


# PUT /weather/<id>
# ADMIN - Update a weather record
@weather_bp.route('/weather/<string:record_id>', methods=['PUT'])
@jwt_required
@admin_required
def updateWeather(record_id):
    data = request.form
    update_field = {}

    # Update text fields
    for key in ["station_name", "city", "state", "region", "place", "country", "overall_condition"]:
        if data.get(key):
            update_field[key] = data.get(key)

    # Update numeric fields
    for key, cast in [("avg_temp_c", float), ("max_wind_kmh", float),
                      ("air_quality_index", int), ("views", int)]:
        if data.get(key):
            try:
                update_field[key] = cast(data.get(key))
            except:
                return make_response(jsonify({"Error": f"Invalid value for {key}"}), 400)

    if not update_field:
        return make_response(jsonify({"Error": "No valid data passed"}), 400)

    update_field["last_updated_at"] = datetime.datetime.utcnow()

    try:
        results = weather_collection.update_one(
            {"_id": ObjectId(record_id)},
            {"$set": update_field}
        )
        if results.modified_count == 1:
            updated_weather_link = f"http://127.0.0.1:5000/weather/{record_id}"
            return make_response(jsonify({"URL": updated_weather_link}), 200)
        else:
            return make_response(jsonify({"message": "No changes made"}), 404)
    except Exception as e:
        return make_response(jsonify({
            "Error": "Failed to update weather record",
            "Details": str(e)
        }), 400)


# DELETE /weather/<id>
# ADMIN - Delete a weather record
@weather_bp.route('/weather/<string:record_id>', methods=['DELETE'])
@jwt_required
@admin_required
def deleteWeather(record_id):
    try:
        results = weather_collection.delete_one({"_id": ObjectId(record_id)})
        if results.deleted_count == 1:
            return make_response(jsonify({"message": "Weather record deleted"}), 200)
        else:
            return make_response(jsonify({"Error": "Record not found"}), 404)
    except Exception as e:
        return make_response(jsonify({
            "Error": "Invalid ID",
            "Details": str(e)
        }), 400)


# GET /weather/stats
# PUBLIC - Analyze weather stats by region/state/place
@weather_bp.route('/weather/stats', methods=['GET'])
def getWeatherStats():
    """
    Returns average temperature, air quality index, and wind speed
    for a specific region, state, or place.
    Example:
        /weather/stats?region=England
        /weather/stats?state=California
        /weather/stats?place=Tokyo
    """
    try:
        region = request.args.get("region", "").strip()
        state = request.args.get("state", "").strip()
        place = request.args.get("place", "").strip()

        if not (region or state or place):
            return make_response(jsonify({
                "error": "Missing filter parameter. Example: /weather/stats?region=England"
            }), 400)

        query = {}
        if region:
            query["region"] = {"$regex": region, "$options": "i"}
        if state:
            query["state"] = {"$regex": state, "$options": "i"}
        if place:
            query["place"] = {"$regex": place, "$options": "i"}

        cursor = weather_collection.find(query)

        temps, winds, aqi = [], [], []
        count = 0
        stations = []

        for doc in cursor:
            count += 1
            doc["_id"] = str(doc["_id"])
            stations.append(doc.get("station_name", "Unknown Station"))
            temps.append(float(doc.get("avg_temp_c", 0)))
            winds.append(float(doc.get("max_wind_kmh", 0)))
            aqi.append(int(doc.get("air_quality_index", 0)))

        if count == 0:
            return make_response(jsonify({
                "message": "No weather data found for given filters"
            }), 404)

        # Compute averages
        avg_temp = sum(temps) / len(temps)
        avg_wind = sum(winds) / len(winds)
        avg_aqi = sum(aqi) / len(aqi)

        stats = {
            "filters": {"region": region, "state": state, "place": place},
            "total_stations": count,
            "avg_temperature_c": round(avg_temp, 2),
            "avg_wind_speed_kmh": round(avg_wind, 2),
            "avg_air_quality_index": round(avg_aqi, 2),
            "stations_included": stations
        }

        return make_response(jsonify(stats), 200)

    except Exception as e:
        return make_response(jsonify({
            "error": "Failed to calculate weather stats.",
            "details": str(e)
        }), 500)


# GET /weather/alerts
# PUBLIC - Show weather alerts (with filters + summary)
@weather_bp.route('/weather/alerts', methods=['GET'])
def getWeatherAlerts():
    """
    Returns all weather records that have alerts ( Heatwave,  Storm, etc.)
    Works with both 'alert' and 'alerts' fields.
    Supports optional filtering by 'region', 'state', or 'city/place'.

    Example:
        /weather/alerts
        /weather/alerts?region=England
        /weather/alerts?state=California
        /weather/alerts?city=Tokyo
    """
    try:
        region = request.args.get("region", "").strip()
        state = request.args.get("state", "").strip()
        city = request.args.get("city", "").strip()
        place = request.args.get("place", "").strip()

        query = {
            "$or": [
                {"alerts": {"$exists": True, "$ne": []}},
                {"alert": {"$exists": True, "$ne": []}}
            ]
        }

        if region:
            query["region"] = {"$regex": region, "$options": "i"}
        if state:
            query["state"] = {"$regex": state, "$options": "i"}
        if city:
            query["city"] = {"$regex": city, "$options": "i"}
        if place:
            query["place"] = {"$regex": place, "$options": "i"}

        alert_cursor = weather_collection.find(
            query,
            {"station_name": 1, "city": 1, "state": 1, "region": 1, "place": 1,
             "country": 1, "alerts": 1, "alert": 1}
        )

        alert_data = []
        summary = {}

        for alert_doc in alert_cursor:
            alert_doc["_id"] = str(alert_doc["_id"])
            alerts_list = alert_doc.get("alerts") or alert_doc.get("alert") or []
            if not alerts_list:
                continue

            alert_data.append({
                "station_name": alert_doc.get("station_name"),
                "city": alert_doc.get("city"),
                "state": alert_doc.get("state"),
                "region": alert_doc.get("region"),
                "place": alert_doc.get("place"),
                "country": alert_doc.get("country"),
                "alerts": alerts_list
            })

            for alert_type in alerts_list:
                summary[alert_type] = summary.get(alert_type, 0) + 1

        if not alert_data:
            location_text = region or state or city or place or "all locations"
            return make_response(jsonify({
                "message": f"No weather alerts found for {location_text}."
            }), 404)

        return make_response(jsonify({
            "count": len(alert_data),
            "filtered_by": region or state or city or place or "all",
            "summary_by_alert_type": summary,
            "alerts": alert_data
        }), 200)

    except Exception as e:
        return make_response(jsonify({
            "error": "Failed to retrieve weather alerts.",
            "details": str(e)
        }), 500)

# GET /weather/<id>/trends
# PUBLIC - Analyze weather readings (avg/min/max)
# GET /weather/<id>/trends
# PUBLIC - Analyze weather readings for one station
@weather_bp.route('/weather/<string:record_id>/trends', methods=['GET'])
def get_weather_trends(record_id):
    try:
        record = weather_collection.find_one({"_id": ObjectId(record_id)})
        if not record:
            return make_response(jsonify({"Error": "Station not found"}), 404)

        readings = record.get("readings", [])
        if not readings:
            return make_response(jsonify({"message": "No readings available"}), 404)

        # Extract numeric data
        temps = [r.get("temperature_c", 0) for r in readings]
        humidity = [r.get("humidity_pct", 0) for r in readings]
        wind = [r.get("wind_speed_kmh", 0) for r in readings]

        # Compute trends
        trends = {
            "station_name": record.get("station_name"),
            "city": record.get("city"),
            "total_readings": len(readings),
            "avg_temp": round(sum(temps) / len(temps), 2),
            "min_temp": min(temps),
            "max_temp": max(temps),
            "avg_humidity": round(sum(humidity) / len(humidity), 2),
            "avg_wind_kmh": round(sum(wind) / len(wind), 2)
        }

        return make_response(jsonify(trends), 200)
    except Exception as e:
        return make_response(jsonify({
            "Error": "Failed to analyze trends",
            "Details": str(e)
        }), 500)


# GET /weather/trends/all
# PUBLIC - Analyze all weather stations (global trends)
@weather_bp.route('/weather/trends/all', methods=['GET'])
def get_all_weather_trends():
    try:
        records = list(weather_collection.find())
        if not records:
            return make_response(jsonify({"message": "No weather data found"}), 404)

        temps, humidity, wind = [], [], []

        for r in records:
            if "readings" in r:
                for item in r["readings"]:
                    temps.append(item.get("temperature_c", 0))
                    humidity.append(item.get("humidity_pct", 0))
                    wind.append(item.get("wind_speed_kmh", 0))

        if not temps:
            return make_response(jsonify({"message": "No readings found"}), 404)

        global_trends = {
            "total_stations": len(records),
            "total_readings": len(temps),
            "avg_temp": round(sum(temps) / len(temps), 2),
            "avg_humidity": round(sum(humidity) / len(humidity), 2),
            "avg_wind_kmh": round(sum(wind) / len(wind), 2),
            "min_temp": min(temps),
            "max_temp": max(temps)
        }

        return make_response(jsonify(global_trends), 200)
    except Exception as e:
        return make_response(jsonify({
            "Error": "Failed to calculate global trends",
            "Details": str(e)
        }), 500)