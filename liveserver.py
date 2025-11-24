from datetime import datetime from flask import Flask, jsonify import roslibpy import threading import time app = 
Flask(__name__) geojson = {
    "type": "FeatureCollection", "metadata": { "api": "1.0", "count": 0, "generated": int(datetime.utcnow().timestamp() * 
        1000), "status": 200, "title": "Robot Seed Drops", "url": "http://YOUR_PUBLIC_IP_OR_DOMAIN/seeds.geojson"
    },
    "features": []
}
def add_gps_point(seed_id, lon, lat): feature = { "type": "Feature", "id": f"seed_{seed_id}", "geometry": {"type": "Point", 
        "coordinates": [lon, lat]}, "properties": {
            "timestamp": datetime.utcnow().isoformat() + "Z", "type": "seed_drop"
        }
    }
    geojson["features"].append(feature) geojson["metadata"]["count"] = len(geojson["features"]) 
    geojson["metadata"]["generated"] = int(datetime.utcnow().timestamp() * 1000)
# Flask route to serve live GeoJSON
@app.route('/seeds.geojson') def get_geojson(): return jsonify(geojson) def ros_listener(): client = 
    roslibpy.Ros(host='100.73.171.53', port=9090) client.run() def gps_callback(msg):
        lon = msg.get('longitude') lat = msg.get('latitude') print(f"GPS: lon={lon}, lat={lat}") 
        add_gps_point(len(geojson["features"]), lon, lat)
    listener = roslibpy.Topic(client, '/gps/fix', 'sensor_msgs/msg/NavSatFix') listener.subscribe(gps_callback)
    # Keep the listener running
    try: while client.is_connected: time.sleep(0.1) except KeyboardInterrupt: listener.unsubscribe() client.terminate() if 
__name__ == '__main__':
    # Start ROS listener in background
    threading.Thread(target=ros_listener, daemon=True).start()
    # Start Flask web server
    app.run(host='0.0.0.0', port=5000)
