from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SportCategory, ProductType, SportProduct, Cart, CartItem, Favorite, Brand, Warehouse, StockMovement, EquipmentFeature
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem
from .forms import OrderForm

def index(request):
    sport_products = SportProduct.objects.filter(is_available=True)[:3]
    categories = SportCategory.objects.all()
    brands = Brand.objects.all()
    return render(request, 'hello/index.html', {
        'sport_products': sport_products,
        'categories': categories,
        'brands': brands
    })

def second(request):
    return render(request, 'hello/second.html')

def product_list(request):
    products = SportProduct.objects.filter(is_available=True)
    categories = SportCategory.objects.all()
    brands = Brand.objects.all()
    # Фильтрация
    brand_id = request.GET.get('brand')
    category_id = request.GET.get('category')
    if brand_id:
        products = products.filter(brand_id=brand_id)
    if category_id:
        products = products.filter(category_id=category_id)
    return render(request, 'hello/product_list.html', {
        'products': products,
        'categories': categories,
        'brands': brands
    })

def product_detail(request, product_id):
    product = get_object_or_404(SportProduct, id=product_id)
    features = product.features.all()
    stock_movements = StockMovement.objects.filter(product=product).order_by('-movement_date')[:5]
    return render(request, 'hello/product_detail.html', {
        'product': product,
        'features': features,
        'stock_movements': stock_movements
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(SportProduct, id=product_id)
    if not product.is_available or product.stock < 1:
        return redirect('product_list')
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
    return redirect('cart_view')

@login_required
def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    return render(request, 'hello/cart.html', {'cart': cart})

@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(SportProduct, id=product_id)
    Favorite.objects.get_or_create(user=request.user, product=product)
    return redirect('product_list')

@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'hello/favorites.html', {'favorites': favorites})

# --- Дополнения для полного CRUD ---

from .forms import (
    SportCategoryForm, ProductTypeForm, BrandForm, SportProductForm, CartForm,
    CartItemForm, FavoriteForm, WarehouseForm, StockMovementForm, EquipmentFeatureForm
)

# SportProduct (Создание, обновление, удаление)
@login_required
def product_create(request):
    if request.method == 'POST':
        form = SportProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = SportProductForm()
    return render(request, 'clothes/product_form.html', {'form': form})

@login_required
def product_update(request, product_id):
    product = get_object_or_404(SportProduct, id=product_id)
    if request.method == 'POST':
        form = SportProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = SportProductForm(instance=product)
    return render(request, 'clothes/product_form.html', {'form': form})

@login_required
def product_delete(request, product_id):
    product = get_object_or_404(SportProduct, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'clothes/product_confirm_delete.html', {'object': product})

# CartItem (Обновление, удаление)
@login_required
def cart_item_update(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        form = CartItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('cart_view')
    else:
        form = CartItemForm(instance=item)
    return render(request, 'clothes/cart_item_form.html', {'form': form})

@login_required
def cart_item_delete(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('cart_view')
    return render(request, 'clothes/cart_item_confirm_delete.html', {'object': item})

# Favorite (Удаление)
@login_required
def favorite_delete(request, favorite_id):
    favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
    if request.method == 'POST':
        favorite.delete()
        return redirect('favorites_view')
    return render(request, 'clothes/favorite_confirm_delete.html', {'object': favorite})

# Warehouse (Список, создание, обновление, удаление)
@login_required
def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'clothes/warehouse_list.html', {'warehouses': warehouses})

@login_required
def warehouse_create(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('warehouse_list')
    else:
        form = WarehouseForm()
    return render(request, 'clothes/warehouse_form.html', {'form': form})

@login_required
def warehouse_update(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            form.save()
            return redirect('warehouse_list')
    else:
        form = WarehouseForm(instance=warehouse)
    return render(request, 'clothes/warehouse_form.html', {'form': form})

@login_required
def warehouse_delete(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)
    if request.method == 'POST':
        warehouse.delete()
        return redirect('warehouse_list')
    return render(request, 'clothes/warehouse_confirm_delete.html', {'object': warehouse})

# StockMovement (Список, создание, удаление)
@login_required
def stock_movement_list(request):
    stock_movements = StockMovement.objects.all()
    return render(request, 'clothes/stock_movement_list.html', {'stock_movements': stock_movements})

@login_required
def stock_movement_create(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock_movement_list')
    else:
        form = StockMovementForm()
    return render(request, 'clothes/stock_movement_form.html', {'form': form})

@login_required
def stock_movement_delete(request, movement_id):
    movement = get_object_or_404(StockMovement, id=movement_id)
    if request.method == 'POST':
        movement.delete()
        return redirect('stock_movement_list')
    return render(request, 'clothes/stock_movement_confirm_delete.html', {'object': movement})

# EquipmentFeature (Список, создание, обновление, удаление)
@login_required
def equipment_feature_list(request):
    equipment_features = EquipmentFeature.objects.all()
    return render(request, 'clothes/equipment_feature_list.html', {'equipment_features': equipment_features})

@login_required
def equipment_feature_create(request):
    if request.method == 'POST':
        form = EquipmentFeatureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipment_feature_list')
    else:
        form = EquipmentFeatureForm()
    return render(request, 'clothes/equipment_feature_form.html', {'form': form})

@login_required
def equipment_feature_update(request, feature_id):
    feature = get_object_or_404(EquipmentFeature, id=feature_id)
    if request.method == 'POST':
        form = EquipmentFeatureForm(request.POST, instance=feature)
        if form.is_valid():
            form.save()
            return redirect('equipment_feature_list')
    else:
        form = EquipmentFeatureForm(instance=feature)
    return render(request, 'clothes/equipment_feature_form.html', {'form': form})

@login_required
def equipment_feature_delete(request, feature_id):
    feature = get_object_or_404(EquipmentFeature, id=feature_id)
    if request.method == 'POST':
        feature.delete()
        return redirect('equipment_feature_list')
    return render(request, 'clothes/equipment_feature_confirm_delete.html', {'object': feature})

# SportCategory (Список, создание, обновление, удаление)
@login_required
def category_list(request):
    categories = SportCategory.objects.all()
    return render(request, 'clothes/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = SportCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = SportCategoryForm()
    return render(request, 'clothes/category_form.html', {'form': form})

@login_required
def category_update(request, category_id):
    category = get_object_or_404(SportCategory, id=category_id)
    if request.method == 'POST':
        form = SportCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = SportCategoryForm(instance=category)
    return render(request, 'clothes/category_form.html', {'form': form})

@login_required
def category_delete(request, category_id):
    category = get_object_or_404(SportCategory, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'clothes/category_confirm_delete.html', {'object': category})

# ProductType (Список, создание, обновление, удаление)
@login_required
def product_type_list(request):
    product_types = ProductType.objects.all()
    return render(request, 'clothes/product_type_list.html', {'product_types': product_types})

@login_required
def product_type_create(request):
    if request.method == 'POST':
        form = ProductTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_type_list')
    else:
        form = ProductTypeForm()
    return render(request, 'clothes/product_type_form.html', {'form': form})

@login_required
def product_type_update(request, type_id):
    product_type = get_object_or_404(ProductType, id=type_id)
    if request.method == 'POST':
        form = ProductTypeForm(request.POST, instance=product_type)
        if form.is_valid():
            form.save()
            return redirect('product_type_list')
    else:
        form = ProductTypeForm(instance=product_type)
    return render(request, 'clothes/product_type_form.html', {'form': form})

@login_required
def product_type_delete(request, type_id):
    product_type = get_object_or_404(ProductType, id=type_id)
    if request.method == 'POST':
        product_type.delete()
        return redirect('product_type_list')
    return render(request, 'clothes/product_type_confirm_delete.html', {'object': product_type})

# Brand (Список, создание, обновление, удаление)
@login_required
def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'clothes/brand_list.html', {'brands': brands})

@login_required
def brand_create(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('brand_list')
    else:
        form = BrandForm()
    return render(request, 'clothes/brand_form.html', {'form': form})

@login_required
def brand_update(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            return redirect('brand_list')
    else:
        form = BrandForm(instance=brand)
    return render(request, 'clothes/brand_form.html', {'form': form})

@login_required
def brand_delete(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    if request.method == 'POST':
        brand.delete()
        return redirect('brand_list')
    return render(request, 'clothes/brand_confirm_delete.html', {'object': brand})



from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm

# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# Вход пользователя
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли!')
            return redirect('product_list')
        else:
            messages.error(request, 'Неверный email, имя пользователя или пароль.')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})

# Выход пользователя
def user_logout(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта.')
    return redirect('login')



from django.core.mail import send_mail

@login_required
def create_order(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        messages.error(request, 'Ваша корзина пуста.')
        return redirect('cart_view')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                total_price=sum(item.product.price * item.quantity for item in cart.items.all()),
                status='pending'
            )
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            cart.items.all().delete()

            # Отправка email клиенту
            subject = f'Заказ #{order.id} успешно оформлен'
            message = f'''
            Здравствуйте, {request.user.first_name}!

            Ваш заказ #{order.id} успешно оформлен.
            Общая стоимость: {order.total_price} руб.
            Адрес доставки: {order.address}
            Телефон: {order.phone}

            Состав заказа:
            '''
            for item in order.items.all():
                message += f'- {item.product.name} ({item.quantity} шт.) - {item.price * item.quantity} руб.\n'
            message += '\nСпасибо за покупку!'
            send_mail(
                subject,
                message,
                'shoesstore0507@gmail.com',
                [order.email],
                fail_silently=False,
            )

            # Отправка email администратору
            admin_subject = f'Новый заказ #{order.id}'
            admin_message = f'''
            Новый заказ #{order.id} от {request.user.username}.
            Email: {order.email}
            Телефон: {order.phone}
            Адрес: {order.address}
            Общая стоимость: {order.total_price} руб.

            Состав заказа:
            '''
            for item in order.items.all():
                admin_message += f'- {item.product.name} ({item.quantity} шт.) - {item.price * item.quantity} руб.\n'
            send_mail(
                admin_subject,
                admin_message,
                'shoesstore0507@gmail.com',
                ['shoesstore0507@gmail.com'],
                fail_silently=False,
            )

            messages.success(request, 'Заказ успешно оформлен!')
            return redirect('order_success')
    else:
        form = OrderForm(initial={'email': request.user.email})
    return render(request, 'orders/create_order.html', {'form': form, 'cart': cart})


def order_success(request):
    return render(request, 'orders/order_success.html')



from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import CartItem
import json

@login_required
@require_POST
def update_cart_item(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id, cart__user=request.user)
        data = json.loads(request.body)
        quantity = data.get('quantity', 1)
        if quantity < 1:
            return JsonResponse({'success': False, 'error': 'Количество не может быть меньше 1'}, status=400)
        if quantity > item.product.stock:
            return JsonResponse({'success': False, 'error': f'Доступно только {item.product.stock} шт.'}, status=400)
        item.quantity = quantity
        item.save()
        return JsonResponse({'success': True})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Товар не найден'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    


@require_POST
def favorite_delete(request, favorite_id):
    try:
        favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
        favorite.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_POST
def cart_item_delete(request, item_id):
    try:
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})