from base64 import b64decode, b64encode
from urllib.parse import quote, unquote


class Common:
    @staticmethod
    def encode_cursor(cursor):
        return quote(b64encode(cursor))

    @staticmethod
    def decode_cursor(cursor):
        return b64decode(unquote(cursor))
