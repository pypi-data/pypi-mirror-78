class A1Z26:
    @staticmethod
    def encode(text):
        result = []
        for i in text:
            if i.isalpha():
                result.append(str(ord(i.lower()) - 96))
            else:
                result.append(i)
        return " - ".join(result)

    @staticmethod
    def decode(code):
        result = []
        code = code.split(" - ")
        for i in code:
            if i.isnumeric():
                result.append(chr(int(i) + 96))
            else:
                result.append(i)
        return "".join(result)