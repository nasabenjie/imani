import uuid
import requests
import base64
from django.conf import settings


class MTNMoMoService:
    """
    MTN Mobile Money Collections API.
    Docs: https://momodeveloper.mtn.com/docs/services/collection
    """

    SANDBOX_BASE_URL = "https://sandbox.momodeveloper.mtn.com"
    PRODUCTION_BASE_URL = "https://proxy.momoapi.mtn.com"

    def __init__(self):
        self.sandbox = settings.MTN_SANDBOX
        self.base_url = self.SANDBOX_BASE_URL if self.sandbox else self.PRODUCTION_BASE_URL
        self.subscription_key = settings.MTN_SUBSCRIPTION_KEY
        self.api_user = settings.MTN_API_USER
        self.api_key = settings.MTN_API_KEY

    def _get_access_token(self):
        """Get OAuth access token from MTN."""
        credentials = f"{self.api_user}:{self.api_key}"
        encoded = base64.b64encode(credentials.encode()).decode()

        response = requests.post(
            f"{self.base_url}/collection/token/",
            headers={
                "Authorization": f"Basic {encoded}",
                "Ocp-Apim-Subscription-Key": self.subscription_key,
            }
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def request_payment(self, phone, amount, reference, note="IMANI Order Payment"):
        """
        Request payment from a customer's MTN Mobile Money account.
        Returns the external_id (our reference) and raw response.
        """
        access_token = self._get_access_token()
        external_id = str(uuid.uuid4())

        # Normalize phone — MTN expects format: 256XXXXXXXXX
        phone = self._normalize_phone(phone)

        payload = {
            "amount": str(amount),
            "currency": "UGX" if not self.sandbox else "EUR",  # sandbox uses EUR
            "externalId": external_id,
            "payer": {
                "partyIdType": "MSISDN",
                "partyId": phone,
            },
            "payerMessage": note,
            "payeeNote": f"Order {reference}",
        }

        response = requests.post(
            f"{self.base_url}/collection/v1_0/requesttopay",
            json=payload,
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-Reference-Id": external_id,
                "X-Target-Environment": "sandbox" if self.sandbox else "production",
                "Ocp-Apim-Subscription-Key": self.subscription_key,
                "Content-Type": "application/json",
            }
        )

        return external_id, response.status_code, {}

    def check_payment_status(self, external_id):
        """Check the status of a payment request."""
        access_token = self._get_access_token()

        response = requests.get(
            f"{self.base_url}/collection/v1_0/requesttopay/{external_id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-Target-Environment": "sandbox" if self.sandbox else "production",
                "Ocp-Apim-Subscription-Key": self.subscription_key,
            }
        )
        response.raise_for_status()
        return response.json()

    def _normalize_phone(self, phone):
        """Convert 07XXXXXXXX to 2567XXXXXXXX."""
        phone = phone.strip().replace(" ", "").replace("+", "")
        if phone.startswith("0"):
            phone = "256" + phone[1:]
        elif phone.startswith("7") and len(phone) == 9:
            phone = "256" + phone
        return phone