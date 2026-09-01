from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import Profile
from store.models import Product, ProductVariant
from orders.models import Coupon

from .models import CartItem, WishlistItem


# ==================================
# CHECK CUSTOMER
# ==================================
def is_customer(user):

    if not user.is_authenticated:
        return False

    return Profile.objects.filter(
        user=user,
        role='customer'
    ).exists()


# ==================================
# WISHLIST PAGE
# ==================================
@login_required
def wishlist_detail(request):

    if not is_customer(request.user):
        return redirect('role_dashboard')

    wishlist_items = WishlistItem.objects.filter(
        user=request.user
    ).select_related('product')

    return render(
        request,
        'cart/wishlist.html',
        {
            'wishlist_items': wishlist_items
        }
    )


# ==================================
# ADD TO WISHLIST
# ==================================
@login_required
def add_to_wishlist(request, product_id):

    if not is_customer(request.user):
        return redirect('role_dashboard')

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    wishlist_item, created = WishlistItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        messages.success(
            request,
            'Product added to wishlist.'
        )

    else:
        messages.info(
            request,
            'Product is already in your wishlist.'
        )

    return redirect('wishlist_detail')


# ==================================
# REMOVE FROM WISHLIST
# ==================================
@login_required
def remove_from_wishlist(request, item_id):

    if not is_customer(request.user):
        return redirect('role_dashboard')

    item = get_object_or_404(
        WishlistItem,
        id=item_id,
        user=request.user
    )

    item.delete()

    messages.success(
        request,
        'Product removed from wishlist.'
    )

    return redirect('wishlist_detail')


# ==================================
# WISHLIST TO CART
# ==================================
@login_required
def wishlist_to_cart(request, item_id):

    if not is_customer(request.user):
        return redirect('role_dashboard')

    wishlist_item = get_object_or_404(
        WishlistItem,
        id=item_id,
        user=request.user
    )

    product = wishlist_item.product

    # Variant product hole age variant select korte hobe
    if product.variants.exists():

        messages.info(
            request,
            'Please select a product variant first.'
        )

        return redirect(
            'product_detail',
            pk=product.id
        )

    if product.stock <= 0:

        messages.error(
            request,
            'This product is out of stock.'
        )

        return redirect('wishlist_detail')

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        variant=None
    )

    if created:

        cart_item.quantity = 1

    else:

        if cart_item.quantity >= product.stock:

            messages.warning(
                request,
                'Maximum available stock reached.'
            )

            return redirect('wishlist_detail')

        cart_item.quantity += 1

    cart_item.save()

    wishlist_item.delete()

    messages.success(
        request,
        'Product moved to cart.'
    )

    return redirect('cart_detail')


# ==================================
# CART PAGE
# ==================================
@login_required
def cart_detail(request):

    if not is_customer(request.user):
        return redirect('role_dashboard')

    cart_items = CartItem.objects.filter(
        user=request.user
    ).select_related(
        'product',
        'variant'
    )

    subtotal = sum(
        item.subtotal()
        for item in cart_items
    )

    discount = 0
    final_total = subtotal
    coupon = None

    coupon_id = request.session.get('coupon_id')

    if coupon_id:

        coupon = Coupon.objects.filter(
            id=coupon_id,
            is_active=True
        ).first()

        if coupon:

            discount = (
                subtotal * coupon.discount_percent
            ) / 100

            final_total = subtotal - discount

        else:

            request.session.pop(
                'coupon_id',
                None
            )

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount': discount,
        'final_total': final_total,
        'coupon': coupon,

        # Compatibility
        'total': final_total,
    }

    return render(
        request,
        'cart/cart_detail.html',
        context
    )


# ==================================
# APPLY COUPON
# ==================================
@login_required
def apply_coupon(request):

    if not is_customer(request.user):
        return redirect('role_dashboard')

    if request.method == 'POST':

        code = request.POST.get(
            'coupon_code',
            ''
        ).strip()

        coupon = Coupon.objects.filter(
            code__iexact=code,
            is_active=True
        ).first()

        if coupon:

            request.session['coupon_id'] = coupon.id

            messages.success(
                request,
                f'Coupon {coupon.code} applied successfully!'
            )

        else:

            request.session.pop(
                'coupon_id',
                None
            )

            messages.error(
                request,
                'Invalid coupon code.'
            )

    return redirect('cart_detail')


# ==================================
# REMOVE COUPON
# ==================================
@login_required
def remove_coupon(request):

    if not is_customer(request.user):
        return redirect('role_dashboard')

    request.session.pop(
        'coupon_id',
        None
    )

    messages.success(
        request,
        'Coupon removed successfully.'
    )

    return redirect('cart_detail')


# ==================================
# ADD TO CART
# ==================================
@login_required
def add_to_cart(request, product_id):

    if not is_customer(request.user):
        return redirect('role_dashboard')

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    variant_id = request.POST.get('variant_id')

    variant = None

    # Variant product
    if product.variants.exists():

        if not variant_id:

            messages.warning(
                request,
                'Please select a variant.'
            )

            return redirect(
                'product_detail',
                pk=product.id
            )

        variant = get_object_or_404(
            ProductVariant,
            id=variant_id,
            product=product
        )

        if variant.stock <= 0:

            messages.error(
                request,
                'Selected variant is out of stock.'
            )

            return redirect(
                'product_detail',
                pk=product.id
            )

        available_stock = variant.stock

    # Normal product
    else:

        if product.stock <= 0:

            messages.error(
                request,
                'This product is out of stock.'
            )

            return redirect(
                'product_detail',
                pk=product.id
            )

        available_stock = product.stock

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        variant=variant
    )

    if created:

        cart_item.quantity = 1

    else:

        if cart_item.quantity >= available_stock:

            messages.warning(
                request,
                'You cannot add more than available stock.'
            )

            return redirect('cart_detail')

        cart_item.quantity += 1

    cart_item.save()

    messages.success(
        request,
        'Product added to cart.'
    )

    return redirect('cart_detail')


# ==================================
# INCREASE QUANTITY
# ==================================
@login_required
def increase_quantity(request, item_id):

    if not is_customer(request.user):
        return redirect('role_dashboard')

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )

    if cart_item.variant:
        available_stock = cart_item.variant.stock

    else:
        available_stock = cart_item.product.stock

    if cart_item.quantity < available_stock:

        cart_item.quantity += 1
        cart_item.save()

    else:

        messages.warning(
            request,
            'Maximum available stock reached.'
        )

    return redirect('cart_detail')


# ==================================
# DECREASE QUANTITY
# ==================================
@login_required
def decrease_quantity(request, item_id):

    if not is_customer(request.user):
        return redirect('role_dashboard')

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )

    if cart_item.quantity > 1:

        cart_item.quantity -= 1
        cart_item.save()

    else:

        cart_item.delete()

    return redirect('cart_detail')


# ==================================
# REMOVE FROM CART
# ==================================
@login_required
def remove_from_cart(request, item_id):

    if not is_customer(request.user):
        return redirect('role_dashboard')

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )

    cart_item.delete()

    messages.success(
        request,
        'Product removed from cart.'
    )

    return redirect('cart_detail')