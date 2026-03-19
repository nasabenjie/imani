from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    provider_display = serializers.CharField(source="get_provider_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "provider",
            "provider_display",
            "status",
            "status_display",
            "amount",
            "currency",
            "phone",
            "internal_reference",
            "provider_reference",
            "created_at",
            "updated_at",
        ]


class InitiatePaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    provider = serializers.ChoiceField(choices=Payment.Provider.choices)
    phone = serializers.CharField(max_length=20)

    def validate_phone(self, value):
        """Basic Uganda phone number validation."""
        phone = value.strip().replace(" ", "").replace("+", "")
        if phone.startswith("0"):
            phone = "256" + phone[1:]
        if not phone.startswith("256") or len(phone) != 12:
            raise serializers.ValidationError(
                "Enter a valid Uganda phone number e.g. 0771234567"
            )
        return value