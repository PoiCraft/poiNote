from gevent.pywsgi import WSGIServer
from poiNote import app

http_server = WSGIServer(('', 5002), app)
http_server.serve_forever()
