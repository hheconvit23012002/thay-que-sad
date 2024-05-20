from django.shortcuts import render
from rest_framework.response import Response
# Create your views here.
from rest_framework import status
from .models import *
from .serializers import *
from book.serializers import *
from rest_framework.decorators import api_view
from django.db import transaction
# Create your views here.
@api_view(['GET'])
def getListClothes(request):
    try:
        searchText = ""
        if 'search' in request.GET :
            searchText=request.GET.get('search')
        data= Clothes.objects.filter(name__icontains = searchText).all()
        serializer = ClothesSerializer(data,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e :
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def addClothes(request):
    try:
        with transaction.atomic():
            dataRequest = request.data
            productData = {
                "type": "clothes",
                "images": dataRequest["images"],
                "quantity" : dataRequest["quantity"]
            }
            productSeri = ProductSerializer(data = productData)
            if productSeri.is_valid():
                product_instance = productSeri.save()
                product_id = product_instance.id
            else :
                raise Exception("loi tao product")
            dataRequest["product"] = product_id
            serializer = ClothesSerializer(data=dataRequest)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else :
                raise Exception("validate fail")
    except Exception as e :
        transaction.rollback()
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
