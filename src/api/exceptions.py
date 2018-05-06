import json


class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def init(self, code):
        super(ClientError, self).init(code)
        self.code = code

    def send_to(self, channel):
        channel.send({
            "text": json.dumps({
                "error": self.code,
            }),
        })