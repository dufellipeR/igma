from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .helpers import sanitize_cpf, validate_cpf
from .models import Customer
from .pagination import StandardResultsSetPagination
from .serializers import CustomerSerializer


class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all().order_by('name')
    serializer_class = CustomerSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'born']


@extend_schema(
    examples=[
        OpenApiExample(
            "Example with mask",
            description='Example with mask',
            value={
                "born": "2023-04-29",
                "name": "igma",
                "CPF": "111.444.777-35"
            },
            request_only=True,

        ),
        OpenApiExample(
            "Example without mask",
            description='Example without mask',
            value={
                "born": "2023-04-29",
                "name": "igma",
                "CPF": "36467608933"
            },
            request_only=True,

        ),
        OpenApiExample(
            "Example invalid CPF",
            description='Example with invalid CPF',
            value={
                "born": "2023-04-29",
                "name": "igma",
                "CPF": "11144477705"
            },
            request_only=True,

        ),
    ],
)
class CustomerCreate(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):

        sanitized_cpf = sanitize_cpf(request.data.get('CPF'))
        if not validate_cpf(sanitized_cpf):
            return Response({'error': 'Not a valid CPF'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        request.data['CPF'] = sanitized_cpf

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(APIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_object(self, pk=None, cpf=None):
        if pk is not None:
            return get_object_or_404(Customer, pk=pk)
        else:
            raise NotFound(detail='`pk` must be provided.')

    def get(self, request, pk):
        obj = self.get_object(pk=pk)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)


@extend_schema(
    examples=[
        OpenApiExample(
            "Example with mask",
            description='Example with mask',
            value={
                "CPF": "111.444.777-35",
            },
            request_only=True,

        ),
        OpenApiExample(
            "Example without mask",
            description='Example without mask',
            value={
                "CPF": "11144477735",
            },
            request_only=True,

        ),
        OpenApiExample(
            "Example invalid CPF",
            description='Example with invalid CPF',
            value={
                "CPF": "11144477705",
            },
            request_only=True,

        ),
    ],
    description='POST method for sake of privacy on CPF field',

)
class CustomerDetailByCPF(APIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_object(self, cpf=None):
        if cpf is not None:
            return get_object_or_404(Customer, CPF=cpf)
        else:
            raise NotFound(detail='`CPF` must be provided.')

    def post(self, request):
        cpf = request.data.get('CPF')

        sanitized_cpf = sanitize_cpf(cpf)

        if validate_cpf(sanitized_cpf):
            obj = self.get_object(sanitized_cpf)
            if obj is not None:
                serializer = self.serializer_class(obj)
                return Response(serializer.data)
            else:
                return Response({'error': 'No customer found with the specified CPF.'},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Not a valid CPF'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
