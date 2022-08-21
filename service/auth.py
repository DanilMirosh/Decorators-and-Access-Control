import base64
import calendar
import datetime
import hashlib
import jwt

from flask import current_app


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=current_app.config['PWD_HASH_SALT'],
        iterations=current_app.config['PWD_HASH_ITERATIONS']
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compare_password_hash(password_hash, other_password) -> bool:
    return password_hash == generate_password_hash(other_password)


def generate_token(username, password_hash, password, role, is_refresh=False):
    if username is None:
        return None

    if not is_refresh:
        if not compare_password_hash(password_hash=password_hash, other_password=password):
            return None

    data = {
        'username': username,
        'password': password
    }

    # 15 min for access_token
    min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
    data['exp'] = calendar.timegm(min15.timetuple())
    access_token = jwt.encode(data,
                              key=current_app.config['SECRET_HERE'],
                              algorithm=current_app.config['ALGORITHM']
                              )

    # 130 day for refresh_token
    day130 = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['TOKEN_EXPIRE_DAY'])
    data['exp'] = calendar.timegm(day130.timetuple())
    refresh_token = jwt.encode(data,
                               key=current_app.config['SECRET_HERE'],
                               algorithm=current_app.config['ALGORITHM']
                               )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def approve_token(token, user_service):
    data = jwt.decode(token,
                      key=current_app.config['SECRET_HERE'],
                      algorithms=current_app.config['ALGORITHM']
                      )

    username = data.get('username')
    password = data.get('password')
    role = user_service.get_by_username(username)
    return generate_token(username=username,
                          password=password,
                          role=role,
                          password_hash=None,
                          is_refresh=True)
