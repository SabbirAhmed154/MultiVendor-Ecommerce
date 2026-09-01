from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator

from accounts.models import Profile

from .models import (
    Product,
    Category,
    Review,
)

from .forms import (
    ProductForm,
    CategoryForm,
    ReviewForm,
    ProductVariantForm,
    ProductImageForm,
)


# ==================================================
# CHECK USER IS SELLER
# ==================================================
def is_seller(user):

    if not user.is_authenticated:
        return False

    return Profile.objects.filter(
        user=user,
        role='seller'
    ).exists()


# ==================================================
# HOMEPAGE
# ==================================================
def home(request):

    # Featured products
    featured_products = Product.objects.filter(
        is_active=True
    ).annotate(
        average_rating=Avg('reviews__rating')
    ).order_by(
        '-average_rating',
        '-created_at'
    )[:6]

    # Latest products
    latest_products = Product.objects.filter(
        is_active=True
    ).order_by(
        '-created_at'
    )[:6]

    # Categories
    categories = Category.objects.all().order_by(
        'name'
    )

    # Top sellers
    top_sellers = User.objects.filter(
        products__is_active=True
    ).annotate(
        total_products=Count(
            'products',
            distinct=True
        ),
        seller_rating=Avg(
            'products__reviews__rating'
        )
    ).order_by(
        '-total_products'
    )[:4]

    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'categories': categories,
        'top_sellers': top_sellers,
    }

    return render(
        request,
        'store/home.html',
        context
    )


# ==================================================
# PUBLIC PRODUCT LIST / SHOP
# ==================================================
def product_list(request):

    products = Product.objects.filter(
        is_active=True
    ).annotate(
        average_rating=Avg('reviews__rating')
    )

    # Categories
    categories = Category.objects.all().order_by(
        'name'
    )

    # Sellers
    seller_ids = Product.objects.filter(
        is_active=True
    ).values_list(
        'seller_id',
        flat=True
    ).distinct()

    sellers = User.objects.filter(
        id__in=seller_ids
    ).order_by(
        'username'
    )

    # Brands
    brands = Product.objects.filter(
        is_active=True
    ).exclude(
        brand=''
    ).values_list(
        'brand',
        flat=True
    ).distinct().order_by(
        'brand'
    )


    # ==================================================
    # FILTER VALUES
    # ==================================================

    search = request.GET.get(
        'search',
        ''
    ).strip()

    category_id = request.GET.get(
        'category',
        ''
    )

    brand = request.GET.get(
        'brand',
        ''
    )

    min_price = request.GET.get(
        'min_price',
        ''
    )

    max_price = request.GET.get(
        'max_price',
        ''
    )

    seller_id = request.GET.get(
        'seller',
        ''
    )

    rating = request.GET.get(
        'rating',
        ''
    )


    # ==================================================
    # SEARCH
    # ==================================================

    if search:

        products = products.filter(
            Q(name__icontains=search)
            |
            Q(description__icontains=search)
            |
            Q(category__name__icontains=search)
            |
            Q(seller__username__icontains=search)
            |
            Q(brand__icontains=search)
        )


    # ==================================================
    # CATEGORY FILTER
    # ==================================================

    if category_id:

        products = products.filter(
            category_id=category_id
        )


    # ==================================================
    # BRAND FILTER
    # ==================================================

    if brand:

        products = products.filter(
            brand__iexact=brand
        )


    # ==================================================
    # MINIMUM PRICE FILTER
    # ==================================================

    if min_price:

        try:

            minimum = Decimal(
                min_price
            )

            if minimum >= 0:

                products = products.filter(
                    price__gte=minimum
                )

            else:
                min_price = ''

        except (
            InvalidOperation,
            ValueError
        ):
            min_price = ''


    # ==================================================
    # MAXIMUM PRICE FILTER
    # ==================================================

    if max_price:

        try:

            maximum = Decimal(
                max_price
            )

            if maximum >= 0:

                products = products.filter(
                    price__lte=maximum
                )

            else:
                max_price = ''

        except (
            InvalidOperation,
            ValueError
        ):
            max_price = ''


    # ==================================================
    # SELLER FILTER
    # ==================================================

    if seller_id:

        products = products.filter(
            seller_id=seller_id
        )


    # ==================================================
    # RATING FILTER
    # ==================================================

    if rating:

        try:

            rating_value = int(
                rating
            )

            if 1 <= rating_value <= 5:

                products = products.filter(
                    average_rating__gte=rating_value
                )

            else:
                rating = ''

        except ValueError:
            rating = ''


    # ==================================================
    # ORDER PRODUCTS
    # ==================================================

    products = products.order_by(
        '-created_at'
    )


    # ==================================================
    # PAGINATION
    # 24 PRODUCTS PER PAGE
    # ==================================================

    paginator = Paginator(
        products,
        24
    )

    page_number = request.GET.get(
        'page'
    )

    products = paginator.get_page(
        page_number
    )


    # ==================================================
    # CONTEXT
    # ==================================================

    context = {
        'products': products,
        'categories': categories,
        'sellers': sellers,
        'brands': brands,

        'search': search,
        'selected_category': category_id,
        'selected_brand': brand,
        'min_price': min_price,
        'max_price': max_price,
        'selected_seller': seller_id,
        'selected_rating': rating,
    }


    return render(
        request,
        'store/product_list.html',
        context
    )


