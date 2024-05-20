from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import requests
from .models import *
from .serializers import *
# Create your views here.

@api_view(["POST"])
def comment(request):
    try:
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
        
        if int(data['rate']) < 0 or int(data['rate']) > 5:
            raise Exception('rate >=0 and <=5')
        
        cmt = Comment(
            userId = user["id"],
            rate = data["rate"],
            comment = data["comment"],
            productId = data["productId"]
        )
        cmt.save()
        return Response({'success':'success'}, status=status.HTTP_200_OK)

    except Exception as e:
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])

def getListComment(request):
    try:
        productId = request.GET.get('productId')
        if productId is None:
            raise Exception('not fount product')
        
        data = Comment.objects.filter(productId = productId).all()
        serializer = CommentSerializers(data, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)