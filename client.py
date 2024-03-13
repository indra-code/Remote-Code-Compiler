from tkinter import *
from tkinter import filedialog as fd
from tkinter.simpledialog import askstring
import socket
import ssl

fpath = "None"
output = ""
ftypes = (("C Files","*.c"),("Python Files","*.py"))

#create socket and establish connection and SSL handshake
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ipaddr = "localhost"  #Replace with desired IP Address
client.connect((ipaddr, 9999))
certificate_data = client.recv(4096)
cert_file_path = "server.crt"
with open(cert_file_path, "wb") as cert_file:
    cert_file.write(certificate_data)
client_ssl = ssl.wrap_socket(client,ca_certs="./server.crt")


#Choosing a file
def setfilepath():
    global fpath
    
    fp = fd.askopenfilename(
        title="select the code file",
        filetypes=ftypes
    )
    fpath = fp
    ff = "Selected File: {}".format(fp)
    l0["text"] = ff

#Sending the file and receiving code output
def sendfile(fpath):
    global output
    f_name = askstring(title='',prompt="Enter Received File with Extension ")
    file_name = f_name +"<END_FILENAME>"
    client_ssl.send((file_name).encode())
    t = client_ssl.recv(1024)
    print(t.decode())
    with open(fpath, "rb") as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client_ssl.sendall(data)
    client_ssl.send(b"<END>")
    r = client_ssl.recv(1024)
    print(r.decode())
    output = client_ssl.recv(4096).decode()
    print("Output:")
    print(output)
    l1["text"]=output
    
#GUI    
window = Tk()
window.geometry("680x632")
window.configure(bg = "#44444c")

canvas = Canvas(
    window,
    bg = "#44444c",
    height = 832,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
    )
canvas.place(x = 0, y = 0)

canvas.create_text(
    325.0, 183,
    text="Output",
    fill="#ffffff",
    font= "PTSans-Bold 13"
)

#Title
canvas.create_text(
    325.0, 50,
    text="Remote Code Compiler",
    fill="#ffffff",
    font= "PTSans-Bold 30"
)

l0 = Label(
    window, text="Selected File: {}".format(fpath),
    background="#44444c",
    fg="#FFFFFF",
    font="RobotoSans 12"
)

l0.place(x=40,y=107)

l1 = Label(
    window,
    text=output,
    background="#FFFFFF",
    anchor="nw",
    width=93,
    height= 80,
    justify='left',
    pady=0,
    padx=0,

)



l1.place(x=10,y=200)


b0 = Button(
    window,
    text= "Select File Path",
    borderwidth = 0,
    highlightthickness = 0,
    command= setfilepath
)

b0.place(
    x = 206, y = 140,
    width = 100,
    height = 30)

b1 = Button(
        window,
        text="Send",
        borderwidth=0,
        highlightthickness=0,
        command= lambda:sendfile(fpath)
)

b1.place(
    x = 356, y = 140,
    width = 100,
    height = 30)


window.mainloop()
client_ssl.close()
