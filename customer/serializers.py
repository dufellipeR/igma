from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    born = serializers.DateField(format='%d/%m/%Y')

    class Meta:
        model = Customer
        fields = "__all__"
