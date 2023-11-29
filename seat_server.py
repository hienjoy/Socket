import socket
import pickle
import threading

HOST = input('IP 주소 입력 : ')
PORT = 12345

seats = list(range(1, 31))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"서버가 {HOST}:{PORT}에서 실행 중입니다.")

def update_seats(client_socket):
    seat_state = pickle.dumps(seats)
    client_socket.sendall(seat_state)

def handle_client(client_socket, client_address):
    print(f"클라이언트 {client_address[1]} 연결되었습니다.")

    message = "좌석 예약을 시작합니다"
    client_socket.sendall(message.encode())
    update_seats(client_socket)

    while True:
        try:
            receive_data = client_socket.recv(1024).decode()

            if receive_data == "EXIT":
                print(f"클라이언트 {client_address[1]} 종료")
                break
            
            elif receive_data == "UPDATE":
                print(f"클라이언트로부터 업데이트 요청을 받았습니다.")
                update_seats(client_socket)
                    
            else:
                idx = int(receive_data) - 1
                print(f"클라이언트 {client_address[1]} {receive_data}번 좌석 상태 요청")

                if seats[idx] != 0:
                    client_socket.sendall("OK".encode())
                    save_data = client_socket.recv(1024).decode()
                    if save_data == "UPDATE":
                        print(f"클라이언트가 업데이트를 요청했습니다.")
                        update_seats(client_socket)
                        
                    elif seats[idx] != 0:
                        seats[idx] = 0
                        client_socket.sendall("save".encode())
                        print(f"{receive_data}번 좌석은 {client_address[1]}이 예매했습니다")
                    else:
                        client_socket.sendall("done".encode())
                else:
                    client_socket.sendall("NO".encode())
        except ValueError as e:
            print(f"값 오류 발생: {e}")
            break
            
    client_socket.close()

while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
