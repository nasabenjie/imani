import uuid
import requests
from django.conf import settings


class AirtelMoneyService:
    """
    Airtel Money Collections API.
    Docs: https://developers.airtel.africa/documentation
    """

    SANDBOX_BASE_URL = "https://openapiuat.airtel.africa"
    PRODUCTION_BASE_URL = "https://openapi.airtel.africa"

    def __init__(self):
        self.sandbox = settings.AIRTEL_SANDBOX
        self.base_url = self.SANDBOX_BASE_URL if self.sandbox else self.PRODUCTION_BASE_URL
        self.client_id = settings.AIRTEL_CLIENT_ID
        self.client_secret = settings.AIRTEL_CLIENT_SECRET

    def _get_access_token(self):
        """Get OAuth access token from Airtel."""
        response = requests.post(
            f"{self.base_url}/auth/oauth2/token",
            json={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
            },
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def request_payment(self, phone, amount, reference, note="IMANI Order Payment"):
        """
        Request payment from a customer's Airtel Money account.
        Returns the transaction_id and raw response.
        """
        access_token = self._get_access_token()
        transaction_id = str(uuid.uuid4())

        # Normalize phone
        phone = self._normalize_phone(phone)

        payload = {
            "reference": note,
            "subscriber": {
                "country": "UG",
                "currency": "UGX",
                "msisdn": phone,
            },
            "transaction": {
                "amount": str(amount),
                "country": "UG",
                "currency": "UGX",
                "id": transaction_id,
            }
        }

        response = requests.post(
            f"{self.base_url}/merchant/v2/payments/",
            json=payload,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "X-Country": "UG",
                "X-Currency": "UGX",
            }
        )

        data = response.json()
        return transaction_id, response.status_code, data

    def check_payment_status(self, transaction_id):
        """Check the status of a payment."""
        access_token = self._get_access_token()

        response = requests.get(
            f"{self.base_url}/standard/v1/payments/{transaction_id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-Country": "UG",
                "X-Currency": "UGX",
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