import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = 'Af6Nxex4XS0OisTJH2XfObnqbIZ77tNvEwj7zOaY_beb24kGTj-7fUs97Kc_AL4y749VQYtpOzE3xqL9'
        self.client_secret = 'EGFPq5SvhBBflwIBza5G1d1NEAebjPUXJCXUN3tcOX5SBaATM7EWSxduHGrJFgmbpZyNy_hxYFlFU9Tk'
        self.environment = SandboxEnvironment(
            client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
