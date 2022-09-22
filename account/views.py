from django.shortcuts import render
from matplotlib.style import context
from yaml import serialize
from account.models import User
from django.contrib.auth import authenticate
from account.serilizers import UserLoginSerializers,UserDeleteBookViewSerializers,UserAddBookViewSerializers, UserPasswordResetViewSerializers,UserRegistrationSerializers,UserProfileSerializers,UserChangePasswordSerializers,SendPasswordEmailSerializers
from .renders import UserRender
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import  Book, Student
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes=[UserRender]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Sucess'},
            status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes=[UserRender]
    def post(self,request,format=None):
        serializer=UserLoginSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)

            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'login Sucess'},
            status=status.HTTP_201_CREATED)

            else:
                return Response({'errors':{'non_field_errors':['email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    renderer_classes=[UserRender]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializers(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UserPasswordChange(APIView):
    renderer_classes=[UserRender]
    permission_classes = [IsAuthenticated]   

    def post(self,request,format=None):
        serializer =UserChangePasswordSerializers(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'change password Sucess'},status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        
class SendPasswordEmail(APIView):
    renderer_classes=[UserRender]
    def post(self,request,format=None):
        serializer=SendPasswordEmailSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password reset change Sucess'},status=status.HTTP_200_OK)



class UserPasswordResetView(APIView):
    renderer_classes=[UserRender]
    def post(self,request,token,uid,format=None):
        serializer=UserPasswordResetViewSerializers(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password reset change Sucess'},status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class AddBook(APIView):
    renderer_classes=[UserRender]
    def post(self,request,format=None):
        serializer=UserAddBookViewSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg':'book added Sucess'},status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        
       
    
class EditBook(APIView):
    renderer_classes=[UserRender]
    def put(self,pk,request,format=None):
        snippet = self.get_object(pk)
        serializer = UserAddBookViewSerializers(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class DeleteBook(APIView):
    renderer_classes=[UserRender]
    def delete(self,request,format=None):
        serializer=UserDeleteBookViewSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            snippet = self.get_object(pk)
            snippet.delete()
            
            return Response({'msg':'book entry deleted'},status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class GetAllBooks(APIView):
    renderer_classes=[UserRender]
    def get(self,request,format=None):
        serializer=UserAddBookViewSerializers(request.data)
        # return Response(get_entries.data,status=status.HTTP_200_OK)
        return Response(serializer.data,status=status.HTTP_200_OK)