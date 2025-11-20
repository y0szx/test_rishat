from rest_framework import routers
from django.urls import include, path

from . import views

router = routers.DefaultRouter()
router.register(r'items', views.ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('item/<id>/', views.item_detail),
    path('order/<id>/', views.order_detail),
    path('buy/<id>/', views.buy_item),
    path('buy_order/<id>/', views.buy_order),
    path('success/', views.success),
]
