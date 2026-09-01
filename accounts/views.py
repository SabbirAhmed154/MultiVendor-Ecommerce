from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from store.models import Product
from orders.models import OrderItem

from .forms import (
    CustomerRegisterForm,
    SellerRegisterForm,
)

from .models import Profile


# ===============================
# CUSTOMER REGISTER
# ===============================

def customer_register(request):

    if request.user.is_authenticated:
        return redirect('role_dashboard')

    form = CustomerRegisterForm(
        request.POST or None
    )

    if form.is_valid():

        user = form.save()

        user.email = form.cleaned_data[
            'email'
        ]

        user.save()

        Profile.objects.create(
            user=user,
            role='customer',
            phone=form.cleaned_data['phone'],
            address=form.cleaned_data['address']
        )

        return redirect('login')

    return render(
        request,
        'accounts/customer_register.html',
        {
            'form': form
        }
    )


# ===============================
# SELLER REGISTER
# ===============================

def seller_register(request):

    if request.user.is_authenticated:
        return redirect('role_dashboard')

    form = SellerRegisterForm(
        request.POST or None
    )

    if form.is_valid():

        user = form.save()

        user.email = form.cleaned_data[
            'email'
        ]

        user.save()

        Profile.objects.create(
            user=user,
            role='seller',
            phone=form.cleaned_data['phone'],
            address=form.cleaned_data['address']
        )

        return redirect('login')

    return render(
        request,
        'accounts/seller_register.html',
        {
            'form': form
        }
    )


# ===============================
# ROLE DASHBOARD
# ===============================

@login_required
def role_dashboard(request):

    # Superuser
    if request.user.is_superuser:

        return redirect(
            '/admin/'
        )

    try:

        profile = request.user.profile

    except Profile.DoesNotExist:

        return redirect(
            'login'
        )

    if profile.role == 'seller':

        return redirect(
            'seller_dashboard'
        )

    return redirect(
        'customer_dashboard'
    )


# ===============================
# CUSTOMER DASHBOARD
# ===============================

@login_required
def customer_dashboard(request):

    return render(
        request,
        'accounts/customer_dashboard.html'
    )


# ===============================
# SELLER DASHBOARD
# ===============================

@login_required
def seller_dashboard(request):

    # -------------------------------
    # CHECK SELLER
    # -------------------------------

    profile = Profile.objects.filter(
        user=request.user
    ).first()

    if not profile or profile.role != 'seller':

        return redirect(
            'role_dashboard'
        )


    # -------------------------------
    # SELLER PRODUCTS
    # -------------------------------

    products = Product.objects.filter(
        seller=request.user
    )

    total_products = products.count()


    # -------------------------------
    # SELLER ORDER ITEMS
    # -------------------------------

    order_items = OrderItem.objects.filter(
        product__seller=request.user
    )

    # Unique orders
    total_orders = order_items.values(
        'order_id'
    ).distinct().count()


    # -------------------------------
    # ORDER STATUS
    # -------------------------------

    pending_orders = order_items.filter(
        status='Pending'
    ).count()

    delivered_items = order_items.filter(
        status='Delivered'
    )

    delivered_orders = delivered_items.count()


    # -------------------------------
    # TOTAL REVENUE
    # -------------------------------

    total_revenue = sum(
        item.price * item.quantity
        for item in delivered_items
    )


    # -------------------------------
    # BEST SELLING PRODUCT
    # -------------------------------

    best_selling_product = (
        delivered_items
        .values(
            'product__name'
        )
        .annotate(
            total_sold=Sum('quantity')
        )
        .order_by(
            '-total_sold'
        )
        .first()
    )


    # -------------------------------
    # RECENT ORDERS
    # -------------------------------

    recent_orders = order_items.order_by(
        '-id'
    )[:5]


    # -------------------------------
    # CONTEXT
    # -------------------------------

    context = {

        'total_products':
            total_products,

        'total_orders':
            total_orders,

        'pending_orders':
            pending_orders,

        'delivered_orders':
            delivered_orders,

        'total_revenue':
            total_revenue,

        'best_selling_product':
            best_selling_product,

        'recent_orders':
            recent_orders,
    }


    return render(
        request,
        'accounts/seller_dashboard.html',
        context
    )