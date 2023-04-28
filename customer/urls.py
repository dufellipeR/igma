from django.urls import path

from .views import CustomerList, CustomerDetail

urlpatterns = [
    path('list/', CustomerList.as_view()),
    path('detail/<int:pk>/', CustomerDetail.as_view(), name='customer-detail-by-id'),
    path('detail/', CustomerDetail.as_view(), name='customer-detail-by-cpf'),
]
