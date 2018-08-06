from os import environ as env

from ..adapter import Adapter
from ..messages import Message
from ..user import User
from urllib.parse import urlparse, unquote

from http.server import BaseHTTPRequestHandler, HTTPServer


class httpAdapter_RequestHandler(BaseHTTPRequestHandler):

  # GET
  def do_GET(self):
        # Send response status code
        request = urlparse(self.path)
        user_id = 1
        name = "anonymous"

        user = User(user_id, name)
        message = Message(user, 'http', unquote(request.query))
        message.request = self
        self.server.adapter.receive(message)

class HttpAdapter(Adapter):

    def send(self, message, text):
        message.request.send_response(200)

        # Send headers
        message.request.send_header('Content-type', 'text/html')
        message.request.end_headers()

        # Send message back to client
        # Write content as utf-8 data
        message.request.wfile.write(bytes(text, "utf8"))
        #return

    def emote(self, message, text):
        self.send(message, '* {}'.format(text))

    def reply(self, message, text):
        self.send(message, '{}: {}'.format(message.user.name, text))

    def run(self):
        name = env.get('PYBOT_SHELL_USER_NAME', 'Http')

        try:
            user_id = env.get('PYBOT_SHELL_USER_ID')
        except ValueError:
            user_id = 1


        # Server settings
        # Choose port 8080, for port 80, which is normally used for a http server, you need root access
        port = 8081
        server_address = ('0.0.0.0', port)
        print('Starting server...')
        httpd = HTTPServer(server_address, httpAdapter_RequestHandler)
        # Used to get a reference that can be reached within the RequestHandler
        httpd.adapter = self
        print(f'Server listening on port {port}...')
        httpd.serve_forever()
        #httpd.handle_request()



