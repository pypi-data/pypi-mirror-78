from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os
from urllib.parse import urlparse, parse_qs
from bunny_lab.logic import BunnyLab

BUNNY_LAB_DIR = os.path.dirname(__file__)

bunny_lab = BunnyLab()


def handle_reset():
    bunny_lab = BunnyLab()
    return ""

def handle_register_user():
    name = bunny_lab.register_user()
    return name

def handle_unregister_user(name):
    bunny_lab.unregister_user(name)
    return ""

def handle_bunnies_saved(name, number):
    saved_bunnies = bunny_lab.bunnies_saved(name, number)
    return str(saved_bunnies)

def handle_bunny_saved(name):
    saved_bunnies = bunny_lab.bunny_saved(name, number)
    return str(saved_bunnies)

def handle_file_request(path):
    path = os.path.join(BUNNY_LAB_DIR, "static", path)
    return open(path).read()

class RequestHandler(BaseHTTPRequestHandler):

    def confirm_post(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def try_serve_file(self):
        parsed_url = urlparse(self.requestline)
        path = parsed_url.path
        try:
            path = os.path.join(BUNNY_LAB_DIR, "static") + path
            response = open(path).read()
            print("READING FILE: ", open(path).read())
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            results = bunny_lab.print_results()
            self.wfile.write(response.encode())
        except:
            print("FAILED READING FILE: ", path)
            self.send_response(400)
            self.end_headers()

    def generate_and_send_results(self):
        parsed_url = urlparse(self.requestline)
        path = parsed_url.path
        qs = parse_qs(path)
        print(path, qs)
        if "notebook" in qs:
            full_html = False
        else:
            full_html = True

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        results = bunny_lab.print_results(full_html)
        self.wfile.write(results.encode())


    def do_GET(self):
        self.protocol_version = "HTTP/1.1"

        if self.path[:2] != "/?"[:len(self.path)]:
            self.try_serve_file()
        else:
            self.generate_and_send_results()


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_data = parse_qs(post_data)
        print("Incoming post: ", post_data)
        action = post_data["action"][0]

        if action == "reset":
            name = post_data["name"][0]
            if name == "b.diddy":
                handle_reset()
            message = ""
        elif action == "register":
            message = handle_register_user()
        elif action == "unregister":
            name = post_data["name"][0]
            message = handle_unregister_user(name)
        elif action == "saved":
            name = post_data["name"][0]
            number = int(post_data["number"][0])
            message = handle_bunnies_saved(name, number)
        elif action == "bunny_saved":
            name = post_data["name"][0]
            message = handle_bunny_saved(name)

        self.send_response(200, message)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