# ==================================================
# PRODUCT DETAILS
# ==================================================
def product_detail(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk,
        is_active=True
    )

    reviews = product.reviews.all().order_by(
        '-created_at'
    )

    average_rating = reviews.aggregate(
        Avg('rating')
    )['rating__avg']

    review_form = ReviewForm()

    variants = product.variants.all()

    gallery_images = product.images.all()

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form': review_form,
        'variants': variants,
        'gallery_images': gallery_images,
    }

    return render(
        request,
        'store/product_detail.html',
        context
    )


# ==================================================
# SELLER PRODUCT LIST
# ==================================================
@login_required
def seller_product_list(request):

    if not is_seller(
        request.user
    ):
        return redirect(
            'role_dashboard'
        )

    products = Product.objects.filter(
        seller=request.user
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'store/seller_product_list.html',
        {
            'products': products
        }
    )


# ==================================================
# ADD PRODUCT
# ==================================================
@login_required
def product_add(request):

    if not is_seller(
        request.user
    ):
        return redirect(
            'role_dashboard'
        )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            product = form.save(
                commit=False
            )

            product.seller = request.user

            product.save()

            messages.success(
                request,
                'Product added successfully!'
            )

            return redirect(
                'seller_product_list'
            )

    else:

        form = ProductForm()

    return render(
        request,
        'store/product_form.html',
        {
            'form': form,
            'title': 'Add Product'
        }
    )


# ==================================================
# EDIT PRODUCT
# ==================================================
@login_required
def product_edit(request, pk):

    if not is_seller(
        request.user
    ):
        return redirect(
            'role_dashboard'
        )

    product = get_object_or_404(
        Product,
        pk=pk,
        seller=request.user
    )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Product updated successfully!'
            )

            return redirect(
                'seller_product_list'
            )

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        'store/product_form.html',
        {
            'form': form,
            'title': 'Edit Product'
        }
    )


# ==================================================
# DELETE PRODUCT
# ==================================================
@login_required
def product_delete(request, pk):

    if not is_seller(
        request.user
    ):
        return redirect(
            'role_dashboard'
        )

    product = get_object_or_404(
        Product,
        pk=pk,
        seller=request.user
    )

    if request.method == 'POST':

        product.delete()

        messages.success(
            request,
            'Product deleted successfully!'
        )

        return redirect(
            'seller_product_list'
        )

    return render(
        request,
        'store/product_confirm_delete.html',
        {
            'product': product
        }
    )


