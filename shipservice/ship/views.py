from django.shortcuts import render
from rest_framework.response import Response
# Create your views here.
from rest_framework import status
from .models import *
from django.db import transaction
from rest_framework.decorators import api_view
import requests
from .serializers import *

STATUS_PENDING = 'pending'
STATUS_REJECT = 'reject'
STATUS_RECEIVER = 'receiver'

@api_view(['POST'])
def shiperReceiver(request):
    try:
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
                if user['isStaff'] == False :
                    raise Exception('not ship')
            else:
                raise Exception("Error auth")
            
            ship = {
                "shiperId": user["id"],
                "orderId": data["orderId"],
                "address": data["address"],
                "phone": data["phone"],
                "des": data["des"],
                "status": STATUS_PENDING
            }

            serializer_ship = ShipSerializer(data=ship)  # Bỏ many=True
            if serializer_ship.is_valid():
                serializer_ship.save()
            else:
                raise Exception(f"Serialization error: {serializer_ship.errors}")

            ship_detail = ShipDetail(
                ship_id = serializer_ship.data.get('id'),
                address = data["address"],
            )

            ship_detail.save()
            return Response({'success': 'success'}, status=status.HTTP_200_OK)

    except Exception as e:
        transaction.rollback()
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def updateShip(request):
    try:
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
                if user['isStaff'] == False :
                    raise Exception('not ship')
            else:
                raise Exception("Error auth")
            
            ship = Ship.objects.filter(id= data["id"], shiperId = user["id"]).first()
            if ship is None:
                raise Exception('ship not belong to me')
            
            ship.status = data["status"]
            ship.save()

            ship_detail = ShipDetail(
                ship_id = ship.id,
                address = data["address"],
            )

            ship_detail.save()
            return Response({'success': 'success'}, status=status.HTTP_200_OK)

    except Exception as e:
        transaction.rollback()
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def infoShip(request):
    try:
        orderId = None
        if 'orderId' in request.GET :
            orderId=request.GET.get('orderId')
        ship = Ship.objects.filter(orderId = orderId).all()
        serializer = ShipSerializer(ship, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e :
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

