import os
import time
from vodafone_ie_account_checker import api

username = os.getenv("VF_USERNAME", "empty-username")
password = os.getenv("VF_PASSWORD", "empty-password")
token1 = os.getenv("VERIFICATION_TOKEN_1", "empty-token1")
token2 = os.getenv("VERIFICATION_TOKEN_2", "empty-token2")

# api = api.Account(username, password, token1, token2)
# api.get_account_usage_request()
# time.sleep(5)
#
# api.get_account_usage_request()
