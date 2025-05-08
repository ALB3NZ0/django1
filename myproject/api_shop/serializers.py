from rest_framework import serializers
from firstproject.models import (
    SportCategory, ProductType, Brand, SportProduct, Cart, CartItem, Favorite,
    Warehouse, StockMovement, EquipmentFeature, Order, OrderItem
)

class SportCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SportCategory
        fields = ['id', 'name', 'description']

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name', 'description']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'description']

class EquipmentFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentFeature
        fields = ['id', 'feature_name', 'feature_value']

class SportProductSerializer(serializers.ModelSerializer):
    category = SportCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=SportCategory.objects.all(), source='category', write_only=True
    )
    product_types = ProductTypeSerializer(many=True, read_only=True)
    product_type_ids = serializers.PrimaryKeyRelatedField(
        queryset=ProductType.objects.all(), source='product_types', many=True, write_only=True
    )
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), source='brand', write_only=True, allow_null=True
    )
    features = EquipmentFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = SportProduct
        fields = [
            'id', 'name', 'description', 'price', 'size', 'material', 'stock',
            'photo', 'create_date', 'is_available', 'category', 'category_id',
            'product_types', 'product_type_ids', 'brand', 'brand_id', 'features'
        ]

class CartItemSerializer(serializers.ModelSerializer):
    product = SportProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=SportProduct.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']

class FavoriteSerializer(serializers.ModelSerializer):
    product = SportProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=SportProduct.objects.all(), source='product', write_only=True
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product', 'product_id', 'added_at']

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'address', 'capacity']

class StockMovementSerializer(serializers.ModelSerializer):
    product = SportProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=SportProduct.objects.all(), source='product', write_only=True
    )
    warehouse = WarehouseSerializer(read_only=True)
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(), source='warehouse', write_only=True
    )
    destination_warehouse = WarehouseSerializer(read_only=True)
    destination_warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(), source='destination_warehouse', write_only=True, allow_null=True
    )

    class Meta:
        model = StockMovement
        fields = [
            'id', 'product', 'product_id', 'warehouse', 'warehouse_id',
            'movement_type', 'quantity', 'movement_date', 'destination_warehouse',
            'destination_warehouse_id'
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    product = SportProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=SportProduct.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'email', 'phone', 'address', 'created_at',
            'total_price', 'status', 'items'
        ]