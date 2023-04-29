from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from .models import Customer
from .views import CustomerList, CustomerDetail, CustomerCreate, CustomerDetailByCPF
from .helpers import sanitize_cpf, validate_cpf, sum_digits, make_safe_digit


class CustomerListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        Customer.objects.get_or_create(name="Satoshi Nakamoto", born="2008-10-31", CPF="20802113079")
        Customer.objects.get_or_create(name="Hal Finey", born="1956-05-04", CPF="97088230070")
        Customer.objects.get_or_create(name="Adam Back", born="1970-07-30", CPF="61876157003")
        Customer.objects.get_or_create(name="Satoshi Nakamoto", born="2008-10-31", CPF="22349654036")
        Customer.objects.get_or_create(name="Satoshi Nakamoto", born="2008-10-31", CPF="47878593078")
        Customer.objects.get_or_create(name="Satoshi Nakamoto", born="2008-10-31", CPF="64570225020")

    def test_get_customers(self):
        view = CustomerList.as_view()
        request = self.factory.get(f'list', format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 6)
        self.assertNotEqual(response.data["next"], None)


class CustomerCreateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()

    def test_create_customer(self):
        view = CustomerCreate.as_view()

        payload = {"name": "Satoshi Nakamoto", "born": "2008-10-31", "CPF": "20802113079"}
        request = self.factory.post(f'create', payload, format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Customer.objects.filter(CPF=payload["CPF"]).exists())

    def test_create_customer_with_cpf_mask(self):
        view = CustomerCreate.as_view()

        payload = {"name": "Satoshi Nakamoto", "born": "2008-10-31", "CPF": "208.021.130-79"}
        request = self.factory.post(f'create', payload, format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Customer.objects.filter(name="Satoshi Nakamoto").exists())

    def test_create_customer_with_invalid_cpf(self):
        view = CustomerCreate.as_view()

        payload = {"name": "Satoshi Nakamoto", "born": "2008-10-31", "CPF": "20802113040"}
        request = self.factory.post(f'create', payload, format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertTrue(not (Customer.objects.filter(CPF=payload["CPF"]).exists()))

    def test_create_customer_with_invalid_cpf_with_mask(self):
        view = CustomerCreate.as_view()

        payload = {"name": "Satoshi Nakamoto", "born": "2008-10-31", "CPF": "208.021.130-40"}
        request = self.factory.post(f'create', payload, format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertTrue(not (Customer.objects.filter(CPF=payload["CPF"]).exists()))


class CustomerDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.customer = Customer.objects.get_or_create(name="Satoshi Nakamoto", born="2008-10-31", CPF="20802113079")
        Customer.objects.get_or_create(name="Hal Finey", born="1956-05-04", CPF="97088230070")
        Customer.objects.get_or_create(name="Adam Back", born="1970-07-30", CPF="61876157003")

    def test_retrieve_customer_by_pk(self):
        view = CustomerDetail.as_view()
        request = self.factory.get(f'detail/{self.customer[0].id}', format='json')
        response = view(request, pk=self.customer[0].id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.customer[0].id)
        self.assertEqual(response.data['name'], self.customer[0].name)
        self.assertEqual(response.data['CPF'], self.customer[0].CPF)


class CustomerDetailByCPFTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.customer = Customer.objects.get_or_create(name="Satoshi Nakamoto", born="2008-10-31", CPF="20802113079")
        Customer.objects.get_or_create(name="Hal Finey", born="1956-05-04", CPF="97088230070")
        Customer.objects.get_or_create(name="Adam Back", born="1970-07-30", CPF="61876157003")

    def test_retrieve_customer_by_cpf(self):
        view = CustomerDetailByCPF.as_view()

        payload = {"CPF": self.customer[0].CPF}
        request = self.factory.post(f'detail', payload, format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.customer[0].id)
        self.assertEqual(response.data['name'], self.customer[0].name)
        self.assertEqual(response.data['CPF'], self.customer[0].CPF)

    def test_retrieve_customer_by_cpf_with_mask(self):
        view = CustomerDetailByCPF.as_view()

        payload = {"CPF": "208.021.130-79"}
        request = self.factory.post(f'detail', payload, format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.customer[0].id)
        self.assertEqual(response.data['name'], self.customer[0].name)
        self.assertEqual(response.data['CPF'], self.customer[0].CPF)


class HelpersTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cpf_to_sanitize = "111.444.777-35"
        cls.already_sanitized = "11144477735"
        cls.invalid_cpf = "11144477705"

    def test_sanitize_cpf(self):
        self.assertEqual(sanitize_cpf(self.cpf_to_sanitize), self.already_sanitized)

    def test_validate_cpf(self):
        self.assertTrue(validate_cpf(self.already_sanitized))
        self.assertTrue(not (validate_cpf(self.invalid_cpf)))
        self.assertTrue(not (validate_cpf(self.already_sanitized[:5])))

    def test_sum_digits(self):
        self.assertEqual(sum_digits(self.already_sanitized[:9]), 162)
        self.assertEqual(sum_digits(self.already_sanitized[:10]), 204)

    def test_make_safe_digit(self):
        self.assertEqual(make_safe_digit(162), '3')
        self.assertEqual(make_safe_digit(231), '0')
