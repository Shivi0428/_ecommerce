import traceback
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.views import View
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CustomerRegistrationForm, CustomerProfileForm
from .models import Cart, Instance, Customer, Product, OrderPlaced
# Add selected instances to the cart and handle potential errors
@require_POST
@login_required
def add_to_cart(request):
    try:
        user = request.user
        selected_instances = request.POST.getlist('selected_instances')
        quantities = {key.split('_')[1]: int(value) for key, value in request.POST.items() if key.startswith('quantity_')}

        for instance_type in selected_instances:
            quantity = quantities.get(instance_type, 0)
            if quantity > 0:
                instance = Instance.objects.get(type=instance_type)
                item_already_in_cart = Cart.objects.filter(Q(product=instance) & Q(user=user)).exists()
                if not item_already_in_cart:
                    Cart(user=user, product=instance, quantity=quantity).save()
                else:
                    cart_item = Cart.objects.get(user=user, product=instance)
                    cart_item.quantity += quantity
                    cart_item.save()

        messages.success(request, "Selected instances added to cart successfully.")
        return redirect('app/add_to_cart.html')
    except Exception as e:
        traceback.print_exc()
        messages.error(request, "An error occurred while adding items to the cart.")
        return redirect('app/add_to_cart.html')



# Fetch product data from the database and render the comparison view
def instance_comparison_database_view(request):
    instances = Product.objects.all()
    return render(request, 'app/instance_comparison_database.html', {'instances': instances})
from django.shortcuts import render
from .models import Product  # Import your Product model

def instance_comparison_database_view(request):
    instances = Product.objects.all()
    return render(request, 'app/instance_comparison_database.html', {'instances': instances})

# Fetch product data from a predefined list and render the comparison view
class VirtualMachineComparisonView(View):
    def get(self, request):
        instance_data = [
            {"type": "M5.Large", "vcpus": 2, "memory": 8, "storage": "EBS Only", "network": "Up to 10 Gbps", "price": "$0.096/hour"},
            {"type": "C5.Large", "vcpus": 2, "memory": 4, "storage": "EBS Only", "network": "Up to 10 Gbps", "price": "$0.085/hour"},
            {"type": "R5.Large", "vcpus": 2, "memory": 16, "storage": "EBS Only", "network": "Up to 10 Gbps", "price": "$0.126/hour"},
            {"type": "P3.2xlarge", "vcpus": 8, "memory": 61, "storage": "EBS Only", "network": "Up to 10 Gbps", "price": "$3.060/hour"}
        ]
        return render(request, 'app/instance_comparison.html', {'instances': instance_data})

# Fetch product data from the database based on categories and render the home view
class ProductView(View):
    def get(self, request):
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()
        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles, 'totalitem': totalitem})

# Fetch product detail based on product ID and render the product detail view
class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart, 'totalitem': totalitem})

# Search for products based on a query and render the search results view
@login_required
def search_results(request):
    query = request.GET.get('q')
    results = Product.objects.filter(title__icontains=query) if query else Product.objects.none()
    return render(request, 'app/search_results.html', {'results': results})



# Display the cart with items and calculate the total amount including shipping
@login_required
def show_cart(request):
    totalitem = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        amount = sum(p.quantity * p.product.price for p in cart_product)
        totalamount = amount + shipping_amount
        return render(request, 'app/addtocart.html', {'carts': cart, 'amount': amount, 'totalamount': totalamount, 'totalitem': totalitem})
    else:
        return render(request, 'app/emptycart.html', {'totalitem': totalitem})

# Increment the quantity of an item in the cart and return updated cart data
@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = sum(p.quantity * p.product.price for p in Cart.objects.filter(user=request.user))
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + 70.0
        }
        return JsonResponse(data)
    return HttpResponse("")

# Decrement the quantity of an item in the cart and return updated cart data
@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = sum(p.quantity * p.product.price for p in Cart.objects.filter(user=request.user))
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + 70.0
        }
        return JsonResponse(data)
    return HttpResponse("")

# Proceed to checkout, calculate total cost, and render the checkout view
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = sum(p.quantity * p.product.discounted_price for p in cart_items)
    totalamount = amount + 70.0
    return render(request, 'app/checkout.html', {'add': add, 'cart_items': cart_items, 'totalcost': totalamount})

# Handle the payment completion process, save orders and clear the cart
@login_required
def payment_done(request):
    custid = request.GET.get('custid')
    user = request.user
    customer = Customer.objects.get(id=custid)
    cartid = Cart.objects.filter(user=user)
    for cid in cartid:
        OrderPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
        cid.delete()
    return redirect("orders")

# Remove an item from the cart and return updated cart data
@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = sum(p.quantity * p.product.discounted_price for p in Cart.objects.filter(user=request.user))
        data = {
            'amount': amount,
            'totalamount': amount + 70.0
        }
        return JsonResponse(data)
    return HttpResponse("")

# Display user addresses
@login_required
def address(request):
    totalitem = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary', 'totalitem': totalitem})

# Display user orders
@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})

# Filter and display mobile products based on brand and price range
def mobile(request, data=None):
    totalitem = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    if data is None:
        mobiles = Product.objects.filter(category='M')
    elif data in ['Redmi', 'Samsung']:
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobiles': mobiles, 'totalitem': totalitem})

# Handle customer registration
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully.')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})

# Display and update user profile
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})

    def post(self, request):
        totalitem = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            reg = Customer(
                user=usr,
                name=form.cleaned_data['name'],
                locality=form.cleaned_data['locality'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zipcode=form.cleaned_data['zipcode']
            )
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully.')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})
