"""
Views for payments app.
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Payment, BoostPackage
from .serializers import PaymentSerializer, BoostPackageSerializer


class PaymentListView(generics.ListAPIView):
    """
    List user's payments.
    """
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class BoostPackageListView(generics.ListAPIView):
    """
    List available boost packages.
    """
    queryset = BoostPackage.objects.filter(is_active=True)
    serializer_class = BoostPackageSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_payment_intent(request):
    """
    Create a Stripe payment intent.
    """
    # This is a simplified version - in production you'd integrate with Stripe
    amount = request.data.get('amount')
    currency = request.data.get('currency', 'USD')
    
    if not amount:
        return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create payment record
    payment = Payment.objects.create(
        user=request.user,
        amount=amount,
        currency=currency,
        description=request.data.get('description', '')
    )
    
    return Response({
        'payment_id': payment.id,
        'client_secret': f'demo_secret_{payment.id}',
        'amount': amount,
        'currency': currency
    })