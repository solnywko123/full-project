from django.urls import path
from . import views
urlpatterns = [
    path('', views.OrderAPIView.as_view()),
    path('confirm/<int:pk>', views.OrderConfirmView.as_view()),
]