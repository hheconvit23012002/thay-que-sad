from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
import requests
@api_view(['GET'])
def search(request):
    try:
        searchText = ""
        if 'search' in request.GET :
            searchText=request.GET.get('search')
        api_book = "http://127.0.0.1:5000/book/getListBook?search="+searchText
        api_clothes = "http://127.0.0.1:5000/clothes/getListClothes?search="+searchText
        api_mobile = "http://127.0.0.1:5000/mobile/getListMobile?search="+searchText

        item = dict()
        response = requests.get(api_book)
        if response.status_code == 200:
            item["book"] = response.json()
        else:
            raise Exception("Error book")
        

        response = requests.get(api_clothes)
        if response.status_code == 200:
            item["clothes"] = response.json()
        else:
            raise Exception("Error clothes")
        
        response = requests.get(api_mobile)
        if response.status_code == 200:
            item["mobile"] = response.json()
        else:
            raise Exception("Error mobile")

        return Response(item, status=status.HTTP_200_OK)
    except Exception as e :
        message = {'detail': f'Error: {str(e)}'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)



