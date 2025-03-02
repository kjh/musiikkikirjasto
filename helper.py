from functools import wraps
from flask import session, abort

def require_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            abort(403)  # Forbidden
        return func(*args, **kwargs)
    return decorated_function
    