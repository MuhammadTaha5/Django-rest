from django.shortcuts import render
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .userSerializers import UserSerializer, loginSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

class login(APIView):
    permission_classes = [AllowAny]
    #allow all users to access the login url
    #post method to send login credential
    def post(self, request):
        reqData = request.data  #to extract payload from post request
        userSerial = loginSerializer(data=reqData)
        #serializing the data
        #checking data matches with the User model
        if userSerial.is_valid():
            username = userSerial.validated_data['username']
            password = userSerial.validated_data['password']
            #authenticating the user exist in db
            userCheck = authenticate(username=username, password=password)

            if userCheck:
                #Generating the jwt token
                refresh = RefreshToken.for_user(userCheck)
                #sending the response of access, and refresh token
                return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            
            #if authentication fails, send login fail response
            return Response({
                'status': 'Login Failed',
                'message': 'Incorrect Fields'   
            }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            #returning response if request data doesnt match with login serializer
            return Response({
                'status': 'Failed',
                'message': userSerial.errors
            }, status=status.HTTP_401_UNAUTHORIZED)

#creating class based views
class users(APIView):
    #only authenticated user can access these methods(get, put, delete, post)
    permission_classes = [IsAuthenticated]
    #post method to create user
    def post(self, request):
        reqData = request.data
        #extract the request dat from main request
        serialize = UserSerializer(data=reqData)
        #serializing the incoming data
        if serialize.is_valid():
            #adding the 
            serialize.save()

            return Response({
                'status' : 'success',
                'data': serialize.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': 'failed',
                'message': serialize.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        city = request.query_params.get('city', None)
        if city:
            userByCity = User.objects.filter(city__iexact=city )
            serialize = UserSerializer(userByCity, many=True)
            return Response({
                    'status': 'success',
                    'data': serialize.data
                }, status=status.HTTP_200_OK)
                
        user_data = User.objects.all()
        serial = UserSerializer(user_data, many=True)
        if serial.is_valid:
            return Response({
                'status': 'success',
                'data': serial.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': serial.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
class UserDetail(APIView):
    #check if user is authenticated or not
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            user = User.objects.get(user_id=id)  #fetching the user by Id
        except User.DoesNotExist:   ##checking if user exist
            #returning the Response if user not found
            return Response({   
                'status': 'failed',
                'message': f'User with id {id} not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        try:
            userById = User.objects.get(user_id=id)    
        except User.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': f'User with id {id} not found'
            }, status=status.HTTP_404_NOT_FOUND)
        serialize = UserSerializer(userById, data = request.data)
        print(request.data)
        if serialize.is_valid():
            serialize.save()
            return Response({
                'status': 'Success',
                'message': 'Data Updated',
                'data': serialize.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'Failed',
                'message': serialize.errors,
                'data': serialize.data
            }, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, id):
        requestData = request.data
        try:
            userById = User.objects.get(user_id=id)
        except User.DoesNotExist:
            return Response({
                'status': 'Failed',
                'message': f"No user exist with id {id}"
            }, status=status.HTTP_404_NOT_FOUND)
        
        userById.delete()
        return Response({
            'status':'Success',
            'message': f'User Deleted with id {id}',
            
        }, status=status.HTTP_200_OK)
        
