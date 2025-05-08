from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from firstproject.views import (
    index, second, product_list, product_detail, add_to_cart, cart_view,
    add_to_favorites, favorites_view, product_create, product_update, product_delete,
    cart_item_update, cart_item_delete, favorite_delete, warehouse_list, warehouse_create,
    warehouse_update, warehouse_delete, stock_movement_list, stock_movement_create,
    stock_movement_delete, equipment_feature_list, equipment_feature_create,
    equipment_feature_update, equipment_feature_delete, category_list, category_create,
    category_update, category_delete, product_type_list, product_type_create,
    product_type_update, product_type_delete, brand_list, brand_create, brand_update,
    brand_delete, create_order, order_success, update_cart_item, register, user_login,
    user_logout
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Главная страница — перенаправление на страницу входа
    path('', lambda request: redirect('login'), name='root'),

    # Страница регистрации и входа
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # Оставшиеся страницы
    path('index/', index, name='index'),
    path('second.html', second, name='second'),

    # Защищённые страницы: каталог, корзина, избранное
    path('products/', login_required(product_list), name='product_list'),
    path('product/<int:product_id>/', login_required(product_detail), name='product_detail'),
    path('cart/', login_required(cart_view), name='cart_view'),
    path('cart/add/<int:product_id>/', login_required(add_to_cart), name='add_to_cart'),
    path('cart/update/<int:item_id>/', login_required(cart_item_update), name='cart_item_update'),
    path('cart/delete/<int:item_id>/', login_required(cart_item_delete), name='cart_item_delete'),
    path('favorites/', login_required(favorites_view), name='favorites_view'),
    path('favorites/add/<int:product_id>/', login_required(add_to_favorites), name='add_to_favorites'),
    path('favorites/delete/<int:favorite_id>/', login_required(favorite_delete), name='favorite_delete'),

    # Страницы для управления товарами
    path('products/create/', login_required(product_create), name='product_create'),
    path('products/<int:product_id>/update/', login_required(product_update), name='product_update'),
    path('products/<int:product_id>/delete/', login_required(product_delete), name='product_delete'),

    # Прочие страницы без изменений
    path('warehouses/', login_required(warehouse_list), name='warehouse_list'),
    path('warehouses/create/', login_required(warehouse_create), name='warehouse_create'),
    path('warehouses/<int:warehouse_id>/update/', login_required(warehouse_update), name='warehouse_update'),
    path('warehouses/<int:warehouse_id>/delete/', login_required(warehouse_delete), name='warehouse_delete'),

    path('stock-movements/', login_required(stock_movement_list), name='stock_movement_list'),
    path('stock-movements/create/', login_required(stock_movement_create), name='stock_movement_create'),
    path('stock-movements/<int:movement_id>/delete/', login_required(stock_movement_delete), name='stock_movement_delete'),

    path('equipment-features/', login_required(equipment_feature_list), name='equipment_feature_list'),
    path('equipment-features/create/', login_required(equipment_feature_create), name='equipment_feature_create'),
    path('equipment-features/<int:feature_id>/update/', login_required(equipment_feature_update), name='equipment_feature_update'),
    path('equipment-features/<int:feature_id>/delete/', login_required(equipment_feature_delete), name='equipment_feature_delete'),

    path('categories/', login_required(category_list), name='category_list'),
    path('categories/create/', login_required(category_create), name='category_create'),
    path('categories/<int:category_id>/update/', login_required(category_update), name='category_update'),
    path('categories/<int:category_id>/delete/', login_required(category_delete), name='category_delete'),

    path('product-types/', login_required(product_type_list), name='product_type_list'),
    path('product-types/create/', login_required(product_type_create), name='product_type_create'),
    path('product-types/<int:type_id>/update/', login_required(product_type_update), name='product_type_update'),
    path('product-types/<int:type_id>/delete/', login_required(product_type_delete), name='product_type_delete'),

    path('brands/', login_required(brand_list), name='brand_list'),
    path('brands/create/', login_required(brand_create), name='brand_create'),
    path('brands/<int:brand_id>/update/', login_required(brand_update), name='brand_update'),
    path('brands/<int:brand_id>/delete/', login_required(brand_delete), name='brand_delete'),

    # Создание и успешное завершение заказа
    path('order/create/', login_required(create_order), name='create_order'),
    path('order/success/', login_required(order_success), name='order_success'),

    # API
    path('api/', include('api_shop.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
