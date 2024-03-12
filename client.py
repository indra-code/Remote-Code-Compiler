import os
import socket
import ssl

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ipaddr = "localhost"
client.connect((ipaddr, 9999))
certificate_data = client.recv(4096)
cert_file_path = "server.crt"
with open(cert_file_path, "wb") as cert_file:
    cert_file.write(certificate_data)
client_ssl = ssl.wrap_socket(client,ca_certs="./server.crt")

f_name = "received_test.py"  # Define the file name
# file_size = os.path.getsize("test.c")  # Get the file size
file_name = f_name +"<END_FILENAME>"
# # Send file name
client_ssl.send((file_name).encode())
t = client_ssl.recv(1024)
print(t.decode())
# client.settimeout(20)

# Send file size
#client.send(str(file_size).encode())

# Send file content
with open("test.py", "rb") as file:
    while True:
        data = file.read(1024)
        if not data:
            break
        client_ssl.sendall(data)

# Send end marker
client_ssl.send(b"<END>")
r = client_ssl.recv(1024)
print(r.decode())
output = client_ssl.recv(4096).decode()
print("Output:")
print(output)
client_ssl.close()

