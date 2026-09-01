from decimal import Decimal

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from cart.models import CartItem
from store.models import Product, ProductVariant
from accounts.models import Profile

from .models import Order, OrderItem, Coupon
from .forms import CheckoutForm


# ==================================
# CHECK SELLER
# ==================================
def is_seller(user):

    if not user.is_authenticated:
        return False

    return Profile.objects.filter(
        user=user,
        role='seller'
    ).exists()


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
# CHECKOUT
# ==================================
@login_required
def checkout(request):

    if not is_customer(request.user):
        return redirect('role_dashboard')

    cart_items = CartItem.objects.filter(
        user=request.user
    ).select_related(
        'product',
        'variant'
    )

    # EMPTY CART CHECK
    if not cart_items.exists():

        messages.warning(
            request,
            'Your cart is empty.'
        )

        return redirect('cart_detail')


    # NORMAL SUBTOTAL
    subtotal = sum(
        (
            item.subtotal()
            for item in cart_items
        ),
        Decimal('0.00')
    )


    # COUPON
    coupon = None

    discount = Decimal('0.00')

    final_total = subtotal

    coupon_id = request.session.get(
        'coupon_id'
    )


    if coupon_id:

        coupon = Coupon.objects.filter(
            id=coupon_id,
            is_active=True
        ).first()


        if coupon:

            discount_percent = Decimal(
                str(
                    coupon.discount_percent
                )
            )

            discount = (
                subtotal
                * discount_percent
                / Decimal('100')
            )

            final_total = (
                subtotal - discount
            )

            if final_total < 0:

                final_total = Decimal(
                    '0.00'
                )

        else:

            request.session.pop(
                'coupon_id',
                None
            )


    # PLACE ORDER
    if request.method == 'POST':

        form = CheckoutForm(
            request.POST
        )


        if form.is_valid():

            with transaction.atomic():

                # STOCK CHECK
                for item in cart_items:

                    # VARIANT PRODUCT
                    if item.variant:

                        variant = (
                            ProductVariant.objects
                            .select_for_update()
                            .get(
                                id=item.variant.id,
                                product=item.product
                            )
                        )

                        if item.quantity > variant.stock:

                            messages.error(
                                request,
                                (
                                    f'Not enough stock for '
                                    f'{item.product.name}.'
                                )
                            )

                            return redirect(
                                'cart_detail'
                            )

                    # NORMAL PRODUCT
                    else:

                        product = (
                            Product.objects
                            .select_for_update()
                            .get(
                                id=item.product.id
                            )
                        )

                        if item.quantity > product.stock:

                            messages.error(
                                request,
                                (
                                    f'Not enough stock for '
                                    f'{product.name}.'
                                )
                            )

                            return redirect(
                                'cart_detail'
                            )


                # CREATE ORDER
                order = Order.objects.create(

                    user=request.user,

                    full_name=form.cleaned_data[
                        'full_name'
                    ],

                    phone=form.cleaned_data[
                        'phone'
                    ],

                    address=form.cleaned_data[
                        'address'
                    ],

                    payment_method='COD',

                    status='Pending',

                    total_amount=final_total
                )


                # CREATE ORDER ITEMS
                for item in cart_items:

                    product = Product.objects.get(
                        id=item.product.id
                    )


                    # VARIANT PRODUCT
                    if item.variant:

                        variant = (
                            ProductVariant.objects
                            .select_for_update()
                            .get(
                                id=item.variant.id,
                                product=product
                            )
                        )


                        OrderItem.objects.create(

                            order=order,

                            product=product,

                            variant=variant,

                            variant_color=variant.color,

                            variant_size=variant.size,

                            variant_storage=variant.storage,

                            quantity=item.quantity,

                            price=variant.price,

                            status='Pending'
                        )


                        variant.stock -= (
                            item.quantity
                        )

                        variant.save()


                    # NORMAL PRODUCT
                    else:

                        product = (
                            Product.objects
                            .select_for_update()
                            .get(
                                id=product.id
                            )
                        )


                        OrderItem.objects.create(

                            order=order,

                            product=product,

                            variant=None,

                            variant_color='',

                            variant_size='',

                            variant_storage='',

                            quantity=item.quantity,

                            price=product.price,

                            status='Pending'
                        )


                        product.stock -= (
                            item.quantity
                        )

                        product.save()


                # CLEAR CART
                cart_items.delete()


                # CLEAR COUPON
                request.session.pop(
                    'coupon_id',
                    None
                )


            messages.success(
                request,
                'Order placed successfully!'
            )


            return redirect(
                'order_success',
                order_id=order.id
            )


    else:

        form = CheckoutForm()


    return render(
        request,
        'orders/checkout.html',
        {
            'form': form,
            'cart_items': cart_items,
            'subtotal': subtotal,
            'discount': discount,
            'final_total': final_total,
            'coupon': coupon,

            # Old template compatibility
            'total': final_total,
        }
    )


