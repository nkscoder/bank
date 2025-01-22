from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Account
from .serializers import AccountSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import send_to_rabbitmq  # Assuming this is a custom function in utils

@api_view(['POST'])
def create_account(request):
    email = request.data.get('email')
    password = request.data.get('password')
    account_number = request.data.get('account_number')
    pin = request.data.get('pin')

    if not email or not password or not account_number or not pin:
        return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

    # Create User instance
    user = User.objects.create_user(username=email, email=email, password=password)

    # Create Account instance
    account_data = {
        'user': user.id,
        'account_number': account_number,
        'pin': pin,
        'balance': 0.00  # Default balance
    }
    serializer = AccountSerializer(data=account_data)

    if serializer.is_valid():
        account = serializer.save()

        # Send account data to RabbitMQ to update ATM database
        send_to_rabbitmq({
            'account_number': account.account_number,
            'pin': account.pin,
            'balance': str(account.balance),
        })

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        response_data = {
            'account': serializer.data,
            'access_token': access_token,
            'refresh_token': str(refresh)
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if not user.check_password(password):
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    
    return Response({
        'access_token': access_token,
        'refresh_token': str(refresh)
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_account_details(request):
    user = request.user  # Extract user directly from the request object

    try:
        account = Account.objects.get(user=user)
    except Account.DoesNotExist:
        return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AccountSerializer(account)
    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def get_account_details(request):
    try:
        # Get the user from the JWT token
        user = request.user
        
        # Retrieve the account linked to the user
        account = Account.objects.get(user=user)
        
        # Serialize the account data
        serializer = AccountSerializer(account)
        
        # Return the account details
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Account.DoesNotExist:
        return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
