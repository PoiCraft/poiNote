import json
import hashlib

from geventwebsocket.websocket import WebSocket


class WebSocketCollector:
    ws_client = {}
    ws_client_len = {}

    def add(self, ws: WebSocket, name: str):
        self.ws_client_len[name] = self.ws_client_len.get(name, 0) + 1
        self.ws_client[name] = self.ws_client.get(name, {})
        self.ws_client[name][self.ws_client_len[name]] = ws
        return self.ws_client_len[name] - 1

    def sent_to_all(self, name: str, title: str, body: str):
        clients = self.ws_client[name].copy()
        for k in clients:
            if not clients[k].closed:
                clients[k].send(json.dumps(
                    {
                        'name': name,
                        'title': title,
                        'body': body,
                        'md5': hashlib.md5((title+body).encode(encoding='utf8')).hexdigest()
                    },
                    ensure_ascii=False))
            else:
                del self.ws_client[k]