# ==================================
# ORDER SUCCESS
# ==================================
@login_required
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'orders/order_success.html',
        {
            'order': order
        }
    )


# ==================================
# CUSTOMER ORDER HISTORY
# ==================================
@login_required
def order_history(request):

    if not is_customer(request.user):

        return redirect(
            'role_dashboard'
        )

    orders = Order.objects.filter(
        user=request.user
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'orders/order_history.html',
        {
            'orders': orders
        }
    )


# ==================================
# ORDER DETAILS / TRACKING
# ==================================
@login_required
def order_detail(request, order_id):

    if not is_customer(request.user):

        return redirect(
            'role_dashboard'
        )

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    order_items = (
        order.items
        .select_related(
            'product',
            'variant'
        )
        .all()
    )

    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order,
            'order_items': order_items
        }
    )


# ==================================
# SELLER ORDER LIST
# ==================================
@login_required
def seller_order_list(request):

    if not is_seller(request.user):

        return redirect(
            'role_dashboard'
        )

    order_items = OrderItem.objects.filter(
        product__seller=request.user
    ).select_related(
        'order',
        'order__user',
        'product',
        'variant'
    ).order_by(
        '-order__created_at'
    )

    return render(
        request,
        'orders/seller_order_list.html',
        {
            'order_items': order_items,

            'status_choices':
                OrderItem.STATUS_CHOICES
        }
    )


# ==================================
# SELLER UPDATE ORDER STATUS
# ==================================
@login_required
def seller_update_order_status(
    request,
    item_id
):

    if not is_seller(request.user):

        return redirect(
            'role_dashboard'
        )


    # Seller can update only
    # their own product order
    order_item = get_object_or_404(
        OrderItem,
        id=item_id,
        product__seller=request.user
    )


    if request.method == 'POST':

        new_status = request.POST.get(
            'status'
        )


        valid_statuses = [
            choice[0]
            for choice
            in OrderItem.STATUS_CHOICES
        ]


        if new_status in valid_statuses:

            # UPDATE ITEM STATUS
            order_item.status = new_status

            order_item.save(
                update_fields=[
                    'status'
                ]
            )


            # ==================================
            # UPDATE MAIN ORDER STATUS
            # ==================================

            order = order_item.order

            statuses = list(
                order.items.values_list(
                    'status',
                    flat=True
                )
            )


            # All items delivered
            if statuses and all(
                status == 'Delivered'
                for status in statuses
            ):

                order.status = 'Delivered'


            # All items cancelled
            elif statuses and all(
                status == 'Cancelled'
                for status in statuses
            ):

                order.status = 'Cancelled'


            # At least one shipped
            elif 'Shipped' in statuses:

                order.status = 'Shipped'


            # At least one packed
            elif 'Packed' in statuses:

                order.status = 'Packed'


            # At least one confirmed
            elif 'Confirmed' in statuses:

                order.status = 'Confirmed'


            # Otherwise pending
            else:

                order.status = 'Pending'


            order.save(
                update_fields=[
                    'status'
                ]
            )


            messages.success(
                request,
                (
                    'Order status updated '
                    'successfully.'
                )
            )


        else:

            messages.error(
                request,
                'Invalid order status.'
            )


    return redirect(
        'seller_order_list'
    )