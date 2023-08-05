from flask import request, has_request_context
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

    def __init__(self, id: str, username: str, role: str, last_login: str, created: str, enabled: bool, visible: bool):
        self.id = id
        self.username = username
        self.role = role
        self.last_login = last_login
        self.created = created
        self.enabled = enabled
        self.visible: visible


def _get_user():
    log(f"Checking if authenticated..", "debug")
    try:
        auth_header = request.headers.get("Authorization", None)
        if auth_header:
            log(f"got auth_header", "debug")
            verified_header = validate_authorization_header(auth_header)
            if verified_header["success"] == "true":
                log(f"got verified_header: {verified_header}", "debug")
                user_data = verified_header["result"]
                user = User(
                    id=user_data["id"],
                    username=user_data["username"],
                    role=user_data["username"],
                    last_login=user_data["username"],
                    created=user_data["username"],
                    enabled=user_data["enabled"],
                    visible=user_data["visible"]
                )
                log(f"returning user_data: {user_data}", "debug")
                return user
    except Exception as e:
        log(f"Could not verify Authorization header. Error: {e}", "error")
        return {
                   "success": "false",
                   "message": f"Could not verify Authorization header. Error: {e}"
               }, 401


class authorized_groups(object):
    def __init__(self, groups: list):
        self.groups = groups

    def __call__(self, func):

        @wraps(func)
        def callable(*args, **kwargs):
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
