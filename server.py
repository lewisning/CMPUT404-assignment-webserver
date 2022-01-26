#  coding: utf-8 
import socketserver
import os


# Copyright 2022 Abram Hindle, Eddie Antonio Santos, Lewis Ning
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


def get_file_type(path):
    if '.css' in path:
        return 'text/css'
    elif '.html' in path:
        return 'text/html'


def response200(fileType):
    response = f"HTTP/1.1 200 OK\r\nContent-type: {fileType}\r\n\r\n"
    return response


def response301():
    response = f"HTTP/1.1 301 Moved Permanently\r\n\r\n"
    return response.encode()


def response404():
    response = f"HTTP/1.1 404 Not Found\r\n\r\n"
    return response.encode()


def response405():
    response = f"HTTP/1.1 405 Method Not Allowed\r\n\r\n"
    return response.encode()


class MyWebServer(socketserver.BaseRequestHandler):
    def handle(self):
        # Get the header
        self.data = self.request.recv(1024).strip()
        splited = self.data.decode().split(' ')
        filename = splited[1]
        body = ''

        # 1. Get the current directory path and add the address from header to the end of current path
        #    Serve files from ./www
        root = os.getcwd() + '/www'

        # 2. Check is the GET header
        #    If not, then return 405 code for PUT/POST/DELETE
        if 'GET' != splited[0]:
            self.request.sendall(response405())
        else:
            # 3. Check is the path valid and Handle 404 error (path not found)
            path = root + filename
            if os.path.isdir(path) or os.path.isfile(path):
                # Check is this path going to deep folder
                if '/deep' in path:
                    # Check is current path belongs to a file
                    if os.path.isfile(path):
                        if '.html' or '.css' in path:
                            root_page = open(path, 'r')
                            body = root_page.read()
                            root_page.close()
                    else:
                        # Check is the end of current path should be /
                        if path.endswith('/'):
                            path += 'index.html'
                            root_page = open(path, 'r')
                            body = root_page.read()
                            root_page.close()
                        else:
                            self.request.sendall(response301())
                            path += '/index.html'
                            root_page = open(path, 'r')
                            body = root_page.read()
                            root_page.close()

                # Check is the path going to hardcode folder
                elif '/hardcode' in path:
                    # Check is current path belongs to a file
                    if os.path.isfile(path):
                        if '.html' or '.css' in path:
                            root_page = open(path, 'r')
                            body = root_page.read()
                            root_page.close()
                    else:
                        # Check is the end of current path should be /
                        if path.endswith('/'):
                            path += 'index.html'
                            root_page = open(path, 'r')
                            body = root_page.read()
                            root_page.close()
                        else:
                            self.request.sendall(response301())
                            path += '/index.html'
                            root_page = open(path, 'r')
                            body = root_page.read()
                            root_page.close()

                # Check is the current opening file belongs to group file
                elif '/group' in path:
                    self.request.sendall(response404())

                # If not going to deeper two folders, then access the root file
                elif '/www' in path:
                    # Check is current path belongs to a file
                    if os.path.isfile(path):
                        if '.html' or '.css' in path:
                            root_page = open(path, 'r')
                            body = root_page.read()
                            root_page.close()
                    else:
                        # Check is the end of current path should be /
                        if path.endswith('/'):
                            path += 'index.html'
                            root_page = open(path, 'r')
                            body = root_page.read()
                            root_page.close()
                        else:
                            self.request.sendall(response301())
                            path += '/index.html'
                            root_page = open(path, 'r')
                            body = root_page.read()
                            root_page.close()

                # 3. Check the type
                fileType = get_file_type(path)

                # 4. Send data
                new_header = response200(fileType)
                self.request.send(bytearray(new_header, 'utf-8'))
                if body is not None:
                    self.request.send(bytearray(body, 'utf-8'))
            else:
                self.request.sendall(response404())


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
