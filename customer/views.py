from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .helpers import sanitize_cpf
from .models import Customer
from .pagination import StandardResultsSetPagination
from .serializers import CustomerSerializer


class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all().order_by('name')
    serializer_class = CustomerSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'born']


class CustomerDetail(APIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_object(self, pk=None, cpf=None):
        if pk is not None:
            return get_object_or_404(Customer, pk=pk)
        elif cpf is not None:
            return get_object_or_404(Customer, CPF=cpf)
        else:
            raise NotFound(detail='Either `pk` or `CPF` must be provided.')

    def get(self, request, pk=None, cpf=None):
        obj = self.get_object(pk=pk, cpf=cpf)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def post(self, request):
        cpf = request.data.get('CPF')

        sanitized_cpf = sanitize_cpf(cpf)

        obj = self.get_object(None, sanitized_cpf)
        if obj is not None:
            serializer = self.serializer_class(obj)
            return Response(serializer.data)
        else:
            return Response({'error': 'No customer found with the specified CPF.'}, status=status.HTTP_404_NOT_FOUND)
