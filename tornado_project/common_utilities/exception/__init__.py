from tornado import escape
from tornado.web import HTTPError


class HTTPAPIError(HTTPError):

    def __init__(self, code, status_code=200, error_detail="", error_type="",
                 response="", log_message=None, *args):
        self.code = code
        super(HTTPAPIError, self).__init__(int(status_code), log_message, *args)

        self.error_type = error_type if error_type else \
            _error_types.get(self.code, "unknown_error")
        self.error_detail = error_detail
        self.response = response if response else {}

    def __str__(self):
        err = {"code": self.code, "msg": self.error_type}
        self._set_err(err, ["response"])

        if self.error_detail:
            err["error_details"] = self.error_detail

        return escape.json_encode(err)

    def _set_err(self, err, names):
        for name in names:
            v = getattr(self, name)
            if v:
                err[name] = v


_error_types = {
    10001: "system busy",
    10011: "param_error",
}
