from django.db import models
from django.conf import settings
from orders.models import Order


class Payment(models.Model):

    class Provider(models.TextChoices):
        MTN = "mtn", "MTN Mobile Money"
        AIRTEL = "airtel", "Airtel Money"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name="payments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="payments"
    )
    provider = models.CharField(max_length=10, choices=Provider.choices)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )

    # Amount
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=5, default="UGX")

    # Phone number used for payment
    phone = models.CharField(max_length=20)

    # Provider references
    provider_reference = models.CharField(
        max_length=200,
        blank=True,
        help_text="Transaction ID from MTN or Airtel"
    )
    internal_reference = models.CharField(
        max_length=200,
        unique=True,
        help_text="Our internal payment reference"
    )

    # Raw response from provider (for debugging)
    provider_response = models.JSONField(default=dict, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order", "status"]),
            models.Index(fields=["provider", "status"]),
        ]

    def __str__(self):
        return f"{self.provider} payment {self.internal_reference} — {self.status}"