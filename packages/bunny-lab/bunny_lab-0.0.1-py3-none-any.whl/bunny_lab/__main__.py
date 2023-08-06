import argparse
from bunny_lab.server import HTTPServer, RequestHandler

parser = argparse.ArgumentParser(description='The bunny lab server.')
parser.add_argument('--ip', type=str, help='The IP address to listen to.')
parser.add_argument('--port', type=int, help='The port to listen to')

args = parser.parse_args()
ip = args.ip
port = int(args.port)

#
# Start server
#

print(ip, port)

server = (ip, port)
httpd = HTTPServer(server, RequestHandler)
httpd.serve_forever()
