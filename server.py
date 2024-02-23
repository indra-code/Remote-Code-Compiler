import subprocess
import socket
import threading
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 9999
    server.bind(("localhost", port))
    server.listen()
    print(f"Server is listening at port: {port}")
    while True:
        client, addr = server.accept()
        file_name = receive_file_name(client)
        thread = threading.Thread(target=receivefile,args=(file_name,client))
        thread.start()

def receive_file_name(client_socket):
    file_name = b""  # Initialize an empty byte string to store received data
    while True:
        data = client_socket.recv(12)  # Receive data from the client
        if not data:  # If no data is received, break the loop
            break
        file_name += data  # Concatenate the received data
        if b"<END_FILENAME>" in file_name:  # Check if the end marker is present in the received data
            file_name = file_name.replace(b"<END_FILENAME>", b"")  # Remove the end marker
            break
    return file_name.decode()  # Decode the byte string to get the file name as a string

def compile_and_run(filename):
    error = None
    output = None
    try:
        # Execute the code and capture the output
        if filename.endswith(".py"):
            result = subprocess.run(['python', filename], capture_output=True, text=True, timeout=10)
            output = result.stdout
            error = result.stderr
        elif filename.endswith(".c"):
            compilation = subprocess.run(['gcc', '-o', filename[:-2], filename], capture_output=True, text=True, timeout=10)
            if (compilation.returncode == 0):
                executable = subprocess.run([filename[:-2] + '.exe'], capture_output=True, text=True, timeout=10)
                output = executable.stdout
                error = executable.stderr
        else:
            pass

        if error:
            return error
        else:
            return output
    except subprocess.TimeoutExpired:
        return "Error: Timeout expired. Execution took too long."
    except Exception as e:
        return f"Error: {str(e)}"
    
def receivefile(file_name,client):
    
    print("Receiving:", file_name)
    file = open(file_name, "wb")
    while True:
        data = client.recv(1024)
        if not data:
            break
        if data.endswith(b"<END>"):
            file.write(data[:-5])  # Remove the "<END>" marker before writing to file
            break
        else:
            file.write(data)
    file.close()
    response_message = "File received successfully!"
    client.sendall(response_message.encode())
    output_final = compile_and_run(file_name)
    compile_and_run(file_name)
    client.sendall(output_final.encode())
main()

