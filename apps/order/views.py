from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.order.models import Order
from apps.order.serializers import OrderSerializer


# Create your views here.

class OrderAPIView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        orders = user.orders.all()
        serializer = OrderSerializer(instance=orders, many=True)
        return Response(serializer.data, status=200)


class OrderConfirmView(APIView):
    def get(self, request, pk):
        order = Order.object.get(pk=pk) #достаем тот заказ который нужен pk=pk
        order.status = 'comleted'
        order.save()
        return Response({'message': 'Вы подтвердили заказ'}, status=200)
