import socket
import threading
import sys

# 接收来自服务器消息
def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print("Disconnected from server")
                break
            print(f"Received from server: {data}")
        except Exception as e:
            # print(f"Error: {e}")
            break

# 发送消息给服务器的函数
def send_messages(client_socket):
    while True:
        try:
            message = input("Client: ")
            # 如果输入 "exit" 则退出聊天
            if message.lower() == "exit":
                print("Exiting...")
                client_socket.send(message.encode('utf-8'))
                client_socket.close()
                sys.exit()
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
            break

def main():
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # 启动接收消息的线程
    receive_handler = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_handler.start()

    # 启动发送消息的线程
    send_handler = threading.Thread(target=send_messages, args=(client_socket,))
    send_handler.start()

if __name__ == "__main__":
    main()
