import requests
import time

class Manager:
    def __init__(self, api_key="0Bf9SfGlW_VDL85-iUPzR5cnzi3ApXsuOyY6La6F-2EB", token_expiration=300):  # Cache for 5 minutes (300 seconds) by default
        self.api_key = api_key
        self.token_expiration = token_expiration
        self._token = None
        self._token_timestamp = None

    def _get_new_token(self):
        iam_url = "https://iam.cloud.ibm.com/identity/token"
        auth_response = requests.post(
            iam_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=f"apikey={self.api_key}&grant_type=urn:ibm:params:oauth:grant-type:apikey"
        )

        if auth_response.status_code != 200:
            raise Exception("Failed to obtain access token: " + auth_response.text)

        # Update the token and timestamp
        self._token = auth_response.json().get("access_token")
        self._token_timestamp = time.time()
        return self._token

    def get_access_token(self):
        # Check if token is already present and not expired
        if self._token and (time.time() - self._token_timestamp) < self.token_expiration:
            return self._token
        else:
            return self._get_new_token()
