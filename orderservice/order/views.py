from rest_framework.decorators import api_view
from django.db import transaction
import requests
from .models import *
from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def checkout(request):
    try :
        with transaction.atomic():
            data = request.data
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
            
            order = Order(
                userId= user["id"],
                customer_name= user["name"],
                address= data["address"],
                phone_number= data["phone_number"]
            )
            order.save()

            response = requests.get("http://127.0.0.1:3001/cart/getCart/", headers=headers)
            if response.status_code == 200:
                cart = response.json()
            else:
                raise Exception("Error cart")
            cartItem = list()
            for i in  cart["item"]:
                item_data = {
                    "order_id": order.id,
                    "order" : order.id,
                    "product_id": i["product"]["product"],
                    "quantity": i["quantity"],
                    "price": i["product"]["price"],
                    "product_name": i["product"]["name"],
                    "images": i["product"]["productDetail"]["images"]
                }
                
                cartItem.append(item_data)
            
            orderSeri = OrderItemSerializer(data=cartItem, many= True )
            if orderSeri.is_valid():
                response = requests.post("http://127.0.0.1:5000/book/check_number_product/", json= orderSeri.data)
                if response.status_code == 201:
                    cart = response.json()
                else:
                    error_message = response.json().get('detail')
                    raise Exception(f"Error check number: {error_message}")
                
                response = requests.post("http://127.0.0.1:5000/book/update_number_product/", json= orderSeri.data)
                if response.status_code == 201:
                    cart = response.json()
                else:
                    error_message = response.json().get('detail')
                    raise Exception(f"Error ship save: {error_message}")
                
                response = requests.get("http://127.0.0.1:3001/cart/deleteCart/", headers=headers)
                if response.status_code == 200:
                    cart = response.json()
                else:
                    error_message = response.json().get('detail')
                    raise Exception(f"Error delete cart: {error_message}")
                orderSeri.save()
                return Response({'success':'success'}, status=status.HTTP_201_CREATED)
            else:
                raise Exception(f"Serialization error: {orderSeri.errors}")
    except Exception as e:
        transaction.rollback()
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
        

@api_view(['GET'])
def getListOrder(request):
    try:
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
        
        order = Order.objects.filter(userId=user["id"]).all()
        serializer = OrderSerializer(order, many= True )
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e :
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getListAllOrder(request):
    try:
        order = Order.objects.all()
        serializer = OrderSerializer(order, many= True )
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e :
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def updateStatusPaid(request):
    try:
        data = request.data
        order = Order.objects.filter(id=data["id"]).first()
        if order is None:
            raise Exception("error")
        order.status_pay = 1
        order.save()
        return Response({'success': 'success'}, status=status.HTTP_200_OK)

    except Exception as e :
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)