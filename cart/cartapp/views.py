from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from django.db import transaction


@api_view(['POST']) 
@permission_classes([AllowAny]) 
def addToCart(request):
    try :
        with transaction.atomic():
            dataRequest = request.data
            if 'Authorization' in request.headers:
                authorization_header = request.headers['Authorization']
            else :
                raise Exception("not auth")
            api_url = "http://127.0.0.1:8000/profile/"

            # Tạo tiêu đề Authorization
            headers = {
                'Authorization': authorization_header
            }
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                user = response.json()
            else:
                raise Exception("Error auth")
            cart = Cart.objects.filter(userId=user["id"]).first()
            if cart is None :
                cart = Cart(
                        userId=user["id"]
                    )
                cart.save()

            obj, created = CartItem.objects.update_or_create(
                cart_id = cart.id,
                product_id = dataRequest["product_id"],
                defaults={
                    'quantity' : dataRequest['quantity'],
                }
            )
            if int(obj.quantity) <= 0 :
                obj.delete()

            return Response({'success': "success"}, status=status.HTTP_200_OK)

    except Exception as e :
        transaction.rollback()
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET']) 
def getCart(request):
    try :
        if 'Authorization' in request.headers:
            authorization_header = request.headers['Authorization']
        else :
            raise Exception("not auth")
        api_url = "http://127.0.0.1:8000/profile/"

        # Tạo tiêu đề Authorization
        headers = {
            'Authorization': authorization_header
        }
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            user = response.json()
        else:
            raise Exception("Error auth")
        cart = Cart.objects.filter(userId=user["id"]).first()
        if cart is None :
            cart = Cart(
                    userId=user["id"]
                )
            cart.save()

        serializer = CartSerializer(cart)
        items = list()

        for item in serializer.data.get('items'):
            response = requests.get(f'http://127.0.0.1:5000/book/get_detail_product/{item.get('product_id')}/')
            if response.status_code == 201:
                result = dict({'quantity' : item.get('quantity'), 'product' : response.json()})
                items.append(result)
            else:
                continue

        res = dict()
        res["userId"] = serializer.data.get('userId')
        res["id"] = serializer.data.get("id")
        res["item"] = items
        return Response(res, status=status.HTTP_200_OK)

    except Exception as e :
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET']) 
def deleteCart(request):
    try :
        if 'Authorization' in request.headers:
            authorization_header = request.headers['Authorization']
        else :
            raise Exception("not auth")
        api_url = "http://127.0.0.1:8000/profile/"

        # Tạo tiêu đề Authorization
        headers = {
            'Authorization': authorization_header
        }
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            user = response.json()
        else:
            raise Exception("Error auth")
        cart = Cart.objects.filter(userId=user["id"]).first()
        if cart is not None:
            CartItem.objects.filter(cart_id = cart.id).delete()
        return Response({'success':'success'}, status=status.HTTP_200_OK )

    except Exception as e :
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)