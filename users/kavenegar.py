from kavenegar import *
from django.conf import settings


def sendLoginSMS(receptor, otp):
    try:
        # api = KavenegarAPI(settings.KAVENEGAR_KEY)
        params = {
            "receptor": receptor,
            "token": otp,
            "template": "test"
        }
        print(params)

        # response = api.verify_lookup(params)
    except APIException as a:
        print(a)
    except HTTPException as h:
        print(h)
