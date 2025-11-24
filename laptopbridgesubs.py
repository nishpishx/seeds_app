import roslibpy 
client = roslibpy.Ros(host='100.126.150.122', port=9090) # laptop Tailscale IP 
client.run() 
print('Connected:', client.is_connected)
