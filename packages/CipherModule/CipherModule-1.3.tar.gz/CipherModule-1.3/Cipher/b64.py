import base64

class B64:
    @staticmethod
    def encode(text):
        return (base64.b64encode(text.encode())).decode()
    @staticmethod
    def decode(code):
        return base64.b64decode(code).decode()