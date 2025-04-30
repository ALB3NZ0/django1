from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SportCategory, ProductType, SportProduct, Cart, CartItem, Favorite, Brand, Warehouse, StockMovement, EquipmentFeature

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