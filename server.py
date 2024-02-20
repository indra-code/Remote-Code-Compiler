import subprocess
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

client, addr = server.accept()

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


file_name = client.recv(1024).decode()
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

# Send response to the client
response_message = "File received successfully!"
client.sendall(response_message.encode())
output_final = compile_and_run(file_name)

# Send the output of the execution back to the client
client.sendall(output_final.encode())

client.close()
server.close()
