import socket
import threading
import sys

# 接收来自客户端的消息
def handle_client(client_socket, addr):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print(f"Disconnected from {addr}")  # 未连接
                break
            print(f"Received from client: {data}")
        except Exception as e:
            # print(f"Error: {e}")
            break

# 发送消息给客户端
def send_messages(server_socket):
    while True:
        try:
            message = input("Server: ")
            # 如果输入 "exit" 则退出聊天
            if message.lower() == "exit":
                print("Exiting...")
                server_socket.send(message.encode('utf-8'))
                server_socket.close()
                sys.exit()
            server_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
            break

def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    client_socket, addr = server_socket.accept()
    print(f"Connected to {addr}")

    # 启动处理客户端消息的线程
    client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_handler.start()

    # 启动发送消息的线程
    send_handler = threading.Thread(target=send_messages, args=(client_socket,))
    send_handler.start()

if __name__ == "__main__":
    main()
