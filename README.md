### A Remote code executer program in Python using the socket library. Includes client & server architecture.
Done as the project for Computer Networks Subject in the 4th Semester.\

___Note:___ Run the program with the flag : `-Xfrozen_modules=off`

### Commands to setup server key and server certificate on server:

1. `openssl genrsa -out server.key 2048`

2. `openssl req -new -key server.key -out server.csr`

3. `openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt`
