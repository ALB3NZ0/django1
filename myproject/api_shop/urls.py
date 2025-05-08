from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SportCategoryViewSet, ProductTypeViewSet, BrandViewSet, SportProductViewSet,
    CartViewSet, CartItemViewSet, FavoriteViewSet, WarehouseViewSet,
    StockMovementViewSet, EquipmentFeatureViewSet, OrderViewSet, OrderItemViewSet
)

router = DefaultRouter()
router.register(r'sportcategory', SportCategoryViewSet)
router.register(r'producttype', ProductTypeViewSet)
router.register(r'brand', BrandViewSet)
router.register(r'sportproduct', SportProductViewSet)
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cartitem', CartItemViewSet, basename='cartitem')
router.register(r'favorite', FavoriteViewSet, basename='favorite')
router.register(r'warehouse', WarehouseViewSet)
router.register(r'stockmovement', StockMovementViewSet)
router.register(r'equipmentfeature', EquipmentFeatureViewSet)
router.register(r'order', OrderViewSet, basename='order')
router.register(r'orderitem', OrderItemViewSet, basename='orderitem')

urlpatterns = []
urlpatterns += router.urls