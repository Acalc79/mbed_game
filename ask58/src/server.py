from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import socket
import json
from game import Game

game = None

class MyHandler(BaseHTTPRequestHandler):
    # HTTP REQUESTS HERE
    
    def do_POST(self):
        content = b"POST: Hello, Mbed!"
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content)
        post_data = self.rfile.read(100)
        print(post_data)
        return
    
    def do_GET(self):
        content = b"GET: Hello, Mbed!"
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content)
        post_data = self.rfile.read(100)
        print(post_data)
        return
 
    def do_PUT(self):
        content = b"PUT: Hello, Mbed!"
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content)
        post_data = self.rfile.read(100)
        json_dict = json.loads(post_data)
##        print(json_dict)
        global game
        if game is not None:
            game.input = data_to_game_inputs(json_dict)
        return

def data_to_game_inputs(data):
    game_inputs = {}
    if 'x' in data and 'y' in data and 'z' in data:
        x, y, z = data['x'], data['y'], data['z']
        game_inputs['x'] = -float(y)
        game_inputs['y'] = -float(x)
    if 'btn' in data:
        game_inputs['btn'] = int(data['btn'])
    if 'dist' in data:
        game_inputs['dist'] = float(data['dist'])
    if 'hum' in data:
        game_inputs['hum'] = float(data['hum'])
    return game_inputs
            
            
def run():
    httpd = HTTPServer(('', 8080), MyHandler)
    print ("HTTP server running on port 8080")
    print ("Your IP address is: ", socket.gethostbyname(socket.gethostname()))
##    httpd.serve_forever()
    httpd.timeout = 0.05
    global game
    game = Game(httpd.handle_request)
    game.start_game()

if __name__ == '__main__':
    run()
