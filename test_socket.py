import socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    s.connect(('127.0.0.1', 5555))
    print("SUCCESS: Connected to 127.0.0.1:5555")
    s.close()
except Exception as e:
    print(f"FAILED: {e}")
