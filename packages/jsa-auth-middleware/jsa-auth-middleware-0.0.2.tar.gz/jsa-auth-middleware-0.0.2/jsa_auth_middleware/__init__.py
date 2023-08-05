import requests
from django.http import HttpResponse
from django.conf import settings

from .query_response import Response

HTTP_HEADER_ENCODING = "iso-8859-1"


class JSAMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response
        self.base_url = settings.AUTH_BASE_URL
        self.failed_status_code = 401
        super().__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, "process_request"):
            response = self.process_request(request)
        response = response or self.get_response(request)
        if hasattr(self, "process_response"):
            response = self.process_response(request, response)

        return response

    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header = request.META.get("HTTP_AUTHORIZATION")

        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    def get_raw_token(self, header, resp):
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            msg = "Empty Authorization header sent"
            resp.message = msg
            return self.send_response(resp, "bad_authorization_header")

        if parts[0] not in ("Bearer"):
            # Assume the header does not contain a JSON web token
            msg = "Missing Authorization Web token type"
            resp.message = msg
            return self.send_response(resp, "bad_authorization_header")

        if len(parts) != 2:
            msg = "Authorization header must contain two space-delimited values"
            resp.message = msg
            return self.send_response(resp, "bad_authorization_header")

        return parts[1]

    def send_response(self, resp, reason, failure=True):
        resp.status_code = self.failed_status_code if failure else 200
        resp.add_param("token_class", "AccessToken")
        resp.add_param("token_type", "access")
        return HttpResponse(
            resp.get_response(),
            status=self.failed_status_code,
            reason=reason,
            content_type="application/json",
        )

    def get_key(self, **kwargs):
        url = self.base_url + "/auth-service/get-key/"
        payload = dict(username=kwargs.get("username"), password=kwargs.get("password"))
        try:
            resp = requests.post(url, data=payload)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            raise e

    def get_auth_token(self, token):
        """
        :param token:
        :return:
        """
        url = self.base_url + "/auth-service/authenticate/"
        header = dict(Authorization="JWT {}".format(token))
        try:
            resp = requests.post(url, headers=header)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            raise e

    def validate(self, token):
        """
        :param token: Authorization token to be validated
        :return: bool True on successful validation and False otherwise
        """
        url = self.base_url + "/auth-service/validate/"
        header = dict(Authorization="Bearer {}".format(token))
        resp = requests.get(url, headers=header)
        if resp.status_code == 200:
            return True

        return False

    def process_request(self, request):
        """
        :param request:
        :return:
        """
        resp = Response()

        header = self.get_header(request)

        if header is None:
            msg = "Empty Authorization header sent"
            resp.message = msg
            return self.send_response(resp, "bad_authorization_header")

        header = header.decode("utf-8")

        raw_token = self.get_raw_token(header, resp)
        if isinstance(raw_token, HttpResponse):
            return raw_token

        validated_token = self.validate(raw_token)
        if not validated_token:
            msg = "Token is invalid or expired"
            resp.message = msg
            return self.send_response(resp, "token_not_valid")

        return
