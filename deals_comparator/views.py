from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Components
from .serializers import ComponentSerializer


class ComponentSearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        if query:
            products = Components.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query)
            )
            if not products:
                return Response({'Message': 'The component that you are searching is not found'}, status= 404)
        else:
            products = Components.objects.all()

        serializer = ComponentSerializer(products, many=True)
        return Response(serializer.data)