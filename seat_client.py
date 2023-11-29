import socket
import pickle
from tkinter import *

HOST = input('서버 IP 주소 입력 : ')
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


start_msg = client_socket.recv(1024).decode()


my_seat=[]
buttons = []

def save_num(seat): #좌석 예매
    client_socket.send(str(seat).encode())
    print(f"{seat}번 좌석 예매 요청")
    result = client_socket.recv(1024).decode()
    if result == "save":
        my_seat.append(seat)
        confirm.config(text=f"{seat}번 좌석을 예약 완료했습니다")
        buttons[seat-1].config(bg="green")
        for i in range(len(my_seat)):
            print(my_seat[i])
    elif result == "done":
        confirm.config(text="예약 완료된 좌석입니다")

    
def send_selected(): #좌석 선택
    seat = int(seat_entry.get())
    client_socket.send(str(seat).encode())
    print(f"{seat}번 좌석 선택")
    response = client_socket.recv(1024).decode()
    if response == "OK":
        buttons[seat-1].config(bg="yellow" )
        choose_seat.config(text=f"{seat}번 좌석을 선택했습니다")
        save_button = Button(input_frame, text="예매하기", command=lambda:save_num(seat))
        save_button.grid(row=4, columnspan=2, padx=5, pady=15)

    elif response == "NO":
        if seat in my_seat:
            choose_seat.config( text=f"이미 예약한 좌석입니다")
        else:
            choose_seat.config( text=f"{seat}번 좌석은 예약 불가합니다")
        seat_entry.delete(0, END)


def update_seats(): #좌석 업데이트
    client_socket.sendall("UPDATE".encode())
    data = client_socket.recv(1024)
    updated_seats = pickle.loads(data)
    print(updated_seats)
    
    # 좌석 정보 업데이트
    for i in range(len(updated_seats)):
        if updated_seats[i] != 0:
            buttons[i].config(bg=info_b1.cget("background"))
        else:
            buttons[i].config(bg="green")
    
def on_closing():
    client_socket.sendall("EXIT".encode())
    client_socket.close()
    win.destroy()
    

win = Tk()
win.title("좌석 예매 프로그램")
win.geometry("700x700")


conn_msg = Label(win, font=4, height=3, text=start_msg)
conn_msg.config(fg='blue')
conn_msg.pack()

data = client_socket.recv(1024) 
seats = pickle.loads(data)
print(seats)

top_frame = Frame(win, bg="white",width="300", height="300")
top_frame.pack(pady=10)

info_b1 = Button(top_frame, text="가능",width=6,height=1)
info_b2 = Button(top_frame, text="불가",width=6,height=1,bg="green")
info_b3 = Button(top_frame, text="선택",width=6,height=1,bg="yellow")
info_b1.grid(row=6,column=3)
info_b2.grid(row=6,column=4)
info_b3.grid(row=6,column=5)


for i in range(1, 31):
    if (seats[i - 1] != 0):
        btn = Button(top_frame, text=str(i), width=6, height=3)
    else:
        btn = Button(top_frame, text=str(i), width=6, height=3, bg="green")
    btn.grid(row=(i - 1) // 6, column=(i - 1) % 6, padx=10, pady=5)
    buttons.append(btn)

input_frame = Frame(win)
input_frame.pack(pady=10)

seat_label = Label(input_frame, text="원하는 좌석을 입력하세요", font=4)
seat_label.grid(row=0, column=0, padx=5, pady=5)

seat_entry = Entry(input_frame, width=15)
seat_entry.grid(row=0, column=1, padx=5, pady=5)

choose_button = Button(input_frame, text="선택하기", command=send_selected)
choose_button.grid(row=2, columnspan=2, padx=5, pady=15)

choose_seat = Label(input_frame, font=4)
choose_seat.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

confirm = Label(input_frame, font=4)
confirm.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

update_button = Button(input_frame, text="업데이트", command=update_seats)
update_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)



win.protocol("WM_DELETE_WINDOW", on_closing)
win.mainloop()
