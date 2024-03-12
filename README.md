Sem 4 Computer Networks Project, a remote code compiler/interpreter for c and python respectively.Uses client server architecture and socket programming.
Commands to setup server key and server certificate on server:
1)openssl genrsa -out server.key 2048

2)openssl req -new -key server.key -out server.csr

3)openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
