from django.shortcuts import render
from .models import Travel
from .serializers import TravelSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(["GET", "POST"])
def index(request):
    if request.method == "GET":
        a = Travel.objects.all()
        b = TravelSerializer(a, many=True)
        return Response(b.data, status=status.HTTP_200_OK)
    if request.method == "POST":
        b = TravelSerializer(data=request.data)
        if b.is_valid():
            b.save()
            return Response(b.data, status=status.HTTP_201_CREATED)
        return Response(b.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(["GET", "PUT", "DELETE"])
def update(request, msd):
    try:
        a = Travel.objects.get(id=msd)
    except Travel.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        b = TravelSerializer(a)
        return Response(b.data, status=status.HTTP_200_OK)
    if request.method == "PUT":
        z = TravelSerializer(instance=a, data=request.data)
        if z.is_valid():
            z.save()
            return Response(z.data, status=status.HTTP_202_ACCEPTED)
        return Response(z.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        a.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
