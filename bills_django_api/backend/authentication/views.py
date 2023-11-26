from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Bill, Payment, Report, Reminder, Customer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError
from rest_framework import status
from .serializers import BillSerializer, CustomerSerializer
from rest_framework.permissions import IsAuthenticated

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
    def delete(self, request, pk):
        user = User.objects.get(id=pk)
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
    def delete(self, request, pk):
        bill = Bill.objects.get(id=pk)
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
    
    def delete(self, request, id):
        try:
            bill = Bill.objects.get(id=id)
            bill.delete()
            return Response("Bill Deleted Successfully")
        except Bill.DoesNotExist:
            return Response({'error': 'Bill not found'}, status=status.HTTP_404_NOT_FOUND)

 # Create Bills view in urls.py
# Path: bills/urls.py
# class BillCreateView(APIView):
#     def post(self, request):
#         serializer = BillSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(user=request.user)
#         return Response(serializer.data)

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