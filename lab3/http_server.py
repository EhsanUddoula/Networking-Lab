from http.server import HTTPServer,BaseHTTPRequestHandler
import os
import cgi

HOST="localhost"
PORT=8000
ENCODER="utf-8"
path="/Users/HP/Documents/networking/lab2"

class server(BaseHTTPRequestHandler):
    def do_GET(self):
        file_path = self.path[1:]
        rfile=""
        for char in reversed(file_path):
            if char=='/':
                break
            rfile+=char
        file_name=rfile[::-1]

            
        try:
            with open(file_name, 'rb') as file:
                file_data = file.read()

            self.send_response(200)
            self.send_header("Content-type", "application/octet-stream")
            self.end_headers()
            self.wfile.write(file_data)
            print(f"200 ok.\n{file_name} is downloaded by client")
        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            print("404 File not found")
            
    def do_POST(self):
        content_type, _ = cgi.parse_header(self.headers.get('Content-type'))

        if content_type == 'multipart/form-data':
            form_data = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         }
            )

            if 'file' in form_data:
                file_item = form_data['file']
                file_name = os.path.basename(file_item.filename)

                with open("e.txt", 'wb') as file:
                    file.write(file_item.file.read())

                self.send_response(201)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                print("New File uploaded...")
                self.wfile.write(f"201 created.\nFile {file_name} received and saved.".encode(ENCODER))
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                print("Bad Request: No file provided")



def main():
    server_socket=HTTPServer((HOST,PORT),server)
    print(f"Server Running On Port {PORT}")
    server_socket.serve_forever()

if __name__== '__main__':
    main()