from django.shortcuts import render
from rest_framework import generics

from .models import Customer
from .pagination import StandardResultsSetPagination
from .serializers import CustomerSerializer


# Create your views here.
class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all().order_by('name')
    serializer_class = CustomerSerializer
    pagination_class = StandardResultsSetPagination

