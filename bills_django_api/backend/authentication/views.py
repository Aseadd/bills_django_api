from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Bill, Payment, Report, Reminder, Customer, Product, SwiftConnection
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError
from rest_framework import status
from .serializers import BillSerializer, CustomerSerializer, ProductSerializer, SwiftConnectionSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
import stripe
import json
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import Group, Permission

stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

class UserView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        return Response("User Deleted Successfully")

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    

class Loginview(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        print("Received from React", email, password)
        
        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Account does  not exist")

        if user is None:
            raise AuthenticationFailed("User does not exist")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")
        access_token = str(AccessToken.for_user(user))
        refresh_token = str(RefreshToken.for_user(user))
        return Response({
            "access_token" : access_token,
            "refresh_token" : refresh_token
        })
    
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response("Logout Successful", status=status.HTTP_200_OK)
        except TokenError:
            raise AuthenticationFailed("Invalid Token")

# Create view for Bills
# Path: bills/views.py
class BillsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        bills = Bill.objects.all()
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # if not request.user.is_authenticated:
        #     return Response({"error": "User is not authenticated."}, status=401)
        serializer = BillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Bill Created Successfully")
    def delete(self, request, id):    
        bill = Bill.objects.get(id=id)
        bill.delete()
        return Response("Bill Deleted Successfully")

class BillDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            bill = Bill.objects.get(id=id)
            serializer = BillSerializer(bill)
            return Response(serializer.data)
        except Bill.DoesNotExist:
            return Response({'error': 'Bill not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, id):
        try:
            bill = Bill.objects.get(id=id)
            serializer = BillSerializer(instance=bill, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Bill.DoesNotExist:
            return Response({'error': 'Bill not found'}, status=status.HTTP_404_NOT_FOUND)
    
class BillCreateView(APIView):
    def post(self, request):
        serializer = BillSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class CustomerView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self, request, pk):
        customer = Customer.objects.get(id=pk)
        customer.delete()
        return Response("Customer Deleted Successfully")

@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount', None)
        if amount is None:
            amount = 2000
        if amount is not None:
            try:
                # Convert amount to float before multiplying
                amount_float = float(amount)

                # Use int(amount_float) to convert the float to an integer
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(amount_float * 100),
                    currency='usd',
                )

                Payment.objects.create(
                    amount=amount_float,
                    status=request.POST.get('status', ''),  # Assuming 'status' is also part of the request
                    transaction_id=request.POST.get('transaction_id', ''),
                )

                return JsonResponse({'clientSecret': payment_intent.client_secret})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'error': 'Amount not provided'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.headers['Stripe-Signature']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, 'your_endpoint_secret'
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  
    return HttpResponse(status=200)

admin_group, created = Group.objects.get_or_create(name='Admin')
if created:
    admin_group.permissions.add(Permission.objects.get(codename='admin_permissions'))

# Create Biller group
biller_group, created = Group.objects.get_or_create(name='Biller')
if created:
    biller_group.permissions.add(Permission.objects.get(codename='biller_permissions'))

# Create Customer group
customer_group, created = Group.objects.get_or_create(name='Customer')
if created:
    customer_group.permissions.add(Permission.objects.get(codename='customer_permissions'))

customer_user = User.objects.get(email="at@gmail.com")
customer_user.groups.add(customer_group)

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Product Created Successfully")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SwiftConnectionView(APIView):
    def get(self, request):
        connections = SwiftConnection.objects.all()
        serializer = SwiftConnectionSerializer(connections, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SwiftConnectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Connection Created Successfully")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)