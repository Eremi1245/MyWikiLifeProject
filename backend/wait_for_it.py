import socket
import time

def wait_for_service(host, port, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                print(f"Service {host}:{port} is available")
                return
        except (ConnectionRefusedError, socket.timeout):
            time.sleep(1)
    
    print(f"Timeout exceeded. Failed to connect to {host}:{port}")

# Пример использования
wait_for_service("elasticsearch", 9200, timeout=30)
