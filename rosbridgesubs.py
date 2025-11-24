import roslibpy
# Connect to your laptop's rosbridge server
client = roslibpy.Ros(host='100.126.150.122', port=9091) 
client.run()
# Subscribe to the mirrored GPS topic
listener = roslibpy.Topic(client, '/mirrored_gps', 'sensor_msgs/msg/NavSatFix') 
def handle_gps(msg):
    # Print key GPS fields
    print(f"Latitude: {msg['latitude']}, Longitude: {msg['longitude']}, Altitude: {msg['altitude']}")
    # Optional: print full message print(msg)
listener.subscribe(handle_gps) 
try:
    import time 
    while True: 
      time.sleep(1) 
except: 
    listener.unsubscribe() 
    client.terminate()
