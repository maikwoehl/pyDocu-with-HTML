import http.server
import sys

HTTP = ""
PORT = 8000

handler = http.server.CGIHTTPRequestHandler

httpd = http.server.HTTPServer((HTTP, PORT), handler)
httpd.server_name = "tkhelp Webserver"
httpd.server_port = PORT

print("Server: ", httpd.server_name)
print("Port: ", PORT)

try:
    httpd.serve_forever()
except KeyboardInterrupt: 
    print("\n You pressed ^C (Ctrl+C)")
    print("Is going shutdown...")
    sys.exit(0)
