import time
import jwt
from config import settings

JWT_SECRET = settings.JWT_SECRET
JET_ALGORITHM = settings.JWT_ALGORITHM


def token_response(token: str):
    return{
        'token': token
    }


def signJWT(userID: int):
    payload = {
        "userID": userID,
        "expiry": time.time() + 86400
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JET_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JET_ALGORITHM)
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return {}