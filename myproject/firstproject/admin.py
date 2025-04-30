from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Collection, Clothes, SportCategory, ProductType, SportProduct, Cart, CartItem, Favorite, Brand, Warehouse, StockMovement, EquipmentFeature

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Clothes)
class ClothesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_exists', 'create_date')
    search_fields = ('name', 'description')
    list_filter = ('category', 'is_exists', 'create_date')
    list_per_page = 20

# Инлайн для типов товаров в SportProduct (ManyToManyField)
class ProductTypeInline(admin.TabularInline):
    model = SportProduct.product_types.through
    extra = 1
    verbose_name = 'Тип товара'
    verbose_name_plural = 'Типы товаров'

# Инлайн для характеристик в SportProduct
class EquipmentFeatureInline(admin.TabularInline):
    model = EquipmentFeature
    extra = 1
    verbose_name = 'Характеристика'
    verbose_name_plural = 'Характеристики'

# Инлайн для движений стока в SportProduct
class StockMovementInline(admin.TabularInline):
    model = StockMovement
    extra = 1
    verbose_name = 'Движение стока'
    verbose_name_plural = 'Движения стоков'

# Инлайн для элементов корзины в Cart
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    verbose_name = 'Элемент корзины'
    verbose_name_plural = 'Элементы корзины'

# Админка для SportCategory
@admin.register(SportCategory)
class SportCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('name',)
    ordering = ('name',)

# Админка для ProductType
@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)

# Админка для Brand
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)

# Админка для SportProduct
@admin.register(SportProduct)
class SportProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'stock', 'is_available', 'create_date')
    search_fields = ('name', 'description', 'material')
    list_filter = ('category', 'brand', 'is_available', 'create_date')
    list_editable = ('price', 'stock', 'is_available')
    list_per_page = 20
    inlines = [ProductTypeInline, EquipmentFeatureInline, StockMovementInline]
    ordering = ('-create_date',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.photo.url)
        return "Нет фото"
    photo_preview.short_description = 'Фото'

# Админка для Cart
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)
    inlines = [CartItemInline]
    ordering = ('-created_at',)

# Админка для CartItem
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('product__name',)
    list_filter = ('cart__user',)

# Админка для Favorite
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('added_at',)
    ordering = ('-added_at',)

# Админка для Warehouse
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'capacity')
    search_fields = ('name', 'address')
    ordering = ('name',)

# Админка для StockMovement
@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'movement_type', 'quantity', 'movement_date', 'destination_warehouse')
    search_fields = ('product__name',)
    list_filter = ('movement_type', 'warehouse', 'movement_date')
    ordering = ('-movement_date',)

# Админка для EquipmentFeature
@admin.register(EquipmentFeature)
class EquipmentFeatureAdmin(admin.ModelAdmin):
    list_display = ('product', 'feature_name', 'feature_value')
    search_fields = ('feature_name', 'feature_value', 'product__name')
    list_filter = ('product',)