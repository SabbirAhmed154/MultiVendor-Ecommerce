from django import forms

from .models import (
    Product,
    Category,
    Review,
    ProductVariant,
    ProductImage,
)


# =========================
# PRODUCT FORM
# =========================
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            'category',
            'name',
            'brand',
            'description',
            'price',
            'stock',
            'image',
            'is_active',
        ]

        widgets = {

            'category': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Product name'
                }
            ),

            'brand': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: Samsung, Apple, HP'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Product description'
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'step': '0.01'
                }
            ),

            'stock': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0'
                }
            ),

            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            ),
        }


# =========================
# CATEGORY FORM
# =========================
class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = [
            'name'
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Category name'
                }
            ),
        }


# =========================
# REVIEW FORM
# =========================
class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = [
            'rating',
            'comment'
        ]

        widgets = {

            'rating': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Write your review...'
                }
            ),
        }


# =========================
# PRODUCT VARIANT FORM
# =========================
class ProductVariantForm(forms.ModelForm):

    class Meta:
        model = ProductVariant

        fields = [
            'color',
            'size',
            'storage',
            'price',
            'stock'
        ]

        widgets = {

            'color': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: Black'
                }
            ),

            'size': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: M / L / XL'
                }
            ),

            'storage': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: 128GB'
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'step': '0.01'
                }
            ),

            'stock': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0'
                }
            ),
        }


# =========================
# PRODUCT IMAGE FORM
# =========================
class ProductImageForm(forms.ModelForm):

    class Meta:
        model = ProductImage

        fields = [
            'image'
        ]

        widgets = {

            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }