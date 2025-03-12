import socket
import requests

def receive_results(udp_host='192.168.202.1', udp_port=6000):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((udp_host, udp_port))
    print("Waiting for election results...")
    
    # Receiving the results broadcasted by the admin
    data, addr = udp_socket.recvfrom(4096)  # Adjust buffer size if results are large
    print(f"Received results from {addr}:\n{data.decode()}")

    url = 'http://localhost:5000/update_results'
    payload = {'results': data.decode()}
    requests.post(url, json=payload)

    udp_socket.close()

if __name__ == "__main__":
    receive_results()
