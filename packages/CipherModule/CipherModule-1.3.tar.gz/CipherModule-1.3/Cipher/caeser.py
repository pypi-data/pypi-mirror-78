class Caesar:
    @staticmethod
    def encode(code, number):
        result = []
        for i in code:
            index = ord(i) + number
            if index > 126:
                index -= 95
            result.append(chr(index))
        return "".join(result)

    @staticmethod
    def decode(code, number):
        result = []
        for i in code:
            index = ord(i) - number
            if index < 32:
                index += 95
            result.append(chr(index))
        return "".join(result)