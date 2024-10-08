import socket
import threading
import os
import sys
import time

# Create UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse of the address
server.bind(("", 20000))

nm = input("Enter your name: ")
print("\nType '_0' to exit.")

# Ask for IP and port with basic input validation
while True:
    try:
        ip, port = input("Enter IP address and Port number (e.g., 192.168.1.5 20001): ").split()
        port = int(port)
        break
    except ValueError:
        print("Invalid input. Please enter a valid IP address and port number.")

def send():
    while True:
        msg = input()
        if msg == "_0":
            print("Exiting chat...")
            server.close()  # Close socket gracefully
            os._exit(0)     # Exit the program safely
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        sm = "[{}] {}: {}".format(timestamp, nm, msg)
        try:
            server.sendto(sm.encode(), (ip, port))
        except Exception as e:
            print(f"Error sending message: {e}")
            break

def rec():
    while True:
        try:
            msg, addr = server.recvfrom(2048)
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            print("\t\t\t[{}] Friend: {}".format(timestamp, msg.decode()))
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# Create and start the threads
x1 = threading.Thread(target=send, daemon=True)
x2 = threading.Thread(target=rec, daemon=True)

x1.start()
x2.start()

# Keep the main thread alive to let the user chat
try:
    while x1.is_alive() and x2.is_alive():
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting chat...")
    server.close()
    sys.exit(0)
