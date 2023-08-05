from flask import request, has_request_context, _request_ctx_stack
from werkzeug.local import LocalProxy

from factionpy.logger import log
from functools import wraps
from factionpy.services import validate_authorization_header

standard_read = [
    'super-user',
    'user',
    'read-only'
]

standard_write = [
    'super-user',
    'user'
]

current_user = LocalProxy(lambda: _get_user())


class User(object):
    id = None
    username = None
    role = None
    last_login = None
    created = None
    enabled = False
    visible = False

    def __init__(self,
                 id: str = None,
                 username: str = None,
                 role: str = None,
                 last_login: str = None,
                 created: str = None,
                 enabled: bool = False,
                 visible: bool = False):
        self.id = id
        self.username = username
        self.role = role
        self.last_login = last_login
        self.created = created
        self.enabled = enabled
        self.visible: visible


def _load_user():
    """
    This populates the User value of the request context. It first creates a default user object for an anonymous
    user (enabled set to false). It then tries to authenticate the request from its API key. If the API key returns
    a valid user, the anonymous user details are updated to that of the authenticated user.
    """
    log(f"Checking if authenticated..", "debug")
    user = User()
    try:
        auth_header = request.headers.get("Authorization", None)
        if auth_header:
            log(f"got auth_header", "debug")
            verified_header = validate_authorization_header(auth_header)
            if verified_header["success"] == "true":
                log(f"got verified_header: {verified_header}", "debug")
                user_data = verified_header["result"]
                user.id = user_data["id"],
                user.username = user_data["username"],
                user.role = user_data["username"],
                user.last_login = user_data["username"],
                user.created = user_data["username"],
                user.enabled = user_data["enabled"],
                user.visible = user_data["visible"]
                log(f"returning user_data: {user_data}", "debug")
    except Exception as e:
        log(f"Could not verify Authorization header. Error: {e}", "error")
    ctx = _request_ctx_stack.top
    ctx.user = user


def _get_user():
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'user'):
        log(f"Loading User", "debug")
        _load_user()
    return getattr(_request_ctx_stack.top, 'user', None)


class authorized_groups(object):
    def __init__(self, groups: list):
        self.groups = groups

    def __call__(self, func):
        @wraps(func)
        def callable(*args, **kwargs):
            log(f"Current user: {current_user.username}")
            groups = self.groups
            if current_user.enabled:
                try:
                    # Replace meta group names with contents of meta group
                    if 'standard_read' in groups:
                        groups.remove('standard_read')
                        groups.extend(standard_read)

                    if 'standard_write' in groups:
                        groups.remove('standard_write')
                        groups.extend(standard_write)

                    if 'all' in groups:
                        authorized = True

                    # Iterate through valid groups, checking if the user is in there.
                    if current_user.role in groups:
                        log(f"user authorized. returning results of function.", "debug")
                        return func(*args, **kwargs)
                    else:
                        log(f"User {current_user.username} is not in the following groups: {groups}")
                except Exception as e:
                    log(f"Could not verify user_data. Error: {e}", "error")
                    pass
            return {
                "success": "false",
                "message": f"Invalid API key provided or you do not have permission to perform this action."
            }, 401

        return callable
