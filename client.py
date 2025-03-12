import socket

def start_tcp_client(server_ip='127.0.0.1', server_port=12345):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect the socket to the server's IP and port
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")

    try:
        # Send data to the server
        message = "Hello, TCP Server!"
        print(f"Sending: {message}")
        client_socket.sendall(message.encode())
        
        # Look for the response
        response = client_socket.recv(1024)
        print(f"Received: {response.decode()}")
    finally:
        # Close the connection
        print("Closing connection")
        client_socket.close()

if __name__ == "__main__":
    start_tcp_client('127.0.0.1', 12345)  # Replace with the server's IP address
