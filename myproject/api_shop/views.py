from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .permission import StandardResultsSetPagination, CustomPermissions
from firstproject.models import (
    SportCategory, ProductType, Brand, SportProduct, Cart, CartItem, Favorite,
    Warehouse, StockMovement, EquipmentFeature, Order, OrderItem
)
from .serializers import (
    SportCategorySerializer, ProductTypeSerializer, BrandSerializer, SportProductSerializer,
    CartSerializer, CartItemSerializer, FavoriteSerializer, WarehouseSerializer,
    StockMovementSerializer, EquipmentFeatureSerializer, OrderSerializer, OrderItemSerializer
)

class SportCategoryViewSet(viewsets.ModelViewSet):
    queryset = SportCategory.objects.all()
    serializer_class = SportCategorySerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

class SportProductViewSet(viewsets.ModelViewSet):
    queryset = SportProduct.objects.all()
    serializer_class = SportProductSerializer
    permission_classes = [AllowAny, CustomPermissions]
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user)
        return Cart.objects.none()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            raise serializer.ValidationError("User must be authenticated to create a cart.")

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return CartItem.objects.filter(cart__user=self.request.user)
        return CartItem.objects.none()

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [AllowAny]
    pagingation_class = StandardResultsSetPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Favorite.objects.filter(user=self.request.user)
        return Favorite.objects.none()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            raise serializer.ValidationError("User must be authenticated to add to favorites.")

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

class EquipmentFeatureViewSet(viewsets.ModelViewSet):
    queryset = EquipmentFeature.objects.all()
    serializer_class = EquipmentFeatureSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)
        return Order.objects.none()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            raise serializer.ValidationError("User must be authenticated to create an order.")

class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return OrderItem.objects.filter(order__user=self.request.user)
        return OrderItem.objects.none()