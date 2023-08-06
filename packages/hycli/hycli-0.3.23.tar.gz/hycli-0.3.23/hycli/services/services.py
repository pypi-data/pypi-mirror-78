import requests

from halo import Halo

from .requests import request_token


class Services(object):
    def __init__(self, ctx, check_up=False):
        """
        TODO: put correct endpoints to check if online
        extractor: '/'
        vat_validator: https://github.com/hypatos/vat-validator/pull/36
        """
        config = ctx.obj["config"]
        endpoints = config["endpoints"]

        self.env = ctx.obj.get("env")
        self.headers = ctx.obj.get("headers")
        self.username = config.get("username")
        self.password = config.get("password")
        self.authentication_endpoint = endpoints.get("authentication")

        if check_up:
            self.are_up(endpoints)

        self.extractor_endpoint = endpoints.get("extractor")
        self.vat_validator_endpoint = endpoints.get("vat_validation")
        self.validation_endpoint = endpoints.get("validation")

        self.token = None
        self.refresh_token()

    def are_up(self, endpoints):
        """ Check if endpoints are reachable. """
        for name, url in endpoints.items():
            url_spinner = Halo(spinner="dots")
            svc = name.capitalize()

            try:
                req = requests.get(url)

            # On connection error.
            except requests.exceptions.ConnectionError:
                url_spinner.fail(f"{svc} on endpoint {url} is offline\n")
                endpoints[name] = None
                if name == "extractor":
                    quit(f"Expected extraction service on {url}, service is mandatory.")

            # Connection was successful on 401 and 405.
            else:
                if req.status_code == 401 or req.status_code == 405:
                    url_spinner.succeed(f"{svc} endpoint is online\n")
                else:
                    url_spinner.fail(f"{svc} endpoint returns {req.status_code}\n")
                    endpoints[name] = None

    def refresh_token(self):
        if self.env != "localhost":
            self.token = request_token(
                self.authentication_endpoint, self.username, self.password
            )
