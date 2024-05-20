from django.shortcuts import render
from rest_framework.response import Response
# Create your views here.
from rest_framework import status
from .models import *
from .serializers import *
from mobile.serializers import *
from clothes.serializers import *
from rest_framework.decorators import api_view
from clothes.models import *
from mobile.models import *
from django.db import transaction


@api_view(['GET'])
def getListBook(request):
    try:
        searchText = ""
        if 'search' in request.GET :
            searchText=request.GET.get('search')
        data= Book.objects.filter(name__icontains = searchText).all()
        serializer = BookSerializer(data,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e :
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def addBook(request):
    try:
        with transaction.atomic():
            dataRequest = request.data
            productData = {
                "type": "book",
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
            serializer = BookSerializer(data=dataRequest)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else :
                raise Exception("validate fail")
    except Exception as e :
        transaction.rollback()
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def updateNumber(request):
    try:
        dataRequest = request.data
        for i in  dataRequest :
            product = Product.objects.filter(id=i["product_id"]).first()
            product.quantity -= i["quantity"]
            product.save()
        return Response(dataRequest, status=status.HTTP_201_CREATED)
    except Exception as e :
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def checkNumber(request):
    try:
        dataRequest = request.data
        for i in dataRequest :
            product = Product.objects.filter(id=i["product_id"], quantity__gte=i["quantity"]).first()
            if product is None :
                raise Exception(str(i["product_id"]) + " ko du so luong")
        return Response({'success':'success'},status=status.HTTP_201_CREATED)
    except Exception as e :
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getDetailProduct(request, id=None):
    try:
        product = Product.objects.filter(id=id).first()
        serializer = None
        if product.type == "book":
            info = Book.objects.filter(product_id = product.id).all()
            serializer = BookSerializer(info, many= True)
        elif product.type == "clothes":
            info = Clothes.objects.filter(product_id = product.id).all()
            serializer = ClothesSerializer(info, many= True)
        elif product.type == "mobile":
            info = Mobile.objects.filter(product_id = product.id).all()
            serializer = MobileSerializer(info, many= True)
        return Response(serializer.data[0], status=status.HTTP_201_CREATED)
    except Exception as e :
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
