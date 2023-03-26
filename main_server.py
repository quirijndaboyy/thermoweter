import socket
import csv
import threading
import time

# Set up socket connection
HOST = '192.168.2.44' # Replace with the IP address of the sending end (Raspberry Pi Pico)
PORT = 6969
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen()

def handle_client(conn, addr):
    print(f"Connection from {addr}")
    while True:
        data = conn.recvmsg(2048)[0].decode("utf-8")
        if not data:
            break

        datalist = data.split(" ")

        for i in range(len(datalist)):
            datalist[i] = float(datalist[i])


        datalist = [time.time(),addr[0]]+datalist

        print(datalist)

        # Open a file for writing
        with open('data.csv', 'a', newline='') as f:
            # Create a CSV writer object
            writer = csv.writer(f)

            # Write the data to the CSV file
            writer.writerows([datalist])

    conn.close()

while True:
    conn, addr = s.accept()
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()
