import jwt
from flask import request, current_app

from implemented import user_service


def auth_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')

        if not token:
            raise "Not token"

        try:
            jwt.decode(token,
                       key=current_app.config['SECRET_HERE'],
                       algorithms=current_app.config['ALGORITHM'])
            return func(*args, **kwargs)


        except Exception:
            raise Exception

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')

        if not token:
            raise Exception

        try:
            data = jwt.decode(token,
                              key=current_app.config['SECRET_HERE'],
                              algorithms=current_app.config['ALGORITHM'])
            if user_service.get_by_username(data['username']).role == 'admin':
                return func(*args, **kwargs)
            else:
                return 'У вас нет прав администратора'
        except Exception:
            raise Exception

    return wrapper
