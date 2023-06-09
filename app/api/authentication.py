from flask_httpauth import HTTPBasicAuth
from .error import unauthorized
from .error import forbidden

auth =HTTPBasicAuth()

@auth.verify_password
def verify_password(email, password):
    if email == '':
        return False

    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    return unauthorized('Invalide credentials')


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and g.current_user.confirmed:
        return forbidded('Uncornfirmed account')
