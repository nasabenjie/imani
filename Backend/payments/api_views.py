import uuid
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Payment
from .serializers import PaymentSerializer, InitiatePaymentSerializer
from .mtn_service import MTNMoMoService
from .airtel_service import AirtelMoneyService
from orders.models import Order


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    """
    Initiate a mobile money payment for an order.
    Sends a payment prompt to the customer's phone.
    """
    serializer = InitiatePaymentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    order = get_object_or_404(Order, id=data["order_id"], user=request.user)

    # Check order is in a payable state
    if order.payment_status == Order.PaymentStatus.PAID:
        return Response(
            {"error": "Order is already paid"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if order.status == Order.Status.CANCELLED:
        return Response(
            {"error": "Cannot pay for a cancelled order"},
            status=status.HTTP_400_BAD_REQUEST
        )

    provider = data["provider"]
    phone = data["phone"]
    internal_reference = f"IMANI-{order.id}-{uuid.uuid4().hex[:8].upper()}"

    try:
        if provider == Payment.Provider.MTN:
            service = MTNMoMoService()
        else:
            service = AirtelMoneyService()

        provider_reference, status_code, response_data = service.request_payment(
            phone=phone,
            amount=order.total,
            reference=internal_reference,
        )

        # Create payment record
        payment = Payment.objects.create(
            order=order,
            user=request.user,
            provider=provider,
            amount=order.total,
            phone=phone,
            internal_reference=internal_reference,
            provider_reference=provider_reference,
            provider_response=response_data,
        )

        return Response({
            "message": "Payment request sent to your phone. Please approve it.",
            "payment": PaymentSerializer(payment).data,
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {"error": f"Payment initiation failed: {str(e)}"},
            status=status.HTTP_502_BAD_GATEWAY
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def check_payment(request, payment_id):
    """
    Check and update the status of a payment.
    Call this after the customer approves the payment on their phone.
    """
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)

    if payment.status == Payment.Status.SUCCESS:
        return Response(PaymentSerializer(payment).data)

    try:
        if payment.provider == Payment.Provider.MTN:
            service = MTNMoMoService()
        else:
            service = AirtelMoneyService()

        result = service.check_payment_status(payment.provider_reference)

        # Map provider status to our status
        provider_status = result.get("status", "").upper()

        with transaction.atomic():
            if provider_status == "SUCCESSFUL":
                payment.status = Payment.Status.SUCCESS
                payment.provider_response = result
                payment.save()

                # Update order payment status
                payment.order.payment_status = Order.PaymentStatus.PAID
                payment.order.payment_reference = payment.provider_reference
                payment.order.save()

            elif provider_status in ["FAILED", "REJECTED", "TIMEOUT"]:
                payment.status = Payment.Status.FAILED
                payment.provider_response = result
                payment.save()

                payment.order.payment_status = Order.PaymentStatus.FAILED
                payment.order.save()

        return Response(PaymentSerializer(payment).data)

    except Exception as e:
        return Response(
            {"error": f"Status check failed: {str(e)}"},
            status=status.HTTP_502_BAD_GATEWAY
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def payment_history(request):
    """List all payments for the logged in user."""
    payments = Payment.objects.filter(user=request.user).select_related("order")
    return Response(PaymentSerializer(payments, many=True).data)


@api_view(["POST"])
@permission_classes([AllowAny])
def mtn_callback(request):
    """
    Webhook endpoint for MTN payment callbacks.
    MTN calls this URL when a payment is completed.
    """
    data = request.data
    external_id = data.get("externalId") or data.get("referenceId")

    if not external_id:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        payment = Payment.objects.get(provider_reference=external_id)
        provider_status = data.get("status", "").upper()

        with transaction.atomic():
            if provider_status == "SUCCESSFUL":
                payment.status = Payment.Status.SUCCESS
                payment.provider_response = data
                payment.save()

                payment.order.payment_status = Order.PaymentStatus.PAID
                payment.order.payment_reference = external_id
                payment.order.save()

            elif provider_status in ["FAILED", "REJECTED"]:
                payment.status = Payment.Status.FAILED
                payment.provider_response = data
                payment.save()

                payment.order.payment_status = Order.PaymentStatus.FAILED
                payment.order.save()

    except Payment.DoesNotExist:
        pass

    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def airtel_callback(request):
    """
    Webhook endpoint for Airtel Money callbacks.
    Airtel calls this URL when a payment is completed.
    """
    data = request.data
    transaction_id = data.get("transaction", {}).get("id")

    if not transaction_id:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        payment = Payment.objects.get(provider_reference=transaction_id)
        transaction_status = data.get("transaction", {}).get("status", "").upper()

        with transaction.atomic():
            if transaction_status == "TS":  # Airtel uses "TS" for success
                payment.status = Payment.Status.SUCCESS
                payment.provider_response = data
                payment.save()

                payment.order.payment_status = Order.PaymentStatus.PAID
                payment.order.payment_reference = transaction_id
                payment.order.save()

            elif transaction_status in ["TF", "TA"]:  # TF=failed, TA=cancelled
                payment.status = Payment.Status.FAILED
                payment.provider_response = data
                payment.save()

                payment.order.payment_status = Order.PaymentStatus.FAILED
                payment.order.save()

    except Payment.DoesNotExist:
        pass

    return Response(status=status.HTTP_200_OK)