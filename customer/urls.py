from django.urls import path

from .views import CustomerList, CustomerDetail, CustomerCreate, CustomerDetailByCPF

urlpatterns = [
    path('list/', CustomerList.as_view()),
    path('detail/<int:pk>/', CustomerDetail.as_view(), name='customer-detail-by-id'),
    path('detail/', CustomerDetailByCPF.as_view(), name='customer-detail-by-cpf'),
    path('create/', CustomerCreate.as_view())
]
