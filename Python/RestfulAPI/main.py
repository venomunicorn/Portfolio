from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time

# In-memory database
DATA = {
    1: {"id": 1, "name": "Item One", "description": "This is the first item"},
    2: {"id": 2, "name": "Item Two", "description": "This is the second item"}
}

class SimpleAPI(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path == '/items':
            self._set_headers()
            self.wfile.write(json.dumps(list(DATA.values())).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def do_POST(self):
        if self.path == '/items':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data)
                new_id = max(DATA.keys()) + 1 if DATA else 1
                data['id'] = new_id
                DATA[new_id] = data
                
                self._set_headers(201)
                self.wfile.write(json.dumps({"message": "Item created", "item": data}).encode())
            except:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
        else:
            self._set_headers(404)

    def do_DELETE(self):
        if self.path.startswith('/items/'):
            try:
                item_id = int(self.path.split('/')[-1])
                if item_id in DATA:
                    del DATA[item_id]
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"message": f"Item {item_id} deleted"}).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Item not found"}).encode())
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid ID"}).encode())
        else:
            self._set_headers(404)

def run(server_class=HTTPServer, handler_class=SimpleAPI, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting API server on port {port}...")
    print("Endpoints:")
    print(f"  GET    http://localhost:{port}/items")
    print(f"  POST   http://localhost:{port}/items  (Body: JSON)")
    print(f"  DELETE http://localhost:{port}/items/<id>")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server stopped.")

if __name__ == "__main__":
    run()
