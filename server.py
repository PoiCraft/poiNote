from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from poiNote import app

http_server = WSGIServer(('0.0.0.0', 5002), app,
                         handler_class=WebSocketHandler)
http_server.serve_forever()
