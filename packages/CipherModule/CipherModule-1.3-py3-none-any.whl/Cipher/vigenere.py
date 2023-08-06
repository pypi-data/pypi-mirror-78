class Vigenere:
    @staticmethod
    def encode(text, key):
        result = []
        key = (key * (len(text) // len(key))) + key[:len(text) % len(key)]

        for i in range(len(text)):

            if text[i].isalpha() and key[i].isalpha():

                keyCode = ord(key[i].lower()) - 96
                textCode = ord(text[i].lower()) - 96

                ans = textCode + keyCode - 1

                if ans > 26:
                    ans -= 26

                if text[i].isupper():
                    result.append(chr(ans + 96).upper())
                else:
                    result.append(chr(ans + 96))

            else:
                result.append(text[i])

        return "".join(result)

    @staticmethod
    def decode(code, key):
        result = []
        key = (key * (len(code) // len(key))) + key[:len(code) % len(key)]

        for i in range(len(code)):

            if code[i].isalpha() and key[i].isalpha():

                keyCode = ord(key[i].lower()) - 96
                codeCode = ord(code[i].lower()) - 96

                ans = codeCode - keyCode + 1

                if ans < 1:
                    ans += 26

                if code[i].isupper():
                    result.append(chr(ans + 96).upper())
                else:
                    result.append(chr(ans + 96))

            else:
                result.append(code[i])

        return "".join(result)