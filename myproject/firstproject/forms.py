from django import forms
from .models import (
    SportCategory, ProductType, Brand, SportProduct, Cart, CartItem, Favorite,
    Warehouse, StockMovement, EquipmentFeature
)

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


# Форма для SportCategory
class SportCategoryForm(forms.ModelForm):
    class Meta:
        model = SportCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            raise forms.ValidationError("Название категории должно содержать минимум 2 символа.")
        return name


# Форма для ProductType
class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


# Форма для Brand
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


# Форма для SportProduct
class SportProductForm(forms.ModelForm):
    class Meta:
        model = SportProduct
        fields = [
            'name', 'description', 'price', 'size', 'material', 'stock',
            'photo', 'is_available', 'category', 'product_types', 'brand'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'material': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'product_types': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Цена должна быть больше 0.")
        return price

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock < 0:
            raise forms.ValidationError("Количество на складе не может быть отрицательным.")
        return stock


# Форма для Cart
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
        }


# Форма для CartItem
class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'quantity']
        widgets = {
            'cart': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        product = self.cleaned_data.get('product')
        if product and quantity > product.stock:
            raise forms.ValidationError(f"Нельзя заказать больше, чем {product.stock} единиц.")
        return quantity


# Форма для Favorite
class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['user', 'product']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
        }


# Форма для Warehouse
class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'address', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean_capacity(self):
        capacity = self.cleaned_data['capacity']
        if capacity <= 0:
            raise forms.ValidationError("Вместимость склада должна быть больше 0.")
        return capacity


# Форма для StockMovement
class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'warehouse', 'movement_type', 'quantity', 'destination_warehouse']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'warehouse': forms.Select(attrs={'class': 'form-control'}),
            'movement_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'destination_warehouse': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        movement_type = cleaned_data.get('movement_type')
        destination_warehouse = cleaned_data.get('destination_warehouse')
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')
        warehouse = cleaned_data.get('warehouse')

        if movement_type == 'transfer' and not destination_warehouse:
            raise forms.ValidationError("Для перемещения необходимо указать склад назначения.")
        if movement_type != 'transfer' and destination_warehouse:
            raise forms.ValidationError("Склад назначения указывается только для перемещений.")
        if quantity and product and warehouse:
            if movement_type in ['out', 'transfer'] and quantity > product.stock:
                raise forms.ValidationError(f"Недостаточно товара на складе: доступно {product.stock} единиц.")
        return cleaned_data


# Форма для EquipmentFeature
class EquipmentFeatureForm(forms.ModelForm):
    class Meta:
        model = EquipmentFeature
        fields = ['product', 'feature_name', 'feature_value']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'feature_name': forms.TextInput(attrs={'class': 'form-control'}),
            'feature_value': forms.TextInput(attrs={'class': 'form-control'}),
        }



from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Форма для регистрации пользователя
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}), label='Пароль')
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}), label='Подтверждение пароля')

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password', 'password_confirm']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'username': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')

        # Проверка совпадения паролей
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают.')
        
        # Проверка уникальности email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        
        # Проверка уникальности username
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует.')
        
        return cleaned_data

# Форма для входа пользователя
class UserLoginForm(forms.Form):
    login = forms.CharField(label="Email или имя пользователя", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('login')
        password = cleaned_data.get('password')

        if login and password:
            user = None
            # Проверяем, является ли введённое значение email
            try:
                user = User.objects.get(email=login)
            except ObjectDoesNotExist:
                # Если не email, пробуем найти по username
                try:
                    user = User.objects.get(username=login)
                except ObjectDoesNotExist:
                    raise forms.ValidationError("Пользователь с таким email или именем не найден.")

            # Проверяем пароль
            if not user.check_password(password):
                raise forms.ValidationError("Неверный пароль.")
            
            # Проверяем, активен ли аккаунт
            if not user.is_active:
                raise forms.ValidationError("Этот аккаунт неактивен.")
            
            cleaned_data['user'] = user
        return cleaned_data

    def get_user(self):
        return self.cleaned_data.get('user')

class OrderForm(forms.Form):
    email = forms.EmailField(label='Электронная почта')
    phone = forms.CharField(label='Телефон', max_length=20)
    address = forms.CharField(label='Адрес доставки', max_length=255, widget=forms.Textarea(attrs={'rows': 3}))