# ==================================================
# ADD CATEGORY
# ==================================================
@login_required
def category_add(request):

    if not is_seller(
        request.user
    ):
        return redirect(
            'role_dashboard'
        )

    if request.method == 'POST':

        form = CategoryForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Category added successfully!'
            )

            return redirect(
                'product_add'
            )

    else:

        form = CategoryForm()

    return render(
        request,
        'store/category_form.html',
        {
            'form': form
        }
    )


# ==================================================
# ADD REVIEW
# ==================================================
@login_required
def add_review(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    existing_review = Review.objects.filter(
        product=product,
        user=request.user
    ).first()

    if existing_review:

        messages.warning(
            request,
            'You already reviewed this product.'
        )

        return redirect(
            'product_detail',
            pk=product.id
        )

    if request.method == 'POST':

        form = ReviewForm(
            request.POST
        )

        if form.is_valid():

            review = form.save(
                commit=False
            )

            review.product = product
            review.user = request.user

            review.save()

            messages.success(
                request,
                'Review submitted successfully!'
            )

    return redirect(
        'product_detail',
        pk=product.id
    )


# ==================================================
# EDIT REVIEW
# ==================================================
@login_required
def edit_review(request, review_id):

    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )

    if request.method == 'POST':

        form = ReviewForm(
            request.POST,
            instance=review
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Review updated successfully!'
            )

            return redirect(
                'product_detail',
                pk=review.product.id
            )

    else:

        form = ReviewForm(
            instance=review
        )

    return render(
        request,
        'store/edit_review.html',
        {
            'form': form,
            'review': review
        }
    )


# ==================================================
# DELETE REVIEW
# ==================================================
@login_required
def delete_review(request, review_id):

    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )

    product_id = review.product.id

    if request.method == 'POST':

        review.delete()

        messages.success(
            request,
            'Review deleted successfully!'
        )

    return redirect(
        'product_detail',
        pk=product_id
    )


# ==================================================
# PUBLIC SELLER STORE
# ==================================================
def seller_store(request, seller_id):

    seller = get_object_or_404(
        User,
        id=seller_id
    )

    products = Product.objects.filter(
        seller=seller,
        is_active=True
    ).order_by(
        '-created_at'
    )

    total_products = products.count()

    average_rating = Review.objects.filter(
        product__seller=seller
    ).aggregate(
        Avg('rating')
    )['rating__avg']

    context = {
        'seller': seller,
        'products': products,
        'total_products': total_products,
        'average_rating': average_rating,
    }

    return render(
        request,
        'store/seller_store.html',
        context
    )


# ==================================================
# ADD PRODUCT VARIANT
# ==================================================
@login_required
def variant_add(request, product_id):

    if not is_seller(
        request.user
    ):
        return redirect(
            'role_dashboard'
        )

    product = get_object_or_404(
        Product,
        id=product_id,
        seller=request.user
    )

    if request.method == 'POST':

        form = ProductVariantForm(
            request.POST
        )

        if form.is_valid():

            variant = form.save(
                commit=False
            )

            variant.product = product

            variant.save()

            messages.success(
                request,
                'Product variant added successfully!'
            )

            return redirect(
                'seller_product_list'
            )

    else:

        form = ProductVariantForm()

    return render(
        request,
        'store/product_variant_form.html',
        {
            'form': form,
            'product': product
        }
    )


# ==================================================
# ADD EXTRA PRODUCT IMAGE
# ==================================================
@login_required
def product_image_add(request, product_id):

    if not is_seller(
        request.user
    ):
        return redirect(
            'role_dashboard'
        )

    product = get_object_or_404(
        Product,
        id=product_id,
        seller=request.user
    )

    if request.method == 'POST':

        form = ProductImageForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            product_image = form.save(
                commit=False
            )

            product_image.product = product

            product_image.save()

            messages.success(
                request,
                'Product image added successfully!'
            )

            return redirect(
                'seller_product_list'
            )

    else:

        form = ProductImageForm()

    return render(
        request,
        'store/product_image_form.html',
        {
            'form': form,
            'product': product
        }
    )