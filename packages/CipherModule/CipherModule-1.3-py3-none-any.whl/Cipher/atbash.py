class Atbash:
    @staticmethod
    def encode(text):
        return text[::-1]
    @staticmethod
    def decode(code):
        return code[::-1]