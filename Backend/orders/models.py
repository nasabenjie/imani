from django.db import models
from django.db import models
from django.conf import settings
from products.models import Product
from supermarkets.models import Supermarket


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        PREPARING = "preparing", "Preparing"
        OUT_FOR_DELIVERY = "out_for_delivery", "Out for Delivery"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    class PaymentStatus(models.TextChoices):
        UNPAID = "unpaid", "Unpaid"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    class PaymentMethod(models.TextChoices):
        MTN = "mtn", "MTN Mobile Money"
        AIRTEL = "airtel", "Airtel Money"
        CASH = "cash", "Cash on Delivery"

    # Relations
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,      
        related_name="orders"
    )
    supermarket = models.ForeignKey(
        Supermarket,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True                   
    )

    # Payment
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.UNPAID,
        db_index=True
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH
    )
    payment_reference = models.CharField(
        max_length=100,
        blank=True,
        help_text="MTN/Airtel transaction ID"
    )

    # Delivery
    delivery_address = models.TextField()
    delivery_phone = models.CharField(max_length=20)
    delivery_notes = models.TextField(blank=True)

    # Financials
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]      # newest orders first
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["supermarket", "status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Order #{self.id} — {self.user} — {self.status}"

    @property
    def item_count(self):
        return self.items.count()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,      
        related_name="order_items"
    )

    # Snapshot price at time of order — never changes even if product price changes
    product_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=["order"]),
        ]

    def save(self, *args, **kwargs):
        # Auto calculate total_price
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} x {self.quantity} — Order #{self.order.id}"