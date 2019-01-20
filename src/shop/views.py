from django.shortcuts import render, get_object_or_404
from .models import Category, Product

from cart.forms import CartAddProductForm

def product_list(request):
    products = Product.active.all()
    bestseller = Product.objects.filter(is_bestseller=True)
    featured = Product.featured.all()
    return render(request,'shop/product/list.html',{ 'products': products, 'featured':featured, 'bestseller':bestseller})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,id=id,slug=slug,available=True)
    categories = product.categories.filter(is_active=True)
    cart_product_form = CartAddProductForm()
    return render(request,'shop/product/detail.html',{'product': product,'cart_product_form': cart_product_form, 'categories':categories})

def product_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.product_set.all()
    page_title = category.name
    # meta_keywords = category.meta_keywords
    # meta_description = category.meta_description
    return render(request, "shop/product/category.html", {'category':category, 'products':products})







