import json
from base64 import urlsafe_b64decode
from flask import Request, jsonify, abort
from .call import call
from .db import Types

asset_path_templates = {
    Types.WORKSPACES: "workspaces/{wid}",
    Types.CONFIGURATIONS: "workspaces/{wid}/configurations/{cid}",
    Types.STATES: "workspaces/{wid}/configurations/{cid}/states/{sid}",
    Types.PARAM_SETS: "workspaces/{wid}/configurations/{cid}/states/{sid}/paramSets/{pid}",
}


def authorize(request, asset, permission):
    uid = user_info(request)["user_id"]
    resp = call("check_permission", uid=uid, asset=asset, permission=permission)
    if not resp["granted"]:
        resp = jsonify(message="Access denied")
        resp.status_code = 403
        abort(resp)


def auth(permission):
    def wrap(func):
        def wrapped_func(request: Request):
            asset_type = permission.split(".")[0]
            try:
                asset = asset_path_templates[asset_type].format(**request.json)
            except KeyError as e:
                resp = jsonify(message=f"Missing key: {e}")
                resp.status_code = 400
                abort(resp)
            authorize(request, asset, permission)
            request.headers["X-Authorized-Asset"] = asset
            return func(request)

        return wrapped_func

    return wrap


def authorized_asset(request: Request):
    return request.headers.get("X-Authorized-Asset")


def user_info(request):
    encoded_user_info = request.headers.get("X-Endpoint-Api-Userinfo")
    if encoded_user_info:
        if not encoded_user_info.endswith("=="):
            encoded_user_info += "=="
        return json.loads(urlsafe_b64decode(encoded_user_info))
    return None

