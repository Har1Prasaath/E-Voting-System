import socket

def start_tcp_server(server_ip='127.0.0.1', server_port=12345):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the address and port
    server_socket.bind((server_ip, server_port))
    
    # Start listening for incoming connections
    server_socket.listen(1)
    print(f"Server is listening on {server_ip}:{server_port}...")

    while True:
        # Wait for a connection
        connection, client_address = server_socket.accept()
        try:
            print(f"Connection established with {client_address}")
            
            # Receive data in small chunks
            while True:
                data = connection.recv(1024)
                if data:
                    print(f"Received: {data.decode()}")
                    # Send the same data back to the client (echo)
                    connection.sendall(data)
                else:
                    # No more data, close the connection
                    print("No more data from client, closing connection.")
                    break
        finally:
            # Clean up the connection
            connection.close()

if __name__ == "__main__":
    start_tcp_server('0.0.0.0', 12345)  # Listen on all available interfaces
