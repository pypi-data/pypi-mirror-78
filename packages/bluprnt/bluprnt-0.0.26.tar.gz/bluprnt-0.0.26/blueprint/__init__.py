from flask import Request
from .auth import user_info


class ParsedRequest:
    def __init__(self, request: Request):
        data = request.json
        self.user_info = user_info(request)
        self.data = data
        self.repo = "{}-{}".format(data.get("wid"), data.get("cid"))
        self.change_ref = "{}/{}/{}".format(
            data.get("sid"), self.user_info.get("user_id"), data.get("change_id")
        )
        self.plan_ref = "tf/plan/{}".format(self.change_ref)
        self.apply_ref = "tf/apply/{}".format(data.get("sid"))
        self.source_apply_ref = "tf/apply/{}".format(data.get("source_sid"))